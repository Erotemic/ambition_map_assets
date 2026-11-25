#!/usr/bin/env python3
"""Write the rooms of the Unfinished dimension, the one the Boss's agents are
still building (`docs/planning/game/unfinished-dimension.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/unfinished/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/unfinished/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Change the script, not the rooms.

The world file is `unfinished.ldtk`. The gate (address INSTALLING) stands
in the Staging Area. The Staging Area and the Draft join by an edge; the
Site Office is the cabin's inside, so its way in is a door:

      door
 [the Site Office]
        |
 [ the Staging Area ] ==== [ the Draft ]
                             (the void under it)

- `unfinished_staging`: the gate and terminal; the site cabin and its door;
  Subclause 4(b) at the survey post; the half-painted trees; the scaffold
  (decks at 512 and 384, a chest on top).
- `unfinished_draft`: the built ground ends; slabs on cranes' cables over
  the void, a jump apart, the painter's platform among them with Subclause
  4(c); the outlines between are drawings and hold nothing; a built corner
  at the east end with a chest. Bugs on the ground. The void is a hazard.
- `unfinished_site_office`: the gauges, the backlog, the Placeholder.

The robot's numbers (`district_kit`): a jump rises 83, a jump and a double
jump 139; a step of 64 is one jump, 128 a double jump.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
#: The shared generator code and the authoring tool stay in the main repo.
TOOL_ROOT = HERE.parents[4] / "tools" / "ambition_ldtk_tools"
TOOL_SPECS = TOOL_ROOT / "specs"
#: The area specs are made again on each run and not kept: the rooms are the truth.
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_unfinished_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))
sys.path.insert(0, str(HERE))

from district_kit import WALL, WORLDS, door, edge, ensure_world, entity, ledge, make_rooms, resident, room, run, sign, solid, start  # noqa: E402

import gates  # noqa: E402
from blurbs import BLURB  # noqa: E402
from props import scenery  # noqa: E402

WORLD = WORLDS / "unfinished.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/unfinished/make_specs.py"
UID_OFFSET = 1900000

STAGING = "unfinished_staging"
DRAFT = "unfinished_draft"
OFFICE = "unfinished_site_office"

BG = "#C8CED8"
MUSIC = "something_worth_building"

#: Each room: where it is on the flat map, and its size. The Staging Area
#: and the Draft are side by side, their floors at one height where they
#: join; the Site Office is above the Staging Area.
ROOMS_AT = {
    STAGING: ((0, 0), (2400, 768)),
    DRAFT: ((2400, 0), (2400, 1152)),
    OFFICE: ((608, -640), (1280, 576)),
}

#: The Staging Area (`targets/props/unfinished_props.py` draws to these).
FLOOR = 640
CABIN_DOOR_X = 716
SCAFFOLD = (1800, 2040)
DECKS = (512, 384)
#: The Draft.
GROUND_END = 600
SLABS = ((700, 860, 640), (960, 1120, 576), (1220, 1380, 640), (1740, 1900, 640), (2000, 2160, 576))
PAINTER = (1460, 1640, 560)
CORNER = 2240
VOID_TOP = 1120
#: The Site Office.
OFFICE_FLOOR = 512


def blurb(rid, x):
    """The room's blurb (`blurbs.py`): two lines under its title."""
    out = []
    for n, text in enumerate(BLURB[rid]):
        w = len(text) * 9 + 24
        out.append(entity("DebugLabel", x - w // 2, 64 + n * 24, w, 24, name=f"{rid}_blurb_{n}", text=text, category="Room"))
    return out


def chest(name, reward, x, floor):
    return entity("ChestSpawn", x, floor - 58, 76, 58, name=name, reward=reward)


def bug(rid, n, x, floor):
    """A Bug on the ground at `x`."""
    return entity("EnemySpawn", x - 20, floor - 40, 40, 40, name=f"{rid}_glitch_bug_{n}", brain="combatant",
                  character_id="glitch_bug", respawn="OnRoomReenter")


def build(rid, e, title, biome, dangerous=False):
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e + blurb(rid, size[0] // 2), at=at, size=size, biome=biome, music=MUSIC, bg=BG, title=title,
                generator=GENERATOR, dangerous=dangerous)
    return rid, text


def staging():
    rid = STAGING
    w, h = ROOMS_AT[rid][1]
    s0, s1 = SCAFFOLD
    e = [
        solid("ground", 0, FLOOR, w, h - FLOOR),
        solid("west_wall", 0, 0, WALL, FLOOR),
        solid("east_wall", w - WALL, 0, WALL, FLOOR - 96),
        edge("staging_to_draft", "east, to the Draft", w - WALL, FLOOR, DRAFT, "draft_to_staging"),
        # The gate (INSTALLING) and its terminal.
        *gates.as_ron(gates.ring("Staging Gate", "unfinished_staging_gate", 96, FLOOR, "the gate")),
        *gates.as_ron(gates.terminal("Staging Gate", "unfinished_gate_terminal", 400, FLOOR)),
        start(rid, 540, FLOOR),
        sign("staging_sign_gate", 300, FLOOR - 360, "INSTALLING: THE STAGING AREA", 320),
        # The site cabin; its door is the Site Office's.
        door("staging_office_door", "into the Site Office", CABIN_DOOR_X, FLOOR, OFFICE, "office_door"),
        sign("staging_sign_office", 740, 420, "SITE OFFICE", 200),
        # The survey post.
        resident("npc_unfinished_subclause_surveyor", "unfinished_surveyor", 1050, FLOOR, w=28, h=40),
        sign("staging_sign_dust", 1440, 260, "PARDON OUR DUST: A WORLD IS UNDER CONSTRUCTION", 460),
        # The scaffold.
        *[ledge(f"scaffold_deck_{n}", s0 - 6, top, s1 - s0 + 12) for n, top in enumerate(DECKS)],
        sign("staging_sign_soon", (s0 + s1) // 2, DECKS[1] + 44, "EXPECTED COMPLETION: SOON", 260),
        chest("a TODO", "currency:30", 1880, DECKS[1]),
    ]
    return build(rid, e, "THE STAGING AREA", "unfinished")


def draft():
    rid = DRAFT
    w, h = ROOMS_AT[rid][1]
    p0, p1, ptop = PAINTER
    e = [
        solid("built_ground", 0, FLOOR, GROUND_END, h - FLOOR),
        solid("west_wall", 0, 0, WALL, FLOOR - 96),
        edge("draft_to_staging", "west, to the Staging Area", 0, FLOOR, STAGING, "staging_to_draft"),
        start(rid, 120, FLOOR),
        # The slabs on the cranes' cables, and the painter's platform.
        *[solid(f"slab_{n}", x0, top, x1 - x0, 32) for n, (x0, x1, top) in enumerate(SLABS)],
        solid("painter_platform", p0, ptop, p1 - p0, 24),
        resident("npc_unfinished_subclause_painter", "unfinished_painter", 1590, ptop, w=28, h=40),
        sign("draft_sign_idea", 1420, 820, "NOT YET BUILT. PLEASE DO NOT STAND ON THE IDEA.", 460),
        # The built corner at the east end.
        solid("built_corner", CORNER, FLOOR, w - CORNER, h - FLOOR),
        solid("east_wall", w - WALL, 0, WALL, FLOOR),
        chest("a finished corner", "currency:40", 2280, FLOOR),
        sign("draft_sign_edge", 2300, 450, "EDGE OF THE DRAFT", 160),
        # The void.
        entity("HazardBlock", GROUND_END, VOID_TOP, CORNER - GROUND_END, h - VOID_TOP, name="the void"),
        sign("draft_sign_void", 1400, 1060, "THE VOID (RESERVED)", 300),
        # Bugs on the built ground.
        bug(rid, 0, 260, FLOOR),
        bug(rid, 1, 470, FLOOR),
    ]
    return build(rid, e, "THE DRAFT", "unfinished_void", dangerous=True)


def site_office():
    rid = OFFICE
    w, h = ROOMS_AT[rid][1]
    g = OFFICE_FLOOR
    e = [
        solid("floor", 0, g, w, h - g),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 32),
        door("office_door", "out to the Staging Area", 64, g, STAGING, "staging_office_door"),
        start(rid, 150, g),
        sign("office_sign_gravity", 300, 372, "GRAVITY", 160),
        sign("office_sign_weather", 540, 372, "WEATHER", 160),
        sign("office_sign_layers", 780, 372, "LAYERS", 160),
        sign("office_sign_backlog", 1080, 140, "BACKLOG", 200),
        sign("office_sign_todo_sky", 1080, 190, "TODO: SKY (EAST)", 260),
        sign("office_sign_todo_rest", 1080, 222, "TODO: THE REST", 260),
        sign("office_sign_done", 1080, 254, "DONE: THIS SIGN", 260),
        resident("npc_unfinished_placeholder", "unfinished_placeholder", 900, g),
    ]
    return build(rid, e, "THE SITE OFFICE", "unfinished")


ROOMS = (staging, draft, site_office)


def main(argv):
    paths = []
    for make in ROOMS:
        rid, text = make()
        path = SPEC_OUT / f"{rid}.ron"
        path.write_text(text)
        print(path)
        paths.append(path)
    if "--apply" not in argv:
        return 0
    if code := ensure_world(WORLD, UID_OFFSET):
        return code
    # A world made from the sandbox's defs has no `dangerous` level field.
    code, out = run("level", "add-field-def", "dangerous", "--type", "Bool", "--default", "false", "--doc",
                    "Out of town: an NPC on the player's side joins the player's fights here (RoomMetadata::dangerous).",
                    str(WORLD), "--in-place")
    if code and "already" not in out:
        return code
    if code := make_rooms(WORLD, paths, keep_position="--relayout" not in argv):
        return code
    code, _ = run("validate", str(WORLD))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
