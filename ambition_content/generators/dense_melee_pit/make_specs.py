#!/usr/bin/env python3
"""Write the dense-melee pit in the sandbox: a development room packed with
fighters that each build a tactical view (DENSE-MELEE-ROOM, Q93).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/dense_melee_pit/make_specs.py           # writes the spec
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/dense_melee_pit/make_specs.py --apply   # and makes the room

Run it from the repository root. It is a stress room, not game content: the
crowd is there to be measured (`scripts/measure/measure_perception_density.sh
--room dense_melee_pit`), and every owner of crowd cost (perception,
targeting, collision, VFX, camera framing, presentation) can measure in it.

⭐ THE ROOM IS NARROWER THAN ONE VIEWPORT. The hall spreads its cast so far
that each viewer keeps about 14 bodies whatever the population
(`bounded-perception-and-attention.md`); a body in this pit can see most of
the pit, so what a viewer keeps tracks the population until the attention
budget caps it. The cast is the goblin band and the lab raider: each names
the `medium_striker` policy, a Smash-template brain that builds the tactical
view. A `stand_still` cast builds no view and measures nothing.

The way in is a door at the east end of `basement_enemies`, the enemy
gallery, which this script adds to that room when it is missing.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
#: The shared generator code and the authoring tool stay in the main repo.
TOOL_ROOT = HERE.parents[4] / "tools" / "ambition_ldtk_tools"
TOOL_SPECS = TOOL_ROOT / "specs"
#: The area spec is made again on each run and not kept: the room is the truth.
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_dense_melee_pit_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))

from district_kit import WALL, WORLDS, add_entities, door, entity, ledge, make_rooms, room, sign, solid, start  # noqa: E402

WORLD = WORLDS / "sandbox.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/dense_melee_pit/make_specs.py"
PIT = "dense_melee_pit"
W, H, FLOOR, CEILING = 960, 448, 384, 64
#: East of every other sandbox room.
AT = (88320, 0)
#: The gallery's door to the pit: its left edge on the gallery floor, east of
#: the raider and the chest.
GALLERY, GALLERY_FLOOR, GALLERY_DOOR_X = "basement_enemies", 848, 1680
GALLERY_DOOR = "dense_melee_pit_door"
GALLERY_DOOR_NAME = "to the dense melee pit"
ENTRY = "dense_melee_pit_entry"
#: The crowd: four bodies that name the same tactical policy, so the
#: population varies and the brain does not. 200 is the population the
#: perception gate's structural clause names.
CAST = ("goblin", "goblin_raider", "goblin_squat", "npc_lab_raider")
POPULATION = 200
#: The two tiers the crowd stands on besides the floor: one-way ledges, so the
#: fight spills up and down rather than along one line.
LEDGES = ((160, 288, 224), (576, 288, 224))


def crowd():
    """`POPULATION` fighters, spread over the floor and the two ledges.

    Packed closer than a body is wide: the pit is a crowd, and a fighter that
    spawns inside another is pushed apart by the same rule as in any fight."""
    spots = [(x, FLOOR) for x in range(256, W - WALL - 32, 8)]
    for x0, top, width in LEDGES:
        spots += [(x, top) for x in range(x0 + 16, x0 + width - 16, 8)]
    out = []
    for n in range(POPULATION):
        x, feet = spots[n % len(spots)]
        character = CAST[n % len(CAST)]
        out.append(entity("EnemySpawn", x - 16, feet - 48, 32, 48, name=f"{PIT}_{character}_{n}",
                          brain="combatant", character_id=character))
    return out


def specs() -> dict[str, str]:
    pit = [
        solid("floor", 0, FLOOR, W, H - FLOOR),
        solid("ceiling", 0, 0, W, CEILING),
        solid("west wall", 0, CEILING, WALL, FLOOR - CEILING),
        solid("east wall", W - WALL, CEILING, WALL, FLOOR - CEILING),
        *(ledge(f"ledge {i}", x, top, width) for i, (x, top, width) in enumerate(LEDGES)),
        start(PIT, 96, FLOOR),
        door(ENTRY, "back to the enemy gallery", 48, FLOOR, GALLERY, GALLERY_DOOR),
        sign("pit sign", W // 2, CEILING + 16, f"Dense melee: {POPULATION} fighters, one tactical brain"),
        *crowd(),
    ]
    return {
        PIT: room(PIT, pit, at=AT, size=(W, H), title="Dense melee pit (development room)",
                  biome="basement", music="tech_bros_disruption", bg="#1e1a1a", generator=GENERATOR),
    }


def gallery_door() -> str:
    """The way in, as an `entity add` document for the gallery."""
    return f"""# The enemy gallery's door to the pit. Written by {GENERATOR}.
level_id: {GALLERY}
entities:
  - type: LoadingZone
    px: [{GALLERY_DOOR_X}, {GALLERY_FLOOR - 96}]
    size: [48, 96]
    fields:
      id: {GALLERY_DOOR}
      name: {GALLERY_DOOR_NAME}
      activation: Door
      target_room: {PIT}
      target_zone: {ENTRY}
      bidirectional: true
"""


def main(argv: list[str]) -> int:
    paths = []
    for rid, text in specs().items():
        path = SPEC_OUT / f"{rid}.ron"
        path.write_text(text)
        paths.append(path)
        print(f"wrote {path}")
    if "--apply" in argv:
        code = make_rooms(WORLD, paths)
        if code:
            return code
        # Keyed on the door's NAME: its id is in the file already, as the
        # target of the pit's own door.
        return add_entities(gallery_door(), WORLD, SPEC_OUT / "gallery_door.yaml", unless=f'"{GALLERY_DOOR_NAME}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
