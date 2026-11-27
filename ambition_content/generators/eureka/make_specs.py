#!/usr/bin/env python3
"""Write the rooms of Eureka, the science dimension's institute town, and the
space elevator from it up to the orbital station.

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/eureka/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/eureka/make_specs.py --apply  # and makes the rooms

Run it from the repository root.

Jon (2026-10-29): the science dimension's first build is an inhabited town
("we are world building not quest building": no quest), and "the science
dimension should have a space elevator that brings you up to the orbital
station". Eureka is on the planet under the station, in the dimension's own
world file (`science.ldtk`): the station and GNU-ton's gravity works are
overhead, and the tether joins them by real geography. Gate address SCIENCE
arrives in its gate court.

- `eureka_gate_court`: the gate court. Travellers arrive at the ring (the
  gate network's `gate_interface.yaml` places it on the clear floor at the
  west end).
- `eureka_quad`: the campus street, with the lecture hall's terrace over it.
  Doors to the patent office, the coil laboratory and the observatory.
- `eureka_patent_office`: the Patent Clerk's office.
- `eureka_coil_lab`: Tesseract Laboratories, Nikobolt Tesseract's coil hall.
- `eureka_observatory`: Carl Stargan's dome; ledges up to the telescope.
- `eureka_qed_studios`: QED-TV, the station on the lecture hall's terrace:
  the reception, the studio where Will Force, the Science Horse, reads the
  evening news (the anchor desk, the cameras, the lighting grid up its
  ladder, the demonstration bench) and the production room.
- `eureka_elevator_station`: the tether's ground station. Its car rests in the
  floor at the foot of the shaft; stand on it and it carries you up through
  the roof.
- `eureka_elevator_climb`: the climb, a tall room of sky. You arrive on the
  second car (a body that comes up through a floor edge stands 69 px over
  it, `rooms::spawn::edge_arrival`), and it carries you out of the top.
- `orbital_station_tether_terminus`: the station end, east of the docking
  bay: you arrive standing on its floor, and the bay is on through its west
  end. The tether only goes up: the way home from the station is its gate
  (Jon, 2026-11-09: the chute back to the surface goes).

The elevator is the engine's lift (`MovingPlatform` with `lift_dy`): it waits
for a rider, carries it, and goes back down to rest. Jump off on the climb and
you fall back to the ground station.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_eureka_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))

from district_kit import (  # noqa: E402
    WALL, WORLDS, breakable_wall, door, edge, entity, ledge, make_rooms, paint, resident, room, run, sign, solid,
    start,
)

import props  # noqa: E402  (this directory's scenery)

WORLD_LDTK = WORLDS / "science.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/eureka/make_specs.py"

COURT = "eureka_gate_court"
#: Under the lecture hall, down the stair in one of its arches.
COLLIDER = "eureka_collider"
COLLIDER_DOOR_X = 1828
#: The detector's gallery (x0, x1, y), up a ladder (`eureka_collider_props.py`).
COLLIDER_GALLERY = (1488, 1760, 384)
COLLIDER_WALKS = ((448, 560, 512), (576, 688, 448), (704, 1408, 384))
QUAD = "eureka_quad"
QUAD_WALKS = ((576, 960, 576), (1008, 1200, 576), (1232, 1408, 592), (1456, 1600, 576))
PATENT = "eureka_patent_office"
LAB = "eureka_coil_lab"
DOME = "eureka_observatory"
QED = "eureka_qed_studios"
STATION = "eureka_elevator_station"
CLIMB = "eureka_elevator_climb"
TERMINUS = "orbital_station_tether_terminus"
BAY = "orbital_station_docking_bay"
RANGE = "eureka_test_range"
#: Under the quad, down the manhole in its street (quad x, a hole in the
#: street over the plant's shaft): the steam plant; east of it on its floor,
#: the Collider. Behind a bricked door at its west end (a breakable wall),
#: the institute's first lab.
PLANT = "eureka_steam_plant"
FIRST_LAB = "eureka_first_lab"
MANHOLE = (880, 944)
PLANT_FLOOR = 928
#: The plant's walks (x0, x1, y): the upper catwalk, the step, the lower
#: catwalk, the boilers' tops (`eureka_plant_props.py` draws on these).
PLANT_WALKS = ((16, 1500, 400), (1540, 1700, 528), (900, 2240, 656), (1080, 1280, 800), (1760, 1960, 800))
PLANT_RETURN_STEPS = ((1440, 1536, 464), (1728, 1824, 592))
PLANT_EAST_LADDER_X = 2112

#: The contract with the gate network: the arrival point a dialled SCIENCE
#: names (its ring is `gate_interface.yaml`, written by
#: `gate_network/make_gates.py`).
ARRIVAL = "eureka_gate_arrival"
#: The docking bay's side on to the terminus (the bay is `orbital_station`'s
#: room; its generator has the same zone).
BAY_EAST = "bay_east"
#: How high the terminus's west end is open on to the bay.
BAY_OPENING = 128

BIOME = "eureka"
HEIGHTS = "eureka_heights"
STATION_THEME = "orbital"
BG = "#A9D3F0"
TOWN_MUSIC = "a_possible_morning"
PATENT_MUSIC = "graphite_and_rain"
LAB_MUSIC = "scaling_laws"
DOME_MUSIC = "billions_and_billions"
TETHER_MUSIC = "salt_steel_and_starlight"
STATION_MUSIC = "between_objectives"

#: Each room: (world_x, world_y), (width, height). The town is on the ground
#: (y 6880), under the station's rooms (y 3168 and up): the climb and the
#: terminus stand over the ground station's shaft.
#: The world rooms touch where their side and vertical exits join, with their
#: walk lines level (Jon, 2026-10-30: side exits connect the world, doors
#: enter buildings, "a mostly faithful flat map"; `specs/check_flat_map.py`):
#: the court's floor (world y 7584) is the quad's street and the ground
#: station's floor; the climb stands on the station's roof over its shaft,
#: and the terminus on the climb, against the east end of the station's
#: docking bay (x 5056). The buildings (the patent office, the lab,
#: the dome) are entered by doors and sit near their doors.
ROOMS_AT = {
    COURT: ((256, 6880), (1600, 832)),
    # Out of town (Jon, 2026-10-30): the Test Range, west of the gate court.
    RANGE: ((256 - 2816, 6880), (2816, 832)),
    QUAD: ((1856, 6816), (2816, 896)),
    # Buildings: under the steam plant, out of its way.
    PATENT: ((1856, 9024), (1024, 640)),
    LAB: ((3072, 9024), (1280, 576)),
    # Under the quad, its floor the Collider's (world y 8640).
    PLANT: ((2016, 7712), (2400, 992)),
    FIRST_LAB: ((2016 - 640, 8640 - 512), (640, 576)),
    COLLIDER: ((4416, 8064), (2000, 640)),
    # Under the Collider, out of its way.
    QED: ((4480, 9024), (2240, 704)),
    DOME: ((2560, 5792), (1280, 1024)),
    STATION: ((4672, 6240), (1600, 1408)),
    CLIMB: ((5056, 3040), (1280, 3200)),
    TERMINUS: ((5056, 2016), (1280, 1024)),
}

#: The elevator: the cars' size and speed; the foot of the ground station's
#: shaft (room x), and the climb's and terminus's shaft (room x).
CAR_W, CAR_H = 128, 22
#: How far over the ground station's floor its car waits: a hop.
CAR_HOP = 40
CAR_SPEED = 300.0
CLIMB_SPEED = 340.0
STATION_SHAFT_X = 960
STATION_GALLERIES = ((16, 904, 1024), (1144, 1584, 1024))
STATION_STEPS = ((464, 576, 1280), (416, 528, 1216), (352, 464, 1152), (288, 400, 1088),
                 (1120, 1232, 1280), (1184, 1296, 1216), (1248, 1360, 1152), (1312, 1424, 1088))
SHAFT_X = 576
#: A body that comes up through a floor edge stands this far over it.
EDGE_FEET = 68


def build(rid, entities, title, music=TOWN_MUSIC, biome=BIOME, **kw):
    at, size = ROOMS_AT[rid]
    # The room's scenery (`props.py`) is listed first: it draws behind.
    entities = [*props.scenery(rid), *entities]
    return rid, room(rid, entities, at=at, size=size, biome=biome, music=music, bg=BG, title=title, generator=GENERATOR, **kw)


def vertical_edge(zone, name, x, y, w, to_room, to_zone, bidirectional=True):
    """An edge exit across the top or the bottom of a room."""
    return entity("LoadingZone", x, y, w, 16, id=zone, name=name, activation="EdgeExit", target_room=to_room,
                  target_zone=to_zone, bidirectional=bidirectional)


def car(cid, name, x, top, dy, speed):
    """A car of the elevator: it rests with its top at `top` and carries a
    rider `dy` (up is negative). Drawn as `eureka_tether_car` (its floor is
    the platform: `platform_looks.ron`)."""
    return entity("MovingPlatform", x, top, CAR_W, CAR_H, id=cid, name=name, speed=speed, lift_dy=float(dy), one_way=True,
                  visual="eureka_tether_car")


def walk(name, x, y, w):
    """A one-way walk the room's art draws (a gallery on its girder): a still
    platform with no picture of its own."""
    return entity("MovingPlatform", x, y, w, 16, id=name, name=name, speed=0.0, visual="none", one_way=True)


def court():
    """The gate court. Floor 704. The ring stands on the clear floor of the
    west end (x 112..512); a plinth and a bench by it, the institute's sign,
    and the way east to the quad on the floor and along a raised walk."""
    rid = COURT
    _, (w, h) = ROOMS_AT[rid]
    floor, walk = 704, 512
    e = [
        solid("ground", 0, floor, w, h - floor),
        # The west wall, open on the floor to the Test Range.
        solid("west_wall", 0, 0, WALL, floor - 112),
        edge("court_west", "out to the Test Range", 0, floor, RANGE, "range_east"),
        solid("east_wall_high", w - WALL, 0, WALL, walk - 96),
        solid("east_wall_mid", w - WALL, walk + 16, WALL, floor - 96 - walk - 16),
        start(rid, 336, floor),
        ledge("founders_plinth", 640, floor - 64, 128),
        ledge("court_bench", 860, floor - 32, 160),
        sign("court_sign_gate", 336, floor - 300, "SCIENCE: arrivals for the Eureka Institute", 420),
        sign("court_sign_tether", 900, floor - 260, "The tether: ground station east of the quad. Cars on demand.", 520),
        # Ottoline Hum busks in the arcade's middle arch (`eureka.yarn`).
        resident("npc_eureka_hum", "eureka_hum", 1444, floor),
        # Steps up to the raised walk that runs on east over the quad.
        ledge("walk_step_1", 1080, floor - 64, 96),
        ledge("walk_step_2", 1160, floor - 128, 96),
        ledge("raised_walk", 1232, walk, w - 1232),
        edge("court_east_low", "to the quad", w - WALL, floor, QUAD, "quad_west_low"),
        edge("court_east_high", "along the raised walk", w - WALL, walk, QUAD, "quad_west_high"),
    ]
    return build(rid, e, "EUREKA: THE GATE COURT")


def quad():
    """The street connects the offices and the tether station.

    The raised walk passes the patent office, cafe, and fountain. It
    connects the Gate Court to the lecture hall terrace.
    """
    rid = QUAD
    _, (w, h) = ROOMS_AT[rid]
    # The raised walk is as high over the street as the court's is over its
    # floor, so the two meet level.
    street, terrace, walk_y = 768, 576, 576
    m0, m1 = MANHOLE
    e = [
        solid("street_west", 0, street, m0, h - street),
        solid("street_east", m1, street, w - m1, h - street),
        # The manhole down to the steam plant: an open hole with a one-way
        # floor over it (dropped through) and a ladder (`main`).
        ledge("manhole_hatch", m0, street, m1 - m0),
        vertical_edge("quad_manhole", "down the manhole to the steam plant", m0, h - 16, m1 - m0, PLANT, "plant_manhole"),
        sign("manhole_sign", 920, 612, "STEAM PLANT", 144),
        sign("manhole_sign_note", 920, 638, "Staff and the curious", 144),
        solid("west_wall_high", 0, 0, WALL, walk_y - 96),
        solid("west_wall_mid", 0, walk_y + 16, WALL, street - 96 - walk_y - 16),
        solid("east_wall", w - WALL, 0, WALL, street - 96),
        edge("quad_west_low", "to the gate court", 0, street, COURT, "court_east_low"),
        edge("quad_west_high", "along the raised walk", 0, walk_y, COURT, "court_east_high"),
        start(rid, 120, street),
        # The quad's art draws over these (`targets/props/eureka_quad_props.py`);
        # they stay ledges, the ground a navigating body knows.
        ledge("raised_walk", WALL, walk_y, 560),
        ledge("walk_stair_1", 560, street - 64, 96),
        ledge("walk_stair_2", 600, street - 128, 64),
        *[ledge(f"quad_walk_{i}", left, top, right - left)
          for i, (left, right, top) in enumerate(QUAD_WALKS)],
        door("quad_patent_door", "into the patent office", 760, street, PATENT, "patent_door"),
        sign("patent_sign", 757, 598, "PATENT OFFICE", 150),
        sign("patent_sign_class", 757, 622, "Third class", 150),
        ledge("cafe_street_bench", 960, 720, 80),
        ledge("cafe_awning", 1000, street - 112, 200),
        resident("npc_eureka_mina", "eureka_mina", 1100, street),
        sign("cafe_sign", 1104, 597, "THE UNCERTAIN CUP", 190),
        sign("cafe_sign_note", 1104, 621, "Coffee, probably.", 190),
        resident("npc_eureka_priya", "eureka_priya", 1320, street),
        # The lecture hall: its steps up to the terrace, and the observatory's door on it.
        ledge("hall_step_1", 1440, street - 64, 96),
        ledge("hall_step_2", 1520, street - 128, 96),
        ledge("hall_terrace", 1600, terrace, 720),
        # QED-TV on the terrace, west of the observatory (`eureka_qed_props.py`).
        door("quad_qed_door", "into QED-TV", QED_DOOR_X, terrace, QED, "qed_door"),
        sign("qed_sign", 1760, 200, "QED-TV: the news, straight from the horse's mouth", 360),
        resident("npc_eureka_halvorsen", "eureka_halvorsen", 1800, terrace),
        door("quad_dome_door", "up to the observatory", 2180, terrace, DOME, "dome_door"),
        sign("dome_sign", 2204, terrace - 140, "OBSERVATORY: visiting hours after dark", 340),
        sign("hall_sign", 1960, terrace + 16, "THE LECTURE HALL OF THE EUREKA INSTITUTE", 460),
        door("quad_collider_door", "down to the Collider", COLLIDER_DOOR_X, street, COLLIDER, "collider_door"),
        door("quad_lab_door", "into Tesseract Laboratories", 2440, street, LAB, "lab_door"),
        sign("lab_sign", 2464, street - 150, "TESSERACT LABORATORIES: mind the coils", 360),
        resident("npc_eureka_wilbur", "eureka_wilbur", 2620, street),
        edge("quad_east", "to the tether's ground station", w - WALL, street, STATION, "station_west"),
    ]
    return build(rid, e, "THE QUAD")


def patent_office():
    """The clerk works below the archive. Jump or climb to the gallery."""
    rid = PATENT
    _, (w, h) = ROOMS_AT[rid]
    floor, ceiling = h - 64, 32
    gallery_top = floor - 176
    gallery_left = 768
    ladder_top = gallery_top - 16
    ladder = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [{gallery_left}, {ladder_top}], size: [32, {floor - ladder_top}]),
    ]),"""
    e = [
        solid("floor", 0, floor, w, 64),
        solid("ceiling", 0, 0, w, ceiling),
        solid("west_wall", 0, ceiling, WALL, floor - ceiling),
        solid("east_wall", w - WALL, ceiling, WALL, floor - ceiling),
        door("patent_door", "out to the quad", 40, floor, QUAD, "quad_patent_door"),
        start(rid, 140, floor),
        ledge("counter", 480, floor - 48, 240),
        ledge("file_cabinets", 816, floor - 96, 176),
        ledge("archive_gallery", gallery_left, gallery_top, w - WALL - gallery_left),
        resident("special_patent_clerk", "eureka_patent_clerk", 640, floor),
        sign("patent_sign_rules", 520, ceiling + 40, "All applications are processed relative to the applicant.", 520),
    ]
    return build(rid, e, None, music=PATENT_MUSIC, extra=ladder)


def coil_lab():
    """Cross the coil hall on the floor or on the service gantries."""
    rid = LAB
    _, (w, h) = ROOMS_AT[rid]
    floor, ceiling = h - 64, 32
    e = [
        solid("floor", 0, floor, w, 64),
        solid("ceiling", 0, 0, w, ceiling),
        solid("west_wall", 0, ceiling, WALL, floor - ceiling),
        solid("east_wall", w - WALL, ceiling, WALL, floor - ceiling),
        door("lab_door", "out to the quad", 40, floor, QUAD, "quad_lab_door"),
        start(rid, 140, floor),
        ledge("crate", 192, floor - 80, 112),
        ledge("coil_gantry_west", 320, floor - 160, 240),
        ledge("coil_transfer", 576, floor - 192, 128),
        ledge("coil_gantry_east", 720, floor - 224, 240),
        ledge("coil_service_upper", 976, floor - 160, 80),
        ledge("coil_service_lower", 1088, floor - 96, 80),
        ledge("bench", 992, floor - 48, 176),
        resident("npc_eureka_dmitri", "eureka_dmitri", 560, floor),
        # Nikobolt and Coulomba are together between the two gantries, clear
        # of the door, the bench, and the gravity-prototype lever.
        # They live their authored days (`data/npc_lives.ron`): a brain that
        # goes only where a plan sends it.
        resident("npc_science_nikobolt", "eureka_nikobolt", 750, floor, brain="keeps_to_its_tasks", h=76),
        resident("npc_science_coulomba", "eureka_coulomba", 840, floor, brain="keeps_to_its_tasks", h=68),
        sign("lab_sign_rules", 640, ceiling + 40, "DO NOT TOUCH THE COILS. The coils will touch you.", 520),
        sign("lab_sign_director", 1100, floor - 240, "N. TESSERACT, DIRECTOR: AT WORK", 320),
        # The places of Nikobolt's day, by name: his plan's `go_to workbench`
        # is the floor under this sign, at the bench; lunch is at the crate.
        sign("workbench", 1072, floor - 24, "COIL No. 27", 140),
        sign("lunch", 248, floor - 24, "LUNCH. NAPKINS: 18", 200),
        # The director's prototype (Jon, 2026-10-30: "a bit of chutzpah"): a
        # lever that turns the lab's gravity over, and its twin hanging from
        # the ceiling for whoever pressed it. The only door is on the floor.
        entity("Switch", LAB_LEVER_X, floor - 32, 24, 32, id="lab_gravity_prototype", name="the prototype",
               prompt="Do not press", action="FlipGravity"),
        entity("Switch", LAB_LEVER_X, ceiling, 24, 32, id="lab_gravity_prototype_twin", name="the prototype's twin",
               prompt="Press to come down", action="FlipGravity"),
        sign("lab_sign_prototype", LAB_LEVER_X - 132, floor - 208, "ANTI-GRAVITY PROTOTYPE: DO NOT PRESS", 380),
        sign("lab_sign_told_you", LAB_LEVER_X - 60, ceiling + 70, "TOLD YOU.", 160),
    ]
    return build(rid, e, None, music=LAB_MUSIC)


#: Where the coil lab's gravity levers stand (x), one on the floor and one
#: on the ceiling.
LAB_LEVER_X = 1192


def observatory():
    """The spiral and east viewing stair meet at the telescope."""
    rid = DOME
    _, (w, h) = ROOMS_AT[rid]
    floor = h - 64
    platform = 320
    viewing_stair = ((1120, 1264, 640), (1008, 1152, 560), (928, 1072, 480), (848, 992, 400))
    ladder_top = viewing_stair[0][2] - 16
    ladder = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [1232, {ladder_top}], size: [32, {floor - ladder_top}]),
    ]),"""
    e = [
        solid("floor", 0, floor, w, 64),
        solid("dome", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        solid("east_wall", w - WALL, 32, WALL, floor - 32),
        door("dome_door", "down to the quad", 40, floor, QUAD, "quad_dome_door"),
        start(rid, 140, floor),
        # Up the wall in steps of 80 (one jump), east then back west.
        *[ledge(f"stair_{k + 1}", x, floor - 80 * (k + 1), 160) for k, x in enumerate((240, 480, 720, 960, 720, 480, 240))],
        *[ledge(f"viewing_stair_{i + 1}", x0, y, x1 - x0) for i, (x0, x1, y) in enumerate(viewing_stair)],
        ledge("telescope_platform", 320, platform, 480),
        resident("npc_carl_stargan", "eureka_stargan", 560, platform),
        sign("dome_sign_slit", 640, 72, "The station: a pale dot, directly overhead", 440),
    ]
    return build(rid, e, None, music=DOME_MUSIC, extra=ladder)


def elevator_station():
    """The floor leads to the car and the operator.

    The steps give access to the galleries beside the shaft. The car
    waits above the floor and moves up when a rider stands on it.
    """
    rid = STATION
    _, (w, h) = ROOMS_AT[rid]
    floor = h - 64
    sx, sw = STATION_SHAFT_X, CAR_W
    e = [
        solid("floor", 0, floor, w, 64),
        solid("roof_west", 0, 0, sx, 48),
        solid("roof_east", sx + sw, 0, w - sx - sw, 48),
        solid("west_wall_high", 0, 48, WALL, floor - 96 - 48),
        solid("east_wall", w - WALL, 48, WALL, floor - 48),
        edge("station_west", "to the quad", 0, floor, QUAD, "quad_east"),
        start(rid, 200, floor),
        car("tether_car_ground", "the tether's car", sx, floor - CAR_HOP, -(floor - CAR_HOP + 60), CAR_SPEED),
        vertical_edge("station_to_climb", "up the tether", sx, 0, sw, CLIMB, "climb_from_station"),
        resident("npc_eureka_teodora", "eureka_teodora", 720, floor),
        sign("station_sign", 294, 812, "EUREKA TETHER: GROUND STATION", 380),
        sign("station_sign_car", 827, 1180, "STAND ON THE CAR TO ASCEND", 232),
        sign("station_sign_altitude", 1368, 928, "ORBIT IS 35,786 KM ABOVE EUREKA", 344),
        sign("station_sign_altitude_note", 1368, 952, "Allow for the view.", 344),
        *[walk(f"gallery_{side}", left, top, right - left)
          for side, (left, right, top) in zip(("west", "east"), STATION_GALLERIES)],
        *[ledge(f"station_step_{i}", left, top, right - left)
          for i, (left, right, top) in enumerate(STATION_STEPS)],
    ]
    return build(rid, e, "THE TETHER: GROUND STATION")


#: The signs on the climb, by how far up the room they are (0 bottom, 1 top).
CLIMB_SIGNS = [
    (0.08, "12 km: the weather, now under you"),
    (0.30, "100 km: the Karman line. Space, technically"),
    (0.55, "2,000 km: low orbit, and its traffic"),
    (0.80, "20,000 km: the planet fits in the window"),
]


def elevator_climb():
    """The climb: a tall room of sky, the tether up its middle. The second car
    rests where a body coming up through the floor edge stands, and carries
    it out of the top."""
    rid = CLIMB
    _, (w, h) = ROOMS_AT[rid]
    top = h - EDGE_FEET
    e = [
        solid("west_wall", 0, 0, WALL, h),
        solid("east_wall", w - WALL, 0, WALL, h),
        vertical_edge("climb_from_station", "down to the ground station", SHAFT_X, h - 16, CAR_W, STATION, "station_to_climb"),
        car("tether_car_climb", "the tether's car", SHAFT_X, top, -(top + 60), CLIMB_SPEED),
        vertical_edge("climb_to_terminus", "up to the station", SHAFT_X, 0, CAR_W, TERMINUS, "terminus_from_climb"),
        start(rid, SHAFT_X + CAR_W // 2, top),
    ]
    for frac, text in CLIMB_SIGNS:
        e.append(sign(f"climb_sign_{int(frac * 100)}", SHAFT_X + CAR_W // 2 + 260, round(h * (1.0 - frac)), text, 440))
    return build(rid, e, None, music=TETHER_MUSIC, biome=HEIGHTS)


def terminus():
    """The station end of the tether: you come up through the floor and stand
    on it. The docking bay is on through the west end."""
    rid = TERMINUS
    _, (w, h) = ROOMS_AT[rid]
    floor = h - EDGE_FEET
    e = [
        solid("floor", 0, floor, w, h - floor),
        solid("vault", 0, 0, w, 48),
        solid("west_wall", 0, 48, WALL, floor - 48 - BAY_OPENING),
        solid("east_wall", w - WALL, 48, WALL, floor - 48),
        vertical_edge("terminus_from_climb", "down the tether", SHAFT_X, h - 16, CAR_W, CLIMB, "climb_to_terminus"),
        start(rid, SHAFT_X + CAR_W // 2, floor),
        edge("terminus_west", "to the docking bay", 0, floor, BAY, BAY_EAST, h=BAY_OPENING),
        sign("terminus_sign", w // 2, 120, "TETHER TERMINUS: the planet is 35,786 km down", 520),
        # The arrivals board and the souvenir kiosk (`orbital_terminus_props.py`).
        sign("terminus_sign_arrivals", 540, 300, "ARRIVALS: every car ON TIME. It is a ribbon.", 440),
        sign("terminus_sign_kiosk", 375, floor - 150, "GENUINE ORBIT AIR, bottled at altitude", 380),
        resident("npc_station_dobbs", "station_dobbs", 390, floor),
    ]
    return build(rid, e, "THE TETHER TERMINUS", music=STATION_MUSIC, biome=STATION_THEME)


def range_enemy(n, character, x, feet, w, h, brain="combatant"):
    return entity("EnemySpawn", x, feet - h, w, h, name=f"{RANGE}_{character}_{n}", brain=brain,
                  character_id=character, respawn="OnRoomReenter")


def test_range():
    """Out of town: the Test Range, west of the gate court. Floor 704. A
    rocket on its pad with a gantry to climb (its walks y 624..384), a blast
    shelter with a floor passage and roof steps, and an observation tower.
    What the institute tests has got loose: its own machines (dividing mites,
    a steam automaton on the bunker, exploding mites); two crash-test dummies wait to be
    hit."""
    rid = RANGE
    _, (w, h) = ROOMS_AT[rid]
    floor = 704
    bx0, bx1, btop = 1696, 1968, 576
    e = [
        solid("ground", 0, floor, w, h - floor),
        solid("west_wall", 0, 0, WALL, floor),
        solid("east_wall_high", w - WALL, 0, WALL, floor - 112),
        edge("range_east", "back to the gate court", w - WALL, floor, COURT, "court_west"),
        start(rid, w - 200, floor),
        *[ledge(f"gantry_{i}", x0, y, x1 - x0) for i, (x0, x1, y) in enumerate(((680, 820, 624), (760, 900, 544), (680, 820, 464), (760, 900, 384)))],
        solid("bunker_roof", bx0, btop, bx1 - bx0, 32),
        ledge("bunker_west_step", 1568, floor - 64, 112),
        ledge("bunker_east_step", 1984, floor - 64, 112),
        ledge("tower_low", 2280, 560, 120),
        ledge("tower_cab", 2320, 416, 120),
        # A chest for whoever climbs to the top (Jon, 2026-10-30: "interactive elements").
        entity("ChestSpawn", 2340, 416 - 58, 76, 58, name="the range's lost and found", reward="currency:50"),
        sign("range_sign", w - 420, floor - 200, "EUREKA TEST RANGE: if the siren sounds, it is already too late", 520),
        sign("rocket_sign", 960, 110, "PROBABLY FINE III", 260),
        sign("bunker_sign", (bx0 + bx1) // 2, btop - 1, "BLAST BUNKER: knock first, then duck", bx1 - bx0),
        sign("tower_sign", 2380, 300, "OBSERVATION: the safe side of the glass", 360),
        range_enemy(1, "npc_dividing_mite", 1240, floor, 32, 24, "dividing_mite"),
        range_enemy(2, "npc_dividing_mite", 2120, floor, 32, 24, "dividing_mite"),
        range_enemy(3, "steam_automaton", 1810, btop, 48, 80),
        range_enemy(4, "npc_exploding_mite", 480, floor, 38, 66, "exploding_mite"),
        range_enemy(5, "npc_exploding_mite", 1500, floor, 38, 66, "exploding_mite"),
        # A reactive molecular escapee above the western half of the range.
        range_enemy(8, "free_radical", 1020, floor - 180, 64, 46),
        # The range's officer, between the mites and the dummies.
        resident("npc_eureka_pryce", "eureka_pryce", 2500, floor),
        range_enemy(6, "sandbag", 2580, floor, 34, 58, "sandbag_finite"),
        range_enemy(7, "sandbag", 2660, floor, 34, 58, "sandbag_finite"),
    ]
    return build(rid, e, "THE TEST RANGE", music=TOWN_MUSIC, dangerous=True)


# Made from the top of the tether down and then west: a room is placed only
# where no room stands, so a move of the chain places the far end first.
def collider():
    """Follow the floor or the beam service walk to the detector gallery."""
    rid = COLLIDER
    _, (w, h) = ROOMS_AT[rid]
    floor, vault = 576, 48
    g0, g1, gy = COLLIDER_GALLERY
    ladder_top = gy - 16
    ladder = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [1456, {ladder_top}], size: [48, {floor - ladder_top}]),
    ]),"""
    e = [
        solid("floor", 0, floor, w, h - floor),
        solid("vault", 0, 0, w, vault),
        solid("west_wall", 0, vault, WALL, floor - 112 - vault),
        edge("collider_west", "west into the steam plant", 0, floor, PLANT, "plant_east"),
        solid("east_wall", w - WALL, vault, WALL, floor - vault),
        door("collider_door", "up to the quad", 40, floor, QUAD, "quad_collider_door"),
        start(rid, 140, floor),
        *[ledge(f"beam_walk_{i}", x0, y, x1 - x0) for i, (x0, x1, y) in enumerate(COLLIDER_WALKS)],
        ledge("detector_gallery", g0, gy, g1 - g0),
        entity("ChestSpawn", 1590, gy - 58, 76, 58, name="a spare quark (charm)", reward="currency:60"),
        resident("npc_eureka_quark", "eureka_quark", 300, floor),
        sign("collider_sign", 560, 200, "THE EUREKA COLLIDER: circumference 27 km. Staff bicycles only.", 520),
        sign("collider_sign_beam", 900, 272, "BEAM ON: do not lick the pipe", 300),
        range_enemy(10, "npc_dividing_mite", 760, floor, 32, 24, "dividing_mite"),
        range_enemy(11, "npc_dividing_mite", 1080, floor, 32, 24, "dividing_mite"),
        range_enemy(12, "steam_automaton", 1200, COLLIDER_WALKS[-1][2], 48, 80),
    ]
    return build(rid, e, "THE EUREKA COLLIDER", extra=ladder)


def plant():
    """Under the quad, down its manhole: the steam plant that heats the
    institute. Brick and riveted iron, the great pipes, two boilers (one
    gauge in the red, labelled FINE), catwalks up to the vault; east on its
    floor into the Collider. A bricked door at the west end, LAB 0 over it."""
    rid = PLANT
    _, (w, h) = ROOMS_AT[rid]
    g, vault = PLANT_FLOOR, 48
    x0 = ROOMS_AT[PLANT][0][0] - ROOMS_AT[QUAD][0][0]
    s0, s1 = MANHOLE[0] - x0, MANHOLE[1] - x0
    ladder_top = PLANT_WALKS[2][2] - 16
    ladders = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [{s0 + 16}, 0], size: [32, {g}]),
        (kind: "Ladder", px: [{PLANT_EAST_LADDER_X}, {ladder_top}], size: [32, {g - ladder_top}]),
    ]),"""
    e = [
        solid("floor", 0, g, w, h - g),
        solid("vault_west", 0, 0, s0, vault),
        solid("vault_east", s1, 0, w - s1, vault),
        solid("west_wall", 0, vault, WALL, g - 112 - vault),
        solid("east_wall", w - WALL, vault, WALL, g - 112 - vault),
        vertical_edge("plant_manhole", "up the manhole to the quad", s0, 0, s1 - s0, QUAD, "quad_manhole"),
        edge("plant_east", "east into the Collider", w - WALL, g, COLLIDER, "collider_west"),
        # The bricked door (a breakable: hit it; broken for good in the
        # save) over the way west (`secret_`: the map shows the first lab
        # only once it is found).
        breakable_wall("eureka_plant_bricked_door", WALL, g - 112, 32, 112, look="plant_bricked_door", hp=3,
                       name="a bricked door, LAB 0 over it"),
        edge("secret_plant_west", "through the bricked door", 0, g, FIRST_LAB, "secret_first_lab_east"),
        start(rid, s1 + 120, g),
        *[walk(f"plant_walk_{i}", a, y, b - a) for i, (a, b, y) in enumerate(PLANT_WALKS)],
        *[walk(f"plant_return_{i}", a, y, b - a) for i, (a, b, y) in enumerate(PLANT_RETURN_STEPS)],
        entity("ChestSpawn", 1300, 400 - 58, 76, 58, name="the stoker's tin", reward="currency:50"),
        sign("plant_sign", 1200, 90, "EUREKA STEAM PLANT: est. before anyone asked", 420),
        sign("plant_sign_gauge", 1860, 640, "GAUGE: FINE", 220),
        sign("plant_sign_door", 140, 760, "LAB 0", 160),
        range_enemy(20, "npc_dividing_mite", 1100, g, 32, 24, "dividing_mite"),
        range_enemy(21, "steam_automaton", 1640, g, 48, 80),
        range_enemy(22, "npc_dividing_mite", 600, 400, 32, 24, "dividing_mite"),
    ]
    return build(rid, e, "THE STEAM PLANT", extra=ladders)


def first_lab():
    """The camp bed and the workbench give access to the grant chest."""
    rid = FIRST_LAB
    _, (w, h) = ROOMS_AT[rid]
    g, vault = 512, 48
    cabinet_top = 416
    e = [
        solid("floor", 0, g, w, h - g),
        solid("vault", 0, 0, w, vault),
        solid("west_wall", 0, vault, WALL, g - vault),
        solid("east_wall", w - WALL, vault, WALL, g - 112 - vault),
        edge("secret_first_lab_east", "back through the bricked door", w - WALL, g, PLANT, "secret_plant_west"),
        start(rid, w - 120, g),
        ledge("camp_bed", 64, 480, 160),
        ledge("sample_cabinet", 240, cabinet_top, 96),
        ledge("first_lab_bench", 352, 448, 208),
        entity("ChestSpawn", 250, cabinet_top - 58, 76, 58, name="the first grant (unspent)", reward="currency:120"),
        sign("first_lab_sign", 320, 90, "Where it began (please do not tidy)", 420),
    ]
    return build(rid, e, "LAB 0")


#: QED-TV's door on the lecture hall's terrace (quad x).
QED_DOOR_X = 1660
#: The two overhead walks use these room coordinates in the prop art.
QED_GRID = (600, 1580, 340)
QED_PRODUCTION_WALK = (1616, 2000, 400)


def qed_studios():
    """QED-TV: a reception, the studio and the production room in one long
    hall, floor 640. The front desk (y 600) and the couch (y 608); the
    anchor desk (y 584) and Will Force beside it on his way to the
    demonstration bench (y 592); the lighting grid (y 340) up a ladder, a
    box of spare bow ties on it; the vision mixer (y 600) and the weather
    centre's green wall."""
    rid = QED
    _, (w, h) = ROOMS_AT[rid]
    floor, ceiling = h - 64, 32
    g0, g1, gy = QED_GRID
    bx0, bx1, by = QED_PRODUCTION_WALK
    ladders = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [592, 320], size: [48, {floor - 320}]),
        (kind: "Ladder", px: [1952, {by - 16}], size: [32, {floor - by + 16}]),
    ]),"""
    e = [
        solid("floor", 0, floor, w, 64),
        solid("ceiling", 0, 0, w, ceiling),
        solid("west_wall", 0, ceiling, WALL, floor - ceiling),
        solid("east_wall", w - WALL, ceiling, WALL, floor - ceiling),
        door("qed_door", "out to the quad", 40, floor, QUAD, "quad_qed_door"),
        start(rid, 140, floor),
        # The reception.
        ledge("reception_desk", 180, floor - 40, 150),
        ledge("waiting_couch", 440, floor - 32, 120),
        resident("npc_eureka_petra_dish", "eureka_petra_dish", 364, floor),
        sign("qed_sign_reception", 300, 72, "QED-TV: QUOD ERAT DEMONSTRANDUM", 420),
        sign("qed_sign_sign_in", 255, floor - 120, "Guests sign in. Autographs by appointment.", 380),
        # The studio.
        ledge("anchor_desk", 780, floor - 56, 180),
        resident("npc_will_force", "eureka_will_force", 1000, floor, h=74),
        walk("lighting_grid", g0, gy, g1 - g0),
        walk("production_walk", bx0, by, bx1 - bx0),
        entity("ChestSpawn", 1120, gy - 58, 76, 58, name="a box of spare bow ties", reward="currency:40"),
        ledge("demonstration_bench", 1320, floor - 48, 200),
        sign("qed_sign_demonstration", 1420, floor - 272, "DEMONSTRATION AREA: goggles past this line", 440),
        sign("qed_sign_excused", 1420, floor - 246, "(The anchor is excused. The hair is insured.)", 440),
        # The production room.
        ledge("vision_mixer", 1700, floor - 40, 240),
        resident("npc_eureka_avery_gadro", "eureka_avery_gadro", 1660, floor),
        resident("npc_eureka_barry_metric", "eureka_barry_metric", 2090, floor),
        sign("qed_sign_production", 1810, 72, "PRODUCTION: quiet when the light is red", 420),
        sign("qed_sign_weather", 2060, 250, "WEATHER CENTRE: the wall is green; the forecast is not", 300),
    ]
    return build(rid, e, None, music=LAB_MUSIC, extra=ladders)


# The buildings first (they move out of the plant's way).
ROOMS = (patent_office, coil_lab, qed_studios, terminus, elevator_climb, elevator_station, quad, court, test_range, observatory, plant, first_lab,
         collider)

#: The gate network's ring and terminal in the gate court, if it has written
#: them: a regenerate of the rooms puts them back.
GATE_INTERFACE = HERE / "gate_interface.yaml"


def main(argv):
    made = []
    for make in ROOMS:
        rid, text = make()
        path = SPEC_OUT / f"{rid}.ron"
        path.write_text(text)
        made.append(path)
        print(path)
    if "--apply" not in argv:
        return 0
    if code := make_rooms(WORLD_LDTK, made):
        return code
    # An LDtk-owned court is not made again, so it keeps its ring: a second
    # add would duplicate the arrival zone.
    from ambition_ldtk_tools import generated_record
    court_kept = COURT in generated_record.load(WORLD_LDTK)["ldtk_owned"]
    if GATE_INTERFACE.exists() and not court_kept:
        code, _ = run("entity", "add", str(GATE_INTERFACE), "--ldtk", str(WORLD_LDTK), "--in-place")
        if code:
            return code
    if code := paint(WORLD_LDTK, QUAD, "Climbable", 1, MANHOLE[0] + 16, 768 - 80, 32, 896 - 768 + 80):
        return code
    code, _ = run("validate", str(WORLD_LDTK))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
