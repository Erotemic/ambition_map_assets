# ambition_map_assets

Submodule for keeping LDtk bloat out of the main repo.

LDtk worlds are the densest content Ambition tracks: **six files, ~5 MB**, and
they grow as the game is actually built. They compress well in a pack (git
deltas the rewritten JSON ~146x) but every checkout and every archive tarball
carries them at full size. That is the cost this repo exists to remove.

## Layout mirrors the consuming crate

```
ambition_content/worlds/       -> game/ambition_content/assets/worlds/
ambition_demo_mary_o/worlds/   -> game/ambition_demo_mary_o/assets/worlds/
ambition_demo_sanic/worlds/    -> game/ambition_demo_sanic/assets/worlds/
```

The directory name is the crate the world belongs to, so a file's destination is
derivable from its path here and needs no lookup table.

## How it reaches the game: tracked symlinks

The main repo mounts this at `game/ambition_map_assets` and tracks a **symlink**
at each original path, e.g.

```
game/ambition_content/assets/worlds/sandbox.ldtk
  -> ../../../ambition_map_assets/ambition_content/worlds/sandbox.ldtk
```

Git stores symlinks natively (mode 120000), so a fresh clone gets them for free
— no setup script creates them.

⭐ **A symlink rather than a bind mount or hardlink is deliberate.** Those look
like real content to git and would be committed straight back into the main
repo, undoing the whole thing. A symlink stays a pointer — and when this
submodule is not checked out the links **dangle visibly**, which is the loud
failure you want. An uninitialized direct mount is just an empty directory, and
fails silently.

⚠ **Searching still works.** The files here are real, so a recursive grep from
the superproject root finds them at this path. It does not *also* find them at
the symlinked path, which is a deduplication rather than a blind spot. (This is
unlike the generated-sprite mirroring in `scripts/mirror_assets_for_worktree.py`,
where the real files live in a different checkout entirely.)

## ⛔ Never `json.dumps` a `.ldtk`

It collapses the editor's formatting, and `ldtk repair` does **not** restore it —
the result is a diff touching every line of a multi-megabyte file. Write through
`dump_editor_style` (`tools/ambition_ldtk_tools/.../editor_format.py`), which is
what every writer in the toolkit already uses:

```python
path.write_text(dump_editor_style(project))
```

⭐ **`write_text` also preserves the symlink**, because it writes *through* the
link rather than replacing it. A tool that writes to a temp file and renames it
over the destination would silently destroy the symlink and leave a real file
that gets committed to the main repo. Every writer in the toolkit was checked
for this (2026-08-08) and none does an atomic replace — but the LDtk **editor**
is outside that guarantee, so the main repo checks that these paths are still
symlinks.
