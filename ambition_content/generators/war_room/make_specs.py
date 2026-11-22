#!/usr/bin/env python3
"""Write the War Room: the Supreme Leader's fight
(`docs/planning/game/bosses.md`, "The Supreme Leader").

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/war_room/make_specs.py          # writes the spec
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/war_room/make_specs.py --apply  # and makes the room
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/war_room/make_specs.py --apply --hall  # and the hall's door

Run it from the repository root. Change the script, not the room.

The room is in the Nazi Dimension's world file (`evil.ldtk`), joined to no
room of it: it is NOT Castle Godwin, and where it stands in the dimension
(the capital, or anywhere else) is the maintainer's to decide. Until then
the Hall of Bosses' door is the only way in, and the fight there is his one
placement (`hall.supreme_leader`): not a practice copy, so beating him pays
his chest and is saved. The hall's life switch brings him back.

    [ the Hall of Bosses ] -door-> [ the War Room ]

The floor is flat and open: his lines run its whole length. His Command
Uplink comes down 344 in from the west wall in his first phase and from the
east wall after (`ambition_content_modules::supreme_leader::UPLINK_INSET`):
the space behind it, by the wall, is out of its lines. Two ledges over the
floor (a double jump: 136) and a bar over the middle (a double jump again)
are out of the low line's way and in the decree's.

The robot's numbers (`platformer_defaults.ron`): a jump rises 88 px, a jump
and a double jump 139 px; the body is 30 x 48.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_war_room_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))

from district_kit import SANDBOX_LDTK, WALL, WORLDS, add_entities, door, entity, ledge, make_rooms, room, run, sign, solid, start  # noqa: E402

WORLD = WORLDS / "evil.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/war_room/make_specs.py"

ROOM = "hall_supreme_leader_war_room"
ENTRY = "hall_supreme_leader_war_room_entry"
HALL = "hall_of_bosses"
HALL_DOOR = "hall_to_supreme_leader_portal"
HALL_SWITCH = "hall_supreme_leader_life_switch"
#: His placement: his defeat is saved under this id.
PLACEMENT = "hall.supreme_leader"

#: Where the room is in the world (under every room of the dimension, out
#: of their way), and its size.
AT, W, H = (0, 8000), 1920, 768
FLOOR = 704
#: The regime's architecture (the castle's skin and backdrop: the look of
#: the regime, not the place) until the War Room has a backdrop of its own.
BIOME = "castle_godwin"
BG = "#0E0E14"
MUSIC = "military_iron_resolve"
#: The view: about 490 units high, the floor and the bar at once.
ZOOM = 1.6
#: A double jump.
TIER = 136
#: His body box (`npc_supreme_leader`), its feet on the floor at the middle.
LEADER_W, LEADER_H = 64, 150


def war_room():
    w, h = W, H
    e = [
        solid("ground", 0, FLOOR, w, h - FLOOR),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, FLOOR - 32),
        solid("east_wall", w - WALL, 32, WALL, FLOOR - 32),
        door(ENTRY, "back to the hall", 48, FLOOR, HALL, HALL_DOOR),
        start(ROOM, 150, FLOOR),
        # Two ledges a double jump over the floor, and a bar over the
        # middle a double jump over them.
        ledge("ledge_west", 520, FLOOR - TIER, 200),
        ledge("ledge_east", w - 720, FLOOR - TIER, 200),
        ledge("bar_middle", w // 2 - 100, FLOOR - 2 * TIER, 200),
        sign(f"{ROOM}_plan", w // 2, 96, "EVERYTHING IS PROCEEDING ACCORDING TO PLAN", 640),
        entity("BossSpawn", w // 2 - LEADER_W // 2, FLOOR - LEADER_H, LEADER_W, LEADER_H, name="the Supreme Leader",
               brain="PhaseScript:supreme_leader", encounter_id=PLACEMENT),
    ]
    return ROOM, room(ROOM, e, at=AT, size=(w, h), biome=BIOME, music=MUSIC, bg=BG, title="THE WAR ROOM",
                      generator=GENERATOR, zoom=ZOOM, dangerous=True)


#: The hall's door to the War Room and its life switch, on the hall's lower
#: floor between the Mockingbird's switch and the Mode Collapse's door
#: (`hall_of_bosses`, `sandbox.ldtk`).
HALL_DOOR_YAML = f"""# The Hall of Bosses' door to the Supreme Leader's War Room. Written by
# {GENERATOR}.
level_id: {HALL}
entities:
  - type: LoadingZone
    px: [720, 384]
    size: [48, 96]
    fields:
      id: {HALL_DOOR}
      name: "to the Supreme Leader"
      activation: Door
      target_room: {ROOM}
      target_zone: {ENTRY}
      bidirectional: true
  - type: Switch
    px: [776, 448]
    size: [24, 32]
    fields:
      id: {HALL_SWITCH}
      name: "Supreme Leader life switch"
      prompt: "Revive or defeat the Supreme Leader"
      target_encounter: {PLACEMENT}
      action: BossLife
"""


def main(argv):
    rid, text = war_room()
    path = SPEC_OUT / f"{rid}.ron"
    path.write_text(text)
    print(path)
    if "--apply" not in argv:
        return 0
    if code := make_rooms(WORLD, [path], keep_position="--relayout" not in argv):
        return code
    if "--hall" in argv:
        if code := add_entities(HALL_DOOR_YAML, SANDBOX_LDTK, SPEC_OUT / "hall_door.yaml", unless=HALL_DOOR):
            return code
        code, _ = run("validate", str(SANDBOX_LDTK))
        if code:
            return code
    code, _ = run("validate", str(WORLD))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
