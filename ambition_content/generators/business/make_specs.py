#!/usr/bin/env python3
"""Write the rooms of the Business dimension: Capital, the city where
everyone is doing business (`docs/planning/game/business-dimension.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/business/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/business/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Change the script, not the rooms.

The world file is `business.ldtk`. The gate (address DEALINGS) stands at the
west end of Founders' Plaza. The plaza and Records & Processing are one
connected place, so they join by an edge; the Business College is a
building, so its way in is a door:

               door
    [the Business College]
              |
    [ Founders' Plaza ] ==== [ Records & Processing ]

- `business_founders_plaza` has the gate, terminal, and The Bottom Line café.
  Two routes lead to the café balcony, one from the delivery bench and one
  from the Founder's fountain. The plaza also has the Founder's statue, the
  records clerks' picket line, and the Business College entrance.
- `business_records_processing`: two storeys of the city's paperwork. On the
  floor, a conveyor carries forms under the APPROVED press, and the shredder
  is a pit in the floor. Catwalks climb the east side to a folder carrier
  that runs across to the west, up to the senior clerk's desk and the top of
  the archive.
- `business_college_lecture_hall`: Lecture Hall 101. Professor Gail Margin
  at her lectern on the stage; tiers of desks up to the back row, where
  Zorlack 65536 sits.

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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_business_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))
sys.path.insert(0, str(HERE))

from district_kit import WALL, WORLDS, door, edge, ensure_world, entity, ledge, make_rooms, resident, room, run, sign, solid, start  # noqa: E402

import gates  # noqa: E402
from blurbs import BLURB  # noqa: E402
from props import scenery  # noqa: E402

WORLD = WORLDS / "business.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/business/make_specs.py"
UID_OFFSET = 1600000

PLAZA = "business_founders_plaza"
RECORDS = "business_records_processing"
COLLEGE = "business_college_lecture_hall"

BG = "#2A2438"
MUSIC = "series_a_bloodbath"

#: Each room: where it is on the flat map, and its size. The plaza and
#: Records are side by side, their floors at one height where they join;
#: the college is above the plaza.
ROOMS_AT = {
    PLAZA: ((0, 0), (2560, 768)),
    RECORDS: ((2560, -320), (2560, 1088)),
    COLLEGE: ((1504, -1008), (1600, 640)),
}

#: Founders' Plaza (`targets/props/business_props.py` draws to these).
PLAZA_FLOOR = 640
AWNING = 512
BALCONY = 384
RIM = 592
PEDESTAL = 528
COLLEGE_DOOR_X = 2280
#: Records & Processing.
RECORDS_FLOOR = 960
PIT = (1280, 1440)
#: The lecture hall.
HALL_FLOOR = 576
STAGE = 544
TIERS = ((720, 880, 512), (880, 1040, 480), (1040, 1200, 432), (1200, 1584, 384))


def side_walls(w, h, west, east):
    """The side walls of a room, over the floor where each side's edge
    stands (`None`: a whole wall, no edge on that side)."""
    out = []
    for side, x, floor in (("west", 0, west), ("east", w - WALL, east)):
        out.append(solid(f"{side}_wall", x, 0, WALL, (floor - 96) if floor is not None else h))
    return out


def blurb(rid, x):
    """The room's blurb (`blurbs.py`): two lines under its title."""
    out = []
    for n, text in enumerate(BLURB[rid]):
        w = len(text) * 9 + 24
        out.append(entity("DebugLabel", x - w // 2, 64 + n * 24, w, 24, name=f"{rid}_blurb_{n}", text=text, category="Room"))
    return out


def chest(name, reward, x, floor):
    return entity("ChestSpawn", x, floor - 58, 76, 58, name=name, reward=reward)


def build(rid, e, title, biome="business", extra=""):
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e + blurb(rid, size[0] // 2), at=at, size=size, biome=biome, music=MUSIC, bg=BG, title=title,
                generator=GENERATOR, extra=extra)
    return rid, text


def founders_plaza():
    rid = PLAZA
    w, h = ROOMS_AT[rid][1]
    floor = PLAZA_FLOOR
    e = [
        solid("paving", 0, floor, w, h - floor),
        *side_walls(w, h, None, floor),
        # The gate (DEALINGS) and its terminal: the way in and the way home.
        *gates.as_ron(gates.ring("Founders' Plaza Gate", "business_plaza_gate", 96, floor, "the gate")),
        *gates.as_ron(gates.terminal("Founders' Plaza Gate", "business_gate_terminal", 400, floor)),
        start(rid, 540, floor),
        sign("plaza_sign_gate", 300, floor - 360, "DEALINGS: FOUNDERS' PLAZA, CAPITAL", 400),
        sign("plaza_sign_licence", 340, floor - 330, "DIRECTIONS IN CAPITAL ARE LICENSED. THIS SIGN HAS BILLED YOU.", 620),
        # The delivery bench and the fountain give access to the balcony.
        ledge("cafe_delivery_bench", 544, 576, 80),
        ledge("cafe_awning", 640, AWNING, 368),
        ledge("cafe_window_ledge", 864, 448, 144),
        ledge("cafe_balcony", 960, BALCONY, 224),
        ledge("cafe_service_upper", 1152, 464, 80),
        ledge("cafe_service_lower", 1168, 528, 80),
        sign("plaza_sign_cafe", 820, 468, "THE BOTTOM LINE  -  COFFEE, LICENSED CUPS", 420),
        chest("an unclaimed dividend", "currency:25", 1090, BALCONY),
        resident("npc_business_barista", "business_barista", 900, floor),
        resident("npc_quison", "quison", 1060, floor, h=66),
        # Dirk on his call, by the fountain.
        resident("npc_business_dirk_quarterly", "business_dirk", 1220, floor),
        # The Founder's fountain: its rim a step, his pedestal a step over it.
        solid("fountain_rim", 1280, RIM, 320, floor - RIM),
        solid("founder_pedestal", 1384, PEDESTAL, 112, RIM - PEDESTAL),
        sign("plaza_sign_founder", 1440, 250, "THE FOUNDER. SELF-MADE.*", 300),
        sign("plaza_sign_small_print", 1440, 276, "*FROM A SMALL LOAN OF ONE MILLION", 340),
        # The picket line of Local 17.
        resident("npc_business_solly_darity", "business_solly", 1860, floor),
        sign("plaza_sign_picket", 1860, floor - 196, "LOCAL 17 ON STRIKE", 240),
        sign("plaza_sign_picket_2", 1860, floor - 172, "PAID BY THE FORM. THE FORM GOT LONGER.", 420),
        # The Business College: a building, so a door.
        sign("plaza_sign_college", 2304, 112, "CAPITAL BUSINESS COLLEGE", 300),
        door("plaza_college_door", "into the Business College", COLLEGE_DOOR_X, floor, COLLEGE, "college_door"),
        edge("plaza_to_records", "to Records & Processing", w - WALL, floor, RECORDS, "records_from_plaza"),
    ]
    return build(rid, e, "FOUNDERS' PLAZA")


def records_processing():
    rid = RECORDS
    w, h = ROOMS_AT[rid][1]
    floor = RECORDS_FLOOR
    p0, p1 = PIT
    e = [
        solid("floor_west", 0, floor, p0, h - floor),
        solid("floor_east", p1, floor, w - p1, h - floor),
        # The shredder's cutters at the foot of its pit.
        entity("HazardBlock", p0, h - 16, p1 - p0, 16, name="the shredder"),
        solid("ceiling", 0, 0, w, 32),
        *side_walls(w, h, floor, None),
        edge("records_from_plaza", "to Founders' Plaza", 0, floor, PLAZA, "plaza_to_records"),
        start(rid, 120, floor),
        # What the floor is waiting on, on the west wall.
        sign("records_board_title", 300, 560, "TODAY", 160),
        sign("records_board_1", 300, 588, "PENDING 14,382", 200),
        sign("records_board_2", 300, 612, "IN REVIEW 6,701", 200),
        sign("records_board_3", 300, 636, "ESCALATED 327", 200),
        sign("records_board_4", 300, 660, "OVERDUE 5,988", 200),
        sign("records_sign_press", 712, 574, "APPROVED", 160),
        # The collector works the west floor, with space for his bite rush.
        entity("EnemySpawn", 876, floor - 84, 48, 84,
               name="business_records_loan_shark_0", brain="combatant",
               character_id="loan_shark", respawn="OnRoomReenter"),
        # The hedge patrols the separate east floor, beyond the shredder.
        entity("EnemySpawn", 1871, floor - 76, 78, 76,
               name="business_records_hedge_fund_0", brain="combatant",
               character_id="hedge_fund", respawn="OnRoomReenter"),
        sign("records_sign_shredder", 1360, 760, "SHREDDING. NO RETURNS.", 280),
        # The service steps lead to the carrier dock.
        ledge("catwalk_service_step", 1488, floor - 64, 128),
        ledge("catwalk_low", 1600, floor - 128, 360),
        ledge("catwalk_service_landing", 1936, floor - 192, 224),
        ledge("catwalk_east", 2140, floor - 256, w - WALL - 2140),
        ledge("catwalk_carrier_dock", 2112, floor - 320, 144),
        entity("MovingPlatform", 1520, floor - 384, 160, 16, id="business_records_folder_carrier", name="the folder carrier",
               speed=80.0, sweep_dx=440.0, one_way=True, visual="business_folder_carrier"),
        ledge("catwalk_mid", 1040, floor - 384, 460),
        entity("EnemySpawn", 1260, floor - 384 - 82, 60, 82,
               name="business_records_moving_goalposts_0", brain="combatant",
               character_id="moving_goalposts", respawn="OnRoomReenter"),
        ledge("catwalk_intake_shelf", 880, floor - 448, 176),
        ledge("catwalk_desk", 400, floor - 512, 500),
        ledge("archive_step", 336, floor - 576, 128),
        ledge("archive_top", WALL, floor - 640, 344),
        resident("npc_business_records_clerk", "business_clerk", 520, floor - 512),
        sign("records_sign_desk", 660, floor - 600, "SENIOR CLERK. TAKE A NUMBER.", 320),
        chest("a misfiled bonus", "currency:40", 120, floor - 640),
    ]
    return build(rid, e, "RECORDS & PROCESSING", biome="business_office")


def college_lecture_hall():
    rid = COLLEGE
    w, h = ROOMS_AT[rid][1]
    floor = HALL_FLOOR
    back_row = TIERS[-1][2]
    ladder_top = back_row - 16
    ladder = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [1520, {ladder_top}], size: [32, {floor - ladder_top}]),
    ]),"""
    e = [
        solid("floor", 0, floor, w, h - floor),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        solid("east_wall", w - WALL, 32, WALL, floor - 32),
        door("college_door", "out to Founders' Plaza", 64, floor, PLAZA, "plaza_college_door"),
        start(rid, 150, floor),
        # The lecturer's stage and the tiers of desks, each one jump up.
        solid("stage", 176, STAGE, 400, floor - STAGE),
        *[ledge(f"tier_{n}", x0, top, x1 - x0) for n, (x0, x1, top) in enumerate(TIERS)],
        resident("npc_business_professor", "business_professor", 370, STAGE),
        # Zorlack 65536 in the back row.
        resident("npc_ninja_shadow_oni_leader", "business_zorlack", 1420, back_row, h=72),
        sign("hall_sign_board", 460, 342, "SYNERGY: 1 + 1 = 3  (RESULTS NOT TYPICAL)", 440),
        sign("hall_sign_careers", 1112, 320, "CAREERS FAIR FRIDAY. DRESS CODE: BRING YOUR WHOLE SELF (IN A NAVY SUIT).", 680),
    ]
    return build(rid, e, "CAPITAL BUSINESS COLLEGE: LECTURE HALL 101", biome="business_office", extra=ladder)


ROOMS = (founders_plaza, records_processing, college_lecture_hall)


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
