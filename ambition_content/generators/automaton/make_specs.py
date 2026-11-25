#!/usr/bin/env python3
"""Write the rooms of the Automaton dimension, clockwork and cells
(`docs/planning/game/automaton-dimension.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/automaton/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/automaton/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Change the script, not the rooms.

The world file is `automaton.ldtk`. The gate (address CELLS) stands in the
Works. The Works, the Life field and the Cell-ular Arena join by edges; the
Tape Room is the clock tower's inside, so its way in is a door:

        door
  [the Tape Room]
         |
  [ the Works ] ==== [ the Life field ] ==== [ the Cell-ular Arena ]

- `automaton_works`: the gate and terminal; the Escapement Cafe; the water
  wheel; Busy Beaver at his stair of blocks (64 a step) up to a chest; the
  clock tower and its door.
- `automaton_life`: the edge comes in on a terrace at the Works' floor; four
  steps of 64 down to the field; Neighbour Moore by the block; a glider lift
  up to a pillar of cubes and a second up past it to the east terrace, the
  Sierpinski panel and a chest. Spaceships fly the field.
- `automaton_tape_room`: the tape on its spools, the Head on its rail, the
  table of states, the count.
- `automaton_arena`: the Perfect Cellular Automaton's ring (Jon, 2026-11-25:
  "PCA needs an arena to challenge people in the automaton dimension"). The
  edge comes in on a gallery at the Life field's east terrace; the failure
  log and the Imperfect Cellular Automaton are on the gallery; four steps
  of 64 go down to the ground, and the ring stands one jump high on it, the
  PCA in its middle. No ceiling: he flies. Its backdrop is its own
  (`automaton_arena`: the stands and the glider gun's screen); its terrain
  is the Life field's.

A glider lift is a `MovingPlatform` on a `KinematicPath` of two points, a
diagonal at 45 degrees, ping-ponging (a path's points are the platform's
centre, in the room's coordinates).

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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_automaton_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))
sys.path.insert(0, str(HERE))

from district_kit import WALL, WORLDS, door, edge, ensure_world, entity, ledge, make_rooms, resident, room, run, sign, solid, start  # noqa: E402

import gates  # noqa: E402
from blurbs import BLURB  # noqa: E402
from props import scenery  # noqa: E402

WORLD = WORLDS / "automaton.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/automaton/make_specs.py"
UID_OFFSET = 2000000

WORKS = "automaton_works"
LIFE = "automaton_life"
TAPE = "automaton_tape_room"
ARENA = "automaton_arena"

BG = "#B0AAD8"
#: The dimension's theme is the Busy Beaver's song (Jon, 2026-11-25). The PCA's
#: fight is `glider_gun`: its challenge starts it (`automaton.yarn`).
MUSIC = "busy_beaver"

#: Each room: where it is on the flat map, and its size. The Works and the
#: Life field are side by side, their floors at one height where they join;
#: the Tape Room is above the Works.
ROOMS_AT = {
    WORKS: ((0, 0), (2400, 768)),
    LIFE: ((2400, 0), (2400, 1024)),
    TAPE: ((800, -704), (1600, 640)),
    ARENA: ((4800, 0), (2048, 896)),
}

#: The Works (`targets/props/automaton_props.py` draws to these).
FLOOR = 640
STAIRS = ((1560, 576), (1624, 512), (1688, 448), (1752, 384))
STAIR_END = 1880
TOWER_DOOR_X = 2076
#: The Life field.
FIELD_FLOOR = 896
WEST_TERRACE_END = 544
STEPS = ((544, 608, 704), (608, 672, 768), (672, 736, 832))
PILLAR = (1280, 1440, 544)
TERRACE = (2040, 448)
#: Each glider lift: its low end and its high end (its centre), 45 degrees.
LIFTS = (((880, 872), (1200, 552)), ((1520, 600), (1880, 240)))
LIFT_SIZE = (112, 16)
LIFT_SPEED = 60.0
#: The Tape Room.
ROOM_FLOOR = 512
#: The Cell-ular Arena: the gallery's end and its top (the Life field's
#: terrace height), the steps down, the ground, the ring (x0, x1, top).
GALLERY = (448, 448)
ARENA_STEPS = ((448, 512, 512), (512, 576, 576), (576, 640, 640), (640, 704, 704))
ARENA_GROUND = 768
RING = (832, 1856, 720)


def blurb(rid, x):
    """The room's blurb (`blurbs.py`): two lines under its title."""
    out = []
    for n, text in enumerate(BLURB[rid]):
        w = len(text) * 9 + 24
        out.append(entity("DebugLabel", x - w // 2, 64 + n * 24, w, 24, name=f"{rid}_blurb_{n}", text=text, category="Room"))
    return out


def chest(name, reward, x, floor):
    return entity("ChestSpawn", x, floor - 58, 76, 58, name=name, reward=reward)


def flier(rid, character, n, x, y, w=48, h=40):
    """A thing that flies, where it waits in the air when the room opens."""
    return entity("EnemySpawn", x - w // 2, y - h // 2, w, h, name=f"{rid}_{character}_{n}", brain="combatant",
                  character_id=character, respawn="OnRoomReenter")


def glider_lift(rid, n, low, high):
    """A glider lift: its path (two points, the platform's centre) and the
    platform that follows it, drawn as a glider (`automaton_glider_lift`)."""
    path_id = f"{rid}_glider_path_{n}"
    (x0, y0), (x1, y1) = low, high
    w, h = LIFT_SIZE
    return [
        entity("KinematicPath", min(x0, x1), min(y0, y1), max(16, abs(x1 - x0)), max(16, abs(y1 - y0)), name=f"glider path {n}",
               id=path_id, points=f"{x0},{y0};{x1},{y1}", speed=LIFT_SPEED, mode="PingPong"),
        entity("MovingPlatform", x0 - w // 2, y0 - h // 2, w, h, id=f"{rid}_glider_{n}", name=f"glider {n}", path_id=path_id,
               one_way=True, visual="automaton_glider_lift"),
    ]


def build(rid, e, title, biome, dangerous=False, music=MUSIC, extra=""):
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e + blurb(rid, size[0] // 2), at=at, size=size, biome=biome, music=music, bg=BG, title=title,
                generator=GENERATOR, dangerous=dangerous, extra=extra)
    return rid, text


def works():
    rid = WORKS
    w, h = ROOMS_AT[rid][1]
    e = [
        solid("ground", 0, FLOOR, w, h - FLOOR),
        solid("west_wall", 0, 0, WALL, FLOOR),
        solid("east_wall", w - WALL, 0, WALL, FLOOR - 96),
        edge("works_to_life", "east, to the Life field", w - WALL, FLOOR, LIFE, "life_to_works"),
        # The gate (CELLS) and its terminal.
        *gates.as_ron(gates.ring("Works Gate", "automaton_works_gate", 96, FLOOR, "the gate")),
        *gates.as_ron(gates.terminal("Works Gate", "automaton_gate_terminal", 400, FLOOR)),
        start(rid, 520, FLOOR),
        sign("works_sign_gate", 300, FLOOR - 360, "CELLS: THE WORKS", 240),
        # The Escapement Cafe.
        sign("works_sign_cafe", 790, 176, "THE ESCAPEMENT CAFE", 300),
        # Busy Beaver and his stair of blocks.
        resident("npc_busy_beaver", "automaton_busy_beaver", 1500, FLOOR, w=48, h=72),
        *[ledge(f"block_step_{n}", x0, top, STAIR_END - x0) for n, (x0, top) in enumerate(STAIRS)],
        sign("works_sign_blocks", 1720, 236, "UNDER CONSTRUCTION SINCE STEP 1", 340),
        chest("the top block", "currency:40", 1790, STAIRS[-1][1]),
        # The clock tower; its door is the Tape Room's.
        door("works_tape_door", "into the Tape Room", TOWER_DOOR_X, FLOOR, TAPE, "tape_door"),
        sign("works_sign_tape", 2100, 500, "THE TAPE ROOM", 200),
    ]
    return build(rid, e, "THE WORKS", "automaton")


def life():
    rid = LIFE
    w, h = ROOMS_AT[rid][1]
    p0, p1, ptop = PILLAR
    t0, ttop = TERRACE
    e = [
        # The west terrace at the Works' floor, and the steps down.
        solid("west_terrace", 0, FLOOR, WEST_TERRACE_END, h - FLOOR),
        solid("west_wall", 0, 0, WALL, FLOOR - 96),
        edge("life_to_works", "west, to the Works", 0, FLOOR, WORKS, "works_to_life"),
        start(rid, 120, FLOOR),
        *[solid(f"step_{n}", x0, top, x1 - x0, h - top) for n, (x0, x1, top) in enumerate(STEPS)],
        solid("field_floor", STEPS[-1][1], FIELD_FLOOR, t0 - STEPS[-1][1], h - FIELD_FLOOR),
        # Neighbour Moore and the block.
        resident("npc_automaton_neighbour_moore", "automaton_moore", 1100, FIELD_FLOOR, w=32, h=64),
        sign("life_sign_block", 1236, 716, "THE BLOCK: A STILL LIFE", 280),
        # The glider lifts and the pillar between them.
        *glider_lift(rid, 0, *LIFTS[0]),
        solid("pillar", p0, ptop, p1 - p0, h - ptop),
        *glider_lift(rid, 1, *LIFTS[1]),
        sign("life_sign_glider", 1040, 470, "GLIDERS: ONE CELL EACH WAY EVERY FOUR GENERATIONS", 480),
        # The east terrace, the panel and the chest.
        solid("east_terrace", t0, ttop, w - t0, h - ttop),
        solid("east_wall", w - WALL, 0, WALL, ttop - 96),
        edge("life_to_arena", "east, to the Cell-ular Arena", w - WALL, ttop, ARENA, "arena_to_life"),
        sign("life_sign_panel", 2220, 56, "RULE 90, FROM ONE LIVE CELL", 300),
        chest("a fixed point", "currency:50", 2290, ttop),
        # Spaceships.
        flier(rid, "life_spaceship", 0, 1000, 640),
        flier(rid, "life_spaceship", 1, 1700, 720),
        flier(rid, "life_spaceship", 2, 1500, 380),
    ]
    return build(rid, e, "THE LIFE FIELD", "automaton_life", dangerous=True)


def tape_room():
    rid = TAPE
    w, h = ROOMS_AT[rid][1]
    g = ROOM_FLOOR
    e = [
        solid("floor", 0, g, w, h - g),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 32),
        door("tape_door", "out to the Works", 64, g, WORKS, "works_tape_door"),
        start(rid, 160, g),
        sign("tape_sign_tape", 800, 236, "THE TAPE", 160),
        sign("tape_sign_table", 1240, 274, "THE TABLE OF STATES: A B C D E", 360),
        sign("tape_sign_count", 560, 160, "STEPS: 47,176,870. THEN IT HALTS.", 400),
        resident("npc_automaton_head", "automaton_head", 760, g, w=48, h=40),
    ]
    return build(rid, e, "THE TAPE ROOM", "automaton_tower")


def arena():
    rid = ARENA
    w, h = ROOMS_AT[rid][1]
    gx, gtop = GALLERY
    x0, x1, top = RING
    g = ARENA_GROUND
    e = [
        # The gallery at the Life field's terrace, and the steps down.
        solid("gallery", 0, gtop, gx, h - gtop),
        solid("west_wall", 0, 0, WALL, gtop - 96),
        edge("arena_to_life", "west, to the Life field", 0, gtop, LIFE, "life_to_arena"),
        start(rid, 100, gtop),
        *[solid(f"step_{n}", a, t, b - a, h - t) for n, (a, b, t) in enumerate(ARENA_STEPS)],
        solid("ground", ARENA_STEPS[-1][1], g, w - ARENA_STEPS[-1][1], h - g),
        solid("east_wall", w - WALL, 0, WALL, g),
        # The failure log and the one who is in it most.
        sign("arena_sign_log", 260, 196, "THE FAILURE LOG", 240),
        resident("imperfect_cellular_automaton", "automaton_imperfect", 410, gtop, w=40, h=56),
        # The ring, and its host in the middle of it.
        solid("ring", x0, top, x1 - x0, g - top),
        entity("NpcSpawn", (x0 + x1) // 2 - 16, top - 48, 32, 48, character_id="perfect_cellular_automaton",
               prompt="Challenge the Perfect Cell-ular Automaton", dialogue_id="automaton_pca", brain_override="stand_still"),
        sign("arena_sign_rules", (x0 + x1) // 2, 420, "EIGHT NEIGHBOURS. ONE RULE. ONE RING. CHALLENGERS WELCOME.", 620),
    ]
    return build(rid, e, "THE CELL-ULAR ARENA", "automaton_life", extra='\n    backdrop: "automaton_arena",')


ROOMS = (works, life, tape_room, arena)


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
