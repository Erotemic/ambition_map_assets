#!/usr/bin/env python3
"""Write the rooms of the Central Hub, the Gate Authority's capital
(`docs/planning/game/central-hub-dimension.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/authority/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/authority/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Change the script, not the rooms.

The world file is `authority.ldtk`. The gate (address LEGAL, the one
address every terminal posts) stands in the Concourse. The Concourse and the Plaza join by an edge; the Manifest
Office is a room you go into, so its way in is a door:

 [ the Concourse ] ==== [ Authority Plaza ]
   (the baggage              |
    hall below)            door
                      [ the Manifest Office ]

- `authority_concourse`: the gate and terminal; the information booth and
  Ottilie; the catwalk of freight (a chest on it). A grate in the floor over
  the stairwell; under the floor, the baggage hall: the conveyor, the claw,
  the carts and Bertram at Lost Baggage.
- `authority_plaza`: the clock arcade, its steps up to the balcony and
  Gatekeeper Imre at the podium; the blossom tree on its planter (a chest on
  its bough); the notice board; the Manifest Office's door.
- `authority_manifest_office`: the take-a-number machine and the board,
  the chairs, the counter and the Registrar, the filing cabinets (a chest
  on top).

The capital is safe: nothing in it fights. The robot's numbers
(`district_kit`): a jump rises 83, a jump and a double jump 139; a step of
64 is one jump, 128 a double jump.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_authority_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))
sys.path.insert(0, str(HERE))

from district_kit import WALL, WORLDS, door, edge, ensure_world, entity, ledge, make_rooms, resident, room, run, sign, solid, start  # noqa: E402

import gates  # noqa: E402
from blurbs import BLURB  # noqa: E402
from props import scenery  # noqa: E402

WORLD = WORLDS / "authority.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/authority/make_specs.py"
UID_OFFSET = 1800000

CONCOURSE = "authority_concourse"
PLAZA = "authority_plaza"
OFFICE = "authority_manifest_office"

BG = "#AFC6EA"
MUSIC = "terms_and_conditions"

#: Each room: where it is on the flat map, and its size. The Concourse and
#: the Plaza are side by side, their floors at one height where they join;
#: the Manifest Office is above the Plaza.
ROOMS_AT = {
    CONCOURSE: ((0, 0), (2400, 1088)),
    PLAZA: ((2400, 0), (2400, 768)),
    OFFICE: ((3200, -800), (1600, 768)),
}

#: The Concourse (`targets/props/authority_props.py` draws to these).
FLOOR = 640
SLAB = 64
HALL_FLOOR = 1024
CATWALK = (960, 1720, 512)
STAIR_GAP = (1800, 2140)
STEPS = ((2040, 2140, 768), (1940, 2040, 832), (1840, 1940, 896), (1740, 1840, 960))
LIFT_SHAFT = (1120, 1280)
CONVEYOR = (300, LIFT_SHAFT[0], 984)
#: Authority Plaza.
BALCONY = (16, 520, 448)
PLAZA_STEPS = ((520, 600, 512), (600, 680, 576))
CLOCK_WALK = (512, 1056, 448)
PLANTER = (1040, 1360, 576)
BENCHES = ((940, 1040, 604), (1360, 1460, 604))
BOUGH = (1120, 1280, 448)
GARDEN_PERCH = (1280, 1392, 512)
OFFICE_DOOR_X = 2206
#: The Manifest Office.
CHAIRS = (420, 820, 604)
SORTING_COUNTER = (896, 1232, 560)
CABINETS = ((1240, 1400, 512), (1400, 1584, 384))
FILE_TRAY = (1312, 1392, 448)


def blurb(rid, x):
    """The room's blurb (`blurbs.py`): two lines under its title."""
    out = []
    for n, text in enumerate(BLURB[rid]):
        w = len(text) * 9 + 24
        out.append(entity("DebugLabel", x - w // 2, 64 + n * 24, w, 24, name=f"{rid}_blurb_{n}", text=text, category="Room"))
    return out


def chest(name, reward, x, floor):
    return entity("ChestSpawn", x, floor - 58, 76, 58, name=name, reward=reward)


def build(rid, e, title, biome):
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e + blurb(rid, size[0] // 2), at=at, size=size, biome=biome, music=MUSIC, bg=BG, title=title,
                generator=GENERATOR)
    return rid, text


def concourse():
    rid = CONCOURSE
    w, h = ROOMS_AT[rid][1]
    g0, g1 = STAIR_GAP
    c0, c1, walk = CATWALK
    b0, b1, belt = CONVEYOR
    lift_west, lift_east = LIFT_SHAFT
    e = [
        # The Concourse's floor, open over the stairwell; the baggage hall's
        # floor under it.
        solid("floor_west", 0, FLOOR, lift_west, SLAB),
        solid("floor_middle", lift_east, FLOOR, g0 - lift_east, SLAB),
        solid("floor_east", g1, FLOOR, w - g1, SLAB),
        solid("hall_floor", 0, HALL_FLOOR, w, h - HALL_FLOOR),
        solid("west_wall", 0, 0, WALL, HALL_FLOOR),
        solid("east_wall", w - WALL, 0, WALL, FLOOR - 96),
        solid("east_wall_low", w - WALL, FLOOR + SLAB, WALL, HALL_FLOOR - FLOOR - SLAB),
        edge("concourse_to_plaza", "east, to Authority Plaza", w - WALL, FLOOR, PLAZA, "plaza_to_concourse"),
        # The gate (LEGAL) and its terminal.
        *gates.as_ron(gates.ring("Concourse Gate", "authority_concourse_gate", 96, FLOOR, "the gate")),
        *gates.as_ron(gates.terminal("Concourse Gate", "authority_gate_terminal", 400, FLOOR)),
        start(rid, 540, FLOOR),
        sign("concourse_sign_gate", 300, FLOOR - 360, "LEGAL: THE CONCOURSE", 300),
        # Information.
        resident("npc_authority_information", "authority_information", 760, FLOOR),
        sign("concourse_sign_information", 760, 380, "INFORMATION", 200),
        # The catwalk of freight.
        ledge("catwalk", c0, walk, c1 - c0),
        chest("a lost umbrella", "currency:30", 1080, walk),
        # The grate over the stairwell, and the steps down.
        ledge("stairwell_grate", g0, FLOOR, g1 - g0),
        *[ledge(f"stair_{n}", x0, top, x1 - x0) for n, (x0, x1, top) in enumerate(STEPS)],
        sign("concourse_sign_baggage", (g0 + g1) // 2, FLOOR - 60, "BAGGAGE BELOW", 200),
        # The baggage hall.
        ledge("conveyor", b0, belt, b1 - b0),
        ledge("baggage_lift_grate", lift_west, FLOOR, lift_east - lift_west),
        entity("MovingPlatform", lift_west + 4, belt, lift_east - lift_west - 8, 16,
               id="authority_concourse_baggage_lift", name="the baggage lift",
               speed=105.0, lift_dy=float(FLOOR - belt), one_way=True, visual="authority_baggage_lift"),
        sign("baggage_sign_lift", (lift_west + lift_east) // 2, 824, "BAGGAGE LIFT", 150),
        sign("baggage_sign_sentience", 750, 744, "ORGANIC TRAVELLERS' BAGS: PLEASE DECLARE ANY SENTIENCE", 540),
        sign("baggage_sign_lost", 1440, 744, "LOST BAGGAGE", 200),
        resident("npc_authority_baggage", "authority_baggage", 1440, HALL_FLOOR),
        chest("a bag that is not yours", "currency:35", 1620, HALL_FLOOR),
    ]
    return build(rid, e, "THE CONCOURSE", "authority_hall")


def plaza():
    rid = PLAZA
    w, h = ROOMS_AT[rid][1]
    b0, b1, balcony = BALCONY
    p0, p1, ptop = PLANTER
    o0, o1, bough = BOUGH
    w0, w1, walk_top = CLOCK_WALK
    g0, g1, perch_top = GARDEN_PERCH
    e = [
        solid("floor", 0, FLOOR, w, h - FLOOR),
        solid("west_wall", 0, 0, WALL, FLOOR - 96),
        solid("east_wall", w - WALL, 0, WALL, FLOOR),
        edge("plaza_to_concourse", "west, to the Concourse", 0, FLOOR, CONCOURSE, "concourse_to_plaza"),
        start(rid, 120, FLOOR),
        # The street passes under the clock stairs and the raised walk.
        *[ledge(f"arcade_step_{n}", x0, top, x1 - x0) for n, (x0, x1, top) in enumerate(PLAZA_STEPS)],
        ledge("arcade_balcony", b0, balcony, b1 - b0),
        ledge("clock_walk", w0, walk_top, w1 - w0),
        resident("npc_authority_gatekeeper", "authority_gatekeeper", 330, balcony),
        sign("plaza_sign_authority", 268, 100, "THE GATE AUTHORITY", 320),
        # The blossom tree: its planter, the benches, and a step to the bough.
        solid("planter", p0, ptop, p1 - p0, FLOOR - ptop),
        *[ledge(f"bench_{n}", x0, top, x1 - x0) for n, (x0, x1, top) in enumerate(BENCHES)],
        ledge("garden_perch", g0, perch_top, g1 - g0),
        ledge("blossom_bough", o0, bough, o1 - o0),
        chest("a pressed blossom", "currency:30", 1162, bough),
        # The notice board.
        sign("plaza_notice_kevin", 1820, 472, "LOST: ONE DIMENSION. ANSWERS TO KEVIN.", 340),
        sign("plaza_notice_gates", 1820, 512, "UNLICENSED GATES ARE NOT GATES.", 340),
        sign("plaza_notice_legal", 1820, 552, "THE ONLY ADDRESS YOU NEED IS LEGAL.", 340),
        # The Manifest Office's door.
        door("plaza_office_door", "into the Manifest Office", OFFICE_DOOR_X, FLOOR, OFFICE, "office_door"),
        sign("plaza_sign_office", 2230, 316, "THE MANIFEST OFFICE", 240),
    ]
    return build(rid, e, "AUTHORITY PLAZA", "authority")


def manifest_office():
    rid = OFFICE
    w, h = ROOMS_AT[rid][1]
    a0, a1, seat = CHAIRS
    c0, c1, counter_top = SORTING_COUNTER
    t0, t1, tray_top = FILE_TRAY
    e = [
        solid("floor", 0, FLOOR, w, h - FLOOR),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, FLOOR - 32),
        solid("east_wall", w - WALL, 32, WALL, FLOOR - 32),
        door("office_door", "out to Authority Plaza", 64, FLOOR, PLAZA, "plaza_office_door"),
        start(rid, 150, FLOOR),
        sign("office_sign_ticket", 260, 448, "TAKE A NUMBER", 200),
        sign("office_sign_serving", 650, 238, "NOW SERVING: 4,096", 240),
        ledge("chairs", a0, seat, a1 - a0),
        ledge("sorting_counter", c0, counter_top, c1 - c0),
        resident("npc_authority_registrar", "authority_registrar", 1060, FLOOR),
        sign("office_sign_corrected", 1160, 420, "CORRECTED", 160),
        *[solid(f"cabinet_{n}", x0, top, x1 - x0, FLOOR - top) for n, (x0, x1, top) in enumerate(CABINETS)],
        ledge("extended_file_tray", t0, tray_top, t1 - t0),
        chest("a corrected record", "currency:40", 1450, CABINETS[1][2]),
    ]
    return build(rid, e, "THE MANIFEST OFFICE", "authority_hall")


ROOMS = (concourse, plaza, manifest_office)


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
    if code := make_rooms(WORLD, paths, keep_position="--relayout" not in argv):
        return code
    code, _ = run("validate", str(WORLD))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
