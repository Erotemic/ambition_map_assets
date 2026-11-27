#!/usr/bin/env python3
"""Write the rooms of the Frontier dimension: Dry Dock, the spaceport town in
the Leaden Saddle, and Marshal Gallus's Ore Corral
(`docs/planning/game/leadensaddle.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/frontier/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/frontier/make_specs.py --apply  # and makes the rooms
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/frontier/make_specs.py --apply --hall  # and the hall's door

Run it from the repository root. Change the script, not the rooms.

The world file is `frontier.ldtk`. The gate (address LEADENSADDLE) stands on
Pad Three. The pass runs west to east; the outdoor rooms join by edges, and
the two buildings (the saloon, the livery) by doors:

                          door           door
                   [The Wet Whistle] [the livery]
                                |       |
 [Pad Three] ==== [      Main Street      ] ==== [the refinery] ==== [the Ore Corral] -grille-> [the lookout]

- `frontier_landing_pad`: the gate and its terminal on the apron, the
  clerk's booth (its roof a step up), a stack of cargo boxes, the cargo deck
  of the freighter on the next pad.
- `frontier_main_street`: a boardwalk each side (one small step up), the
  porch roofs over it, the water tower in the middle, the saloon's door and
  the livery's, the Marshal's ordinances on a board.
- `frontier_wet_whistle`, `frontier_livery`: the two interiors, each a
  balcony or a hayloft up.
- `frontier_refinery`: the flank of the east mesa, in terraces joined by
  slopes (the ground climbs 320 from west to east), pipe racks and the
  cracking tower's platforms over the terraces. The Marshal's posse
  (chickens).
- `frontier_ore_corral`: the arena. A level yard, a loading dock each side
  one jump up, a catwalk over each a double jump up. The way on to the
  lookout is behind a grille that the Marshal's defeat opens
  (`boss.cleared frontier.marshal_gallus`).
- `frontier_saddle_lookout`: the mesa path and survey decks lead to the summit.
- `hall_marshal_gallus_corral`: the Hall of Bosses' practice copy of the
  corral (placement `hall.marshal_gallus`), by a door on the hall's lower
  floor.

The robot's numbers (`district_kit`): a jump rises 83, a jump and a double
jump 139; a step of 64 is one jump.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_frontier_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))
sys.path.insert(0, str(HERE))

from district_kit import SANDBOX_LDTK, WALL, WORLDS, add_entities, door, edge, ensure_world, entity, ledge, make_rooms, resident, room, run, sign, solid, start  # noqa: E402

import gates  # noqa: E402
from blurbs import BLURB  # noqa: E402
from props import scenery  # noqa: E402

WORLD = WORLDS / "frontier.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/frontier/make_specs.py"
UID_OFFSET = 1500000

PAD = "frontier_landing_pad"
MAIN = "frontier_main_street"
WHISTLE = "frontier_wet_whistle"
LIVERY = "frontier_livery"
REFINERY = "frontier_refinery"
CORRAL = "frontier_ore_corral"
LOOKOUT = "frontier_saddle_lookout"
HALL_CORRAL = "hall_marshal_gallus_corral"
HALL_CORRAL_ENTRY = "hall_marshal_gallus_corral_entry"
HALL = "hall_of_bosses"
HALL_DOOR = "hall_to_marshal_gallus_portal"
HALL_SWITCH = "hall_marshal_gallus_life_switch"
HALL_PLACEMENT = "hall.marshal_gallus"

# The first slice west of Dry Dock
# (`docs/planning/game/techno-western-frontier-first-slice.md`): Halfway
# Siding, the auxiliary gate town on the gulch rim; the Number 9 ore freight
# on the gulch floor, robbed by the Rustler; Clinker Flats down the line,
# which joins Dry Dock's Pad Three by the railhead.
STATION = "frontier_siding_station"
SIDING_STREET = "frontier_siding_street"
INN = "frontier_lie_down_inn"
TRESTLE = "frontier_siding_trestle"
SPROCKET = "frontier_sprocket_row"
TAIL = "frontier_freight_tail"
CARS = "frontier_freight_cars"
HEAD = "frontier_rustler_head"
YARD = "frontier_clinker_yard"
WORKS = "frontier_clinker_works"
ROW = "frontier_clinker_row"
RAILHEAD = "frontier_clinker_railhead"

#: The Marshal's placement. His defeat is saved under this id, and it opens
#: the corral's grille (`boss.cleared <id>`).
PLACEMENT = "frontier.marshal_gallus"

BG = "#3A2418"
#: The rooms name the Frontier's cue; `music_cues.ron` binds each room to
#: its section (the town, the saloon, the refinery, the mesa top).
TOWN_MUSIC = "leaden_saddle"
SALOON_MUSIC = TOWN_MUSIC
REFINERY_MUSIC = TOWN_MUSIC
#: The first slice's cues: the siding (its platform, the inn, the trestle,
#: Sprocket Row), the freight (the cars, the Rustler) and Clinker Flats (the
#: works, the Row); `music_cues.ron` binds each room to its section.
SIDING_MUSIC = "halfway_siding"
FREIGHT_MUSIC = "the_rustler"
FLATS_MUSIC = "clinker_flats"
#: The freight's backdrop runs west at this speed (world px/s): the train
#: stands still in its rooms and the gulch goes by.
FREIGHT_SCROLL = -720

#: Each room: where it is on the flat map, and its size. The outdoor rooms
#: are side by side as they are walked, their floors at one height where
#: they join; the interiors are above the street.
ROOMS_AT = {
    PAD: ((0, 0), (2000, 768)),
    MAIN: ((2000, 0), (2800, 768)),
    WHISTLE: ((2400, -800), (1280, 576)),
    LIVERY: ((4000, -800), (1120, 576)),
    REFINERY: ((4800, -192), (2800, 960)),
    CORRAL: ((7600, -192), (1600, 640)),
    LOOKOUT: ((9200, -192), (1600, 640)),
    HALL_CORRAL: ((0, 1600), (1600, 640)),
    # The first slice, west of the pad: the siding on the rim, the trestle
    # down to the gulch floor, the freight under it, Clinker Flats east of
    # the freight and up to the pad. The tall rooms hold two levels.
    STATION: ((-18800, -1536), (1600, 768)),
    SIDING_STREET: ((-17200, -1536), (2400, 768)),
    INN: ((-17200, -2400), (1280, 576)),
    TRESTLE: ((-14800, -1536), (2400, 1536)),
    SPROCKET: ((-12400, -1536), (2000, 768)),
    TAIL: ((-14800, 0), (2400, 768)),
    CARS: ((-12400, 0), (2800, 768)),
    HEAD: ((-9600, 0), (2400, 768)),
    YARD: ((-7200, -768), (2400, 1536)),
    WORKS: ((-4800, -768), (2400, 768)),
    ROW: ((-4800, 0), (2400, 768)),
    RAILHEAD: ((-2400, -768), (2400, 1536)),
}

#: The street's floor, and the boardwalk one small step over it.
STREET = 640
PAD_LOAD_PATH = (
    ("cargo_scale", 544, 640, 576),
    ("arrivals_loading_walk", 848, 976, 528),
    ("cargo_loading_walk", 1200, 1296, 512),
    ("freighter_service_landing", 1752, 1848, 512),
    ("freighter_service_step", 1840, 1952, 576),
)
TOWER_SERVICE_PATH = (
    ("pump_supply_crate", 1616, 1712, 544),
    ("pump_lower_walk", 1584, 1680, 464),
    ("pump_upper_walk", 1456, 1568, 416),
)
BOARDWALK = STREET - 32
#: The corral: its floor 64 over the room's bottom (the Rhai script's
#: `FLOOR_INSET`), the docks a jump over it, the catwalks a double jump over them.
CORRAL_FLOOR = 576
DOCK = CORRAL_FLOOR - 64
CATWALK = DOCK - 128
DOCK_W = 224
#: The Marshal's body box (`boss_sheets.ron`: the frame is drawn 5/3 of it tall).
MARSHAL_W, MARSHAL_H = 96, 140

#: The steepest a path may climb (Hobford's rule): about 23 degrees.
MAX_SLOPE = 0.42
SLOPE_STUB = 32


def slope(name, x0, y0, x1, y1):
    """A path that climbs or falls, west to east, as the hill it is (filled
    under). Each end meets the flat top of a block."""
    if x1 <= x0 or abs(y1 - y0) > MAX_SLOPE * (x1 - x0):
        raise SystemExit(f"{name}: ({x0},{y0}) to ({x1},{y1}) is steeper than {MAX_SLOPE} or not west to east")
    if any(v % 16 for v in (x0, y0, x1, y1)):
        raise SystemExit(f"{name}: ({x0},{y0}) to ({x1},{y1}) has an end off the 16 px grid")
    points = f"{x0 - SLOPE_STUB},{y0}; {x0},{y0}; {x1},{y1}; {x1 + SLOPE_STUB},{y1}"
    return entity("SurfaceChain", x0, min(y0, y1) - 16, 16, 16, name=name, points=points, fill=True)


def side_walls(w, h, west, east):
    """The side walls of an outdoor room, over the floor where each side's
    edge stands (`None`: a whole wall, no edge on that side)."""
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


def chicken(rid, n, x, floor, hen=False):
    """One of the Marshal's posse: a game chicken that runs straight at you."""
    character = "chicken_hen" if hen else "chicken"
    return entity("EnemySpawn", x - 16, floor - 48, 32, 48, name=f"{rid}_{character}_{n}", brain="combatant",
                  character_id=character, respawn="OnRoomReenter")


def vertical_edge(zone, name, x0, x1, y, to_room, to_zone, height=16):
    """An edge exit across the top (`y` 0) or the bottom of a room."""
    return entity("LoadingZone", x0, y, x1 - x0, height, id=zone, name=name, activation="EdgeExit", target_room=to_room,
                  target_zone=to_zone, bidirectional=True)


def ramp(name, x0, y0, x1, y1):
    """A road on trestles that climbs or falls west to east (not filled under:
    the street goes on beneath it). A walker on the street steps onto its
    foot only holding up."""
    if x1 <= x0 or abs(y1 - y0) > MAX_SLOPE * (x1 - x0):
        raise SystemExit(f"{name}: ({x0},{y0}) to ({x1},{y1}) is steeper than {MAX_SLOPE} or not west to east")
    points = f"{x0},{y0}; {x1},{y1}"
    return entity("SurfaceChain", x0, min(y0, y1) - 16, 16, 16, name=name, points=points, fill=False, boarding="up")


def build(rid, e, title, music, dangerous=False, biome="frontier", extra=""):
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e + blurb(rid, size[0] // 2), at=at, size=size, biome=biome, music=music, bg=BG, title=title,
                generator=GENERATOR, dangerous=dangerous, extra=extra)
    return rid, text


def landing_pad():
    rid = PAD
    w, h = ROOMS_AT[rid][1]
    floor = STREET
    e = [
        solid("apron", 0, floor, w, h - floor),
        *side_walls(w, h, floor, floor),
        edge("pad_from_railhead", "west down the line", 0, floor, RAILHEAD, "railhead_to_pad"),
        # The gate (LEADENSADDLE) and its terminal: the way in and the way home.
        *gates.as_ron(gates.ring("Pad Three Gate", "frontier_pad_gate", 96, floor, "the gate")),
        *gates.as_ron(gates.terminal("Pad Three Gate", "frontier_gate_terminal", 400, floor)),
        start(rid, 540, floor),
        sign("pad_sign_name", 300, floor - 360, "PAD THREE", 220),
        sign("pad_sign_toll", 300, floor - 330, "ORDINANCE 2: GATE TOLL, PAYABLE TO THE MARSHAL", 520),
        # The clerk's booth; its flat roof is a step for the bold.
        ledge("booth_roof", 640, floor - 112, 208),
        sign("pad_sign_booth", 744, floor - 152, "ARRIVALS", 140),
        # Dolores Pike, the clerk, at the booth's window.
        resident("npc_frontier_clerk", "frontier_clerk", 700, floor),
        # Cargo containers in a stack (their tops are ledges, so the art
        # draws the boxes): one jump, then one more, up to the freighter's
        # open cargo deck on the next pad.
        ledge("box_low_west", 1008, floor - 64, 128),
        ledge("box_high", 1072, floor - 128, 128),
        ledge("box_low_east", 1200, floor - 64, 112),
        ledge("freighter_cargo_deck", 1328, floor - 192, 400),
        *[ledge(name, left, top, right - left) for name, left, right, top in PAD_LOAD_PATH],
        sign("pad_sign_ship", 1528, floor - 290, "HOLD 2: FEED, BOLTS, MAIL", 300),
        edge("pad_to_street", "into town", w - WALL, floor, MAIN, "street_from_pad"),
    ]
    return build(rid, e, "PAD THREE", TOWN_MUSIC)


def main_street():
    rid = MAIN
    w, h = ROOMS_AT[rid][1]
    floor = STREET
    porch = BOARDWALK - 112
    tower = porch - 96
    e = [
        solid("street", 0, floor, w, h - floor),
        *side_walls(w, h, floor, floor),
        edge("street_from_pad", "to Pad Three", 0, floor, PAD, "pad_to_street"),
        edge("street_to_refinery", "to the refinery", w - WALL, floor, REFINERY, "refinery_from_street"),
        start(rid, 100, floor),
        # The boardwalks in front of the shops, and the porch roofs over them.
        solid("boardwalk_west", 160, BOARDWALK, 960, floor - BOARDWALK),
        solid("boardwalk_east", 1616, BOARDWALK, 1040, floor - BOARDWALK),
        ledge("porch_saloon", 208, porch, 400),
        ledge("porch_store", 672, porch, 400),
        ledge("porch_livery", 1664, porch, 432),
        ledge("porch_assay", 2160, porch, 432),
        *[ledge(name, left, top, right - left) for name, left, right, top in TOWER_SERVICE_PATH],
        # The water tower in the middle of the street, its walk a double
        # jump over the porch roofs' height, reached from the store's porch.
        ledge("water_tower_walk", 1200, tower, 240),
        chest("a strongbox someone hid up the water tower", "currency:30", 1282, tower),
        # The saloon and the livery: buildings, so their ways in are doors.
        door("street_saloon_door", "into The Wet Whistle", 392, BOARDWALK, WHISTLE, "whistle_door"),
        sign("street_sign_saloon", 416, porch - 32, "THE WET WHISTLE", 240),
        door("street_livery_door", "into the livery", 1880, BOARDWALK, LIVERY, "livery_door"),
        sign("street_sign_livery", 1904, porch - 32, "BELL'S LIVERY: MULES BY THE DAY", 340),
        sign("street_sign_store", 872, porch - 32, "DRY GOODS AND PARTS", 260),
        sign("street_sign_assay", 2376, porch - 32, "ASSAY OFFICE", 200),
        # The Marshal's ordinances on a board by the water tower.
        sign("ordinance_title", 1320, floor - 200, "ORDINANCES OF DRY DOCK, BY ORDER OF THE MARSHAL", 520),
        sign("ordinance_1", 1320, floor - 172, "1. DAWN IS WHEN THE MARSHAL'S WHISTLE BLOWS.", 480),
        sign("ordinance_4", 1320, floor - 148, "4. NO TRAVELLERS PAST THE REFINERY AFTER THE WHISTLE.", 560),
        sign("ordinance_9", 1320, floor - 124, "9. NOBODY CROWS BUT THE MARSHAL.", 380),
    ]
    return build(rid, e, "MAIN STREET, DRY DOCK", TOWN_MUSIC)


def interior_shell(w, h, floor):
    return [
        solid("floor", 0, floor, w, h - floor),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        solid("east_wall", w - WALL, 32, WALL, floor - 32),
    ]


def wet_whistle():
    rid = WHISTLE
    w, h = ROOMS_AT[rid][1]
    floor = 512
    balcony = floor - 160
    e = interior_shell(w, h, floor) + [
        door("whistle_door", "out to Main Street", 64, floor, MAIN, "street_saloon_door"),
        start(rid, 150, floor),
        # Mae behind the bar; Elias at a table.
        resident("npc_frontier_barkeep", "frontier_barkeep", 884, floor),
        resident("npc_frontier_prospector", "frontier_prospector", 380, floor),
        # The entrance steps and the bar lead up to the balcony.
        ledge("whistle_entry_step", 144, 448, 80),
        ledge("whistle_entry_landing", 176, 400, 64),
        ledge("whistle_stair", 672, floor - 80, 320),
        ledge("whistle_balcony", 240, balcony, 752),
        # The stage at the east end, where the piano is.
        solid("whistle_stage", 1008, floor - 48, w - WALL - 1008, 48),
        sign("whistle_sign_drinks", 440, 120, "WATER 2  -  COFFEE 3  -  WHISKEY 5  -  COOLANT (DO NOT DRINK) 1", 640),
        sign("whistle_sign_piano", 1130, floor - 180, "PLEASE DO NOT SHOOT THE PIANO", 300),
    ]
    return build(rid, e, "THE WET WHISTLE", SALOON_MUSIC, biome="frontier_interior")


def livery():
    rid = LIVERY
    w, h = ROOMS_AT[rid][1]
    floor = 512
    loft = floor - 128
    e = interior_shell(w, h, floor) + [
        door("livery_door", "out to Main Street", 64, floor, MAIN, "street_livery_door"),
        start(rid, 150, floor),
        ledge("livery_west_step", 464, floor - 64, 48),
        # Gus Bell, by the stalls.
        resident("npc_frontier_liveryman", "frontier_liveryman", 300, floor),
        ledge("livery_hayloft", 560, loft, 480),
        ledge("livery_east_bales", 1008, floor - 64, w - WALL - 1008),
        sign("livery_sign_rules", 300, 120, "MULES BY THE DAY. RETURN WITH THE SAME NUMBER OF LEGS.", 560),
    ]
    climb = '( kind: "Ladder", px: [528, 352], size: [32, 160] )'
    return build(rid, e, "BELL'S LIVERY", TOWN_MUSIC, biome="frontier_interior",
                 extra=f"\n    intgrid: (climbable: [{climb}]),")


def refinery():
    rid = REFINERY
    w, h = ROOMS_AT[rid][1]
    west, t1, t2, shelf = 832, 704, 576, 512
    e = [
        *side_walls(w, h, west, shelf),
        edge("refinery_from_street", "back to Main Street", 0, west, MAIN, "street_to_refinery"),
        edge("refinery_to_corral", "on to the Ore Corral", w - WALL, shelf, CORRAL, "corral_from_refinery"),
        start(rid, 120, west),
        solid("gate_yard", 0, west, 400, h - west),
        # Ruth Harlan, the night-shift foreman, at the foot of the road.
        resident("npc_frontier_foreman", "frontier_foreman", 290, west),
        slope("lower_road", 400, west, 800, t1),
        solid("terrace_tanks", 800, t1, 480, h - t1),
        slope("upper_road", 1280, t1, 1600, t2),
        solid("terrace_tower", 1600, t2, 560, h - t2),
        solid("corral_shelf", 2160, shelf, w - 2160, h - shelf),
        # The walkway crosses from the tanks to the upper road.
        ledge("pipe_rack_walk", 880, t1 - 128, 720),
        # The cracking tower's platforms over the upper terrace.
        ledge("tower_platform_low", 1696, t2 - 128, 208),
        ledge("tower_platform_high", 1824, t2 - 256, 176),
        chest("the night shift's tip jar", "currency:40", 1874, t2 - 256),
        chicken(rid, 1, 1040, t1),
        chicken(rid, 2, 1120, t1, hen=True),
        chicken(rid, 3, 1760, t2),
        chicken(rid, 4, 2040, t2, hen=True),
        chicken(rid, 5, 2440, shelf),
        sign("refinery_sign_name", 600, west - 260, "DRY DOCK REFINERY  -  NO OPEN FLAME", 440),
        sign("refinery_sign_shift", 1440, t1 - 300, "THE SHIFT STARTS AT THE WHISTLE", 360),
        sign("refinery_sign_corral", 2480, shelf - 200, "ORE CORRAL  -  MARSHAL'S BUSINESS", 360),
    ]
    ladders = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [912, {t2}], size: [32, {t1 - t2}]),
        (kind: "Ladder", px: [1840, {t2 - 256}], size: [32, 256]),
    ]),"""
    return build(rid, e, "THE REFINERY", REFINERY_MUSIC, dangerous=True, biome="frontier_refinery", extra=ladders)


def corral_floor_plan(rid, placement, west_way):
    """The corral: the yard, the two docks and their catwalks, the Marshal.
    The main game's and the hall's copy share it. `west_way` is the entity
    of the way in on the west dock."""
    w, h = ROOMS_AT[rid][1]
    return [
        solid("yard", 0, CORRAL_FLOOR, w, h - CORRAL_FLOOR),
        solid("west_wall", 0, 0, WALL, DOCK - 96),
        solid("west_dock", WALL, DOCK, DOCK_W, CORRAL_FLOOR - DOCK),
        solid("east_dock", w - WALL - DOCK_W, DOCK, DOCK_W, CORRAL_FLOOR - DOCK),
        # The catwalks stop short of the walls: the east one must clear the
        # lintel over the corral's gate.
        ledge("west_catwalk", 96, CATWALK, 256),
        ledge("east_catwalk", w - 96 - 256, CATWALK, 256),
        west_way,
        start(rid, 200, DOCK),
        entity("BossSpawn", w // 2 - MARSHAL_W // 2, CORRAL_FLOOR - MARSHAL_H, MARSHAL_W, MARSHAL_H, name="Marshal Gallus",
               brain="PhaseScript:marshal_gallus", encounter_id=placement),
    ]


def ore_corral():
    rid = CORRAL
    w, h = ROOMS_AT[rid][1]
    grille_x = w - WALL - 64
    e = corral_floor_plan(rid, PLACEMENT, edge("corral_from_refinery", "back to the refinery", 0, DOCK, REFINERY,
                                               "refinery_to_corral")) + [
        solid("east_wall", w - WALL, 0, WALL, DOCK - 96),
        # The way in shuts behind the player while the Marshal fights, so a
        # knockback cannot carry them out by the west edge; it is open while
        # he sleeps and again once he falls.
        entity("LockWall", WALL, DOCK - 112, WALL, 112, id="corral_west_gate", name="the corral's west gate",
               gated_by=f"boss.at_rest {PLACEMENT}", look="temple_gate_iron"),
        # The corral's gate to the mesa top, shut until the Marshal falls.
        entity("LockWall", grille_x, DOCK - 112, WALL, 112, id="corral_lookout_grille", name="the corral's gate",
               gated_by=f"boss.cleared {PLACEMENT}", look="temple_gate_iron"),
        solid("grille_lintel", grille_x, 0, WALL, DOCK - 112),
        edge("corral_to_lookout", "up to the lookout", w - WALL, DOCK, LOOKOUT, "lookout_from_corral"),
    ]
    return build(rid, e, "THE ORE CORRAL", REFINERY_MUSIC, dangerous=True, biome="frontier_refinery")


def hall_corral():
    """The Hall of Bosses' copy of the corral: a practice Marshal of its own
    (`hall.marshal_gallus`), its door back to the hall and no way on."""
    rid = HALL_CORRAL
    w, h = ROOMS_AT[rid][1]
    e = corral_floor_plan(rid, HALL_PLACEMENT, door(HALL_CORRAL_ENTRY, "back to the hall", 48, DOCK, HALL, HALL_DOOR)) + [
        solid("east_wall", w - WALL, 0, WALL, CORRAL_FLOOR),
        solid("west_wall_low", 0, DOCK - 96, WALL, 96),
    ]
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e, at=at, size=size, biome="frontier_refinery", music=REFINERY_MUSIC, bg=BG,
                title="MARSHAL GALLUS (PRACTICE)", generator=GENERATOR, dangerous=True,
                extra="\n    practice: true,")
    return rid, text


def saddle_lookout():
    rid = LOOKOUT
    w, h = ROOMS_AT[rid][1]
    low, top = DOCK, DOCK - 128
    e = [
        *side_walls(w, h, low, None),
        edge("lookout_from_corral", "down to the corral", 0, low, CORRAL, "corral_to_lookout"),
        start(rid, 120, low),
        solid("mesa_shelf", 0, low, 480, h - low),
        slope("summit_path", 480, low, 800, top),
        solid("summit", 800, top, w - 800, h - top),
        ledge("survey_west_deck", 272, 448, 128),
        ledge("survey_middle_deck", 448, 384, 144),
        ledge("survey_rim_deck", 640, 320, 176),
        ledge("lookout_roof", 880, 272, 240),
        chest("the gate tolls", "currency:150", 1340, top),
        sign("lookout_sign", 1100, top - 240, "THE LEADEN SADDLE: THE TOWN, THE PADS, THE PASS", 520),
    ]
    return build(rid, e, "THE MESA TOP", TOWN_MUSIC)


# ---------------------------------------------------------------------------
# The first slice: Halfway Siding, the Number 9 freight, Clinker Flats
# ---------------------------------------------------------------------------

#: The siding's floor, its platform and boardwalks a step over it, the porch
#: roofs (as Dry Dock's street).
RIM = STREET


def siding_station():
    """The auxiliary gate (SIDING) and its terminal on the apron at the west
    end, the rail halt's platform and station house, the agent at her
    window."""
    rid = STATION
    w, h = ROOMS_AT[rid][1]
    floor = RIM
    platform = floor - 32
    e = [
        solid("apron", 0, floor, w, h - floor),
        *side_walls(w, h, None, floor),
        *gates.as_ron(gates.ring("Halfway Siding Gate", "frontier_siding_gate", 96, floor, "the gate")),
        *gates.as_ron(gates.terminal("Halfway Siding Gate", "frontier_siding_terminal", 420, floor)),
        start(rid, 520, floor),
        sign("station_sign_gate", 260, floor - 360, "AUXILIARY GATE TERMINAL", 300),
        sign("station_sign_rest", 260, floor - 332, "ARRIVALS: REST BEFORE YOU TRAVEL ON", 400),
        slope("station_west_ramp", 544, floor, 640, platform),
        solid("station_platform", 640, platform, 848, floor - platform),
        slope("station_east_ramp", 1488, platform, 1584, floor),
        ledge("station_roof", 720, platform - 160, 480),
        ledge("baggage_table", 576, platform - 48, 64),
        ledge("baggage_awning", 640, platform - 112, 96),
        ledge("trunks_low", 1232, platform - 48, 96),
        ledge("trunks_high", 1280, platform - 112, 96),
        sign("station_sign_name", 960, platform - 216, "HALFWAY SIDING", 260),
        sign("station_sign_times", 1360, platform - 200, "NO. 9 ORE FREIGHT, DOWN THE GULCH: 9:40", 420),
        # Augusta Pell, the agent, at the ticket window.
        resident("npc_frontier_station_agent", "frontier_station_agent", 900, platform),
        edge("station_to_street", "into town", w - WALL, floor, SIDING_STREET, "street_from_station"),
    ]
    return build(rid, e, "HALFWAY SIDING STATION", SIDING_MUSIC, biome="frontier_siding")


def siding_street():
    """The one street: the inn (a door), the mercantile, the windmill and its
    trough, the telegraph office, the signpost to the trestle."""
    rid = SIDING_STREET
    w, h = ROOMS_AT[rid][1]
    floor = RIM
    walk = floor - 32
    porch = walk - 112
    e = [
        solid("street", 0, floor, w, h - floor),
        *side_walls(w, h, floor, floor),
        edge("street_from_station", "to the station", 0, floor, STATION, "station_to_street"),
        edge("street_to_trestle", "to the trestle", w - WALL, floor, TRESTLE, "trestle_from_street"),
        start(rid, 48, floor),
        slope("inn_ramp", 80, floor, 160, walk),
        solid("boardwalk_west", 160, walk, 928, floor - walk),
        slope("mercantile_ramp", 1088, walk, 1168, floor),
        slope("telegraph_ramp", 1360, floor, 1440, walk),
        solid("boardwalk_east", 1440, walk, 720, floor - walk),
        slope("trestle_road_ramp", 2160, walk, 2240, floor),
        ledge("porch_inn", 200, porch, 440),
        ledge("porch_store", 700, porch, 360),
        ledge("porch_telegraph", 1460, porch, 320),
        ledge("mercantile_supply_crate", 992, walk - 48, 80),
        ledge("telegraph_wire_reels", 1408, walk - 48, 64),
        ledge("telegraph_service_walk", 1392, porch, 64),
        ledge("windmill_platform", 1136, porch - 64, 208),
        chest("a coffee tin of coins on the windmill", "currency:15", 1206, porch - 64),
        door("street_inn_door", "into The Lie-Down Inn", 396, walk, INN, "inn_door"),
        sign("street_sign_inn", 420, porch - 32, "THE LIE-DOWN INN", 240),
        sign("street_sign_store", 880, porch - 32, "HALFWAY MERCANTILE", 240),
        sign("street_sign_telegraph", 1620, porch - 32, "TELEGRAPH", 160),
        sign("street_sign_post_1", 2020, floor - 200, "SPROCKET ROW, MECHANICS: OVER THE TRESTLE", 440),
        sign("street_sign_post_2", 2020, floor - 172, "DRY DOCK: BY RAIL, DOWN THE GULCH", 380),
    ]
    ladder = "\n    intgrid: (climbable: [(kind: \"Ladder\", px: [1344, 400], size: [32, 240])]),"
    return build(rid, e, "HALFWAY SIDING", SIDING_MUSIC, biome="frontier_siding", extra=ladder)


def lie_down_inn():
    """The recovery inn: the desk, a row of cots for the gate-sick (Alice and
    Bob on two of them), the stair to the rooms upstairs."""
    rid = INN
    w, h = ROOMS_AT[rid][1]
    floor = 512
    e = interior_shell(w, h, floor) + [
        door("inn_door", "out to the street", 64, floor, SIDING_STREET, "street_inn_door"),
        start(rid, 150, floor),
        # Pearl Featherstone at her desk; Alice and Bob, resting.
        resident("npc_frontier_innkeeper", "frontier_innkeeper", 300, floor),
        resident("npc_alice", "frontier_inn_alice", 700, floor),
        resident("npc_bob", "frontier_inn_bob", 820, floor),
        ledge("linen_chest", 368, floor - 64, 80),
        ledge("inn_stair", 976, floor - 64, 112),
        ledge("inn_gallery", 464, floor - 128, w - WALL - 464),
        sign("inn_sign_rates", 560, 120, "ROOMS BY THE HOUR. A BUCKET WITH EVERY COT.", 520),
        sign("inn_sign_quiet", 736, 308, "QUIET PLEASE: GUESTS ARE GATE-SICK", 320),
    ]
    return build(rid, e, "THE LIE-DOWN INN", SIDING_MUSIC, biome="frontier_interior")


#: The trestle's deck, as the street's floor; the loose planks over the hole.
DECK = RIM
PLANKS_X0, PLANKS_X1 = 1120, 1280
WEST_HATCH, EAST_HATCH = 544, 1792
HATCH_WIDTH = 64
INSPECTION_WALK = 848


def siding_trestle():
    """The rail trestle's road deck over the gulch. Its loose planks (a
    one-way floor: a body that drops through them falls) are over the gulch
    floor, where the Number 9 freight passes: the bottom of the room is the
    way down onto it."""
    rid = TRESTLE
    w, h = ROOMS_AT[rid][1]
    exit_depth = 384
    e = [
        solid("deck_west_end", 0, DECK, WEST_HATCH, 32),
        solid("deck_west_span", WEST_HATCH + HATCH_WIDTH, DECK, PLANKS_X0 - WEST_HATCH - HATCH_WIDTH, 32),
        solid("deck_east_span", PLANKS_X1, DECK, EAST_HATCH - PLANKS_X1, 32),
        solid("deck_east_end", EAST_HATCH + HATCH_WIDTH, DECK, w - EAST_HATCH - HATCH_WIDTH, 32),
        ledge("west_inspection_hatch", WEST_HATCH, DECK, HATCH_WIDTH),
        ledge("east_inspection_hatch", EAST_HATCH, DECK, HATCH_WIDTH),
        ledge("loose_planks", PLANKS_X0, DECK, PLANKS_X1 - PLANKS_X0),
        solid("west_inspection_walk", WEST_HATCH - 16, INSPECTION_WALK, PLANKS_X0 - WEST_HATCH + 32, 16),
        solid("east_inspection_walk", PLANKS_X1 - 16, INSPECTION_WALK, EAST_HATCH + HATCH_WIDTH + 32 - PLANKS_X1, 16),
        *side_walls(w, h, DECK, DECK),
        edge("trestle_from_street", "back to the siding", 0, DECK, SIDING_STREET, "street_to_trestle"),
        edge("trestle_to_sprocket", "on to Sprocket Row", w - WALL, DECK, SPROCKET, "sprocket_from_trestle"),
        # A falling body must stay in the exit zone while the room loads.
        vertical_edge("trestle_to_freight", "down onto the freight", WALL, w - WALL, h - exit_depth,
                      TAIL, "freight_from_trestle", height=exit_depth),
        start(rid, 120, DECK),
        sign("trestle_sign_name", 600, DECK - 200, "THE HALFWAY TRESTLE: 300 FEET TO THE GULCH FLOOR", 520),
        sign("trestle_sign_planks", PLANKS_X0 + 80, DECK - 120, "LOOSE PLANKS. STEP LIGHTLY.", 300),
        sign("trestle_sign_sprocket", 2100, DECK - 200, "SPROCKET ROW", 200),
    ]
    ladders = f"""
    intgrid: (climbable: [
        (kind: "Ladder", px: [{WEST_HATCH + 16}, 608], size: [32, 240]),
        (kind: "Ladder", px: [{EAST_HATCH + 16}, 608], size: [32, 240]),
    ]),"""
    return build(rid, e, "THE HALFWAY TRESTLE", SIDING_MUSIC, biome="frontier_siding", extra=ladders)


def sprocket_row():
    """The mechanics' street, with a raised route from the garage to the yard."""
    rid = SPROCKET
    w, h = ROOMS_AT[rid][1]
    floor = RIM
    e = [
        solid("street", 0, floor, w, h - floor),
        *side_walls(w, h, floor, None),
        edge("sprocket_from_trestle", "back over the trestle", 0, floor, TRESTLE, "trestle_to_sprocket"),
        start(rid, 100, floor),
        sign("sprocket_sign_arch", 240, floor - 250, "SPROCKET ROW: FITTERS, SMITHS, MECHANICS", 460),
        ledge("garage_workbench", 544, floor - 64, 112),
        ledge("garage_trolley", 944, floor - 64, 80),
        ledge("hoist_beam", 672, floor - 128, 288),
        ledge("transfer_walk", 992, floor - 144, 208),
        resident("npc_frontier_mechanic", "frontier_mechanic", 760, floor),
        sign("sprocket_sign_garage", 780, floor - 260, "HETTIE GIMBAL: REPAIRS OF ALL KINDS", 400),
        ledge("yard_parts_rack", 1216, floor - 64, 96),
        solid("boiler", 1312, floor - 112, 176, 48),
        ledge("yard_valve_bench", 1488, floor - 64, 96),
        # The workshops' rolling gate across the street's end.
        sign("sprocket_sign_gate", 1800, floor - 230, "WORKSHOPS: CLOSED FOR STOCKTAKE", 380),
    ]
    return build(rid, e, "SPROCKET ROW", SIDING_MUSIC, biome="frontier_siding")


# The freight: every car's underframe ends at UNDERFRAME, its wheels run on
# the rails under it, and the track bed under the cars puts a body that falls
# between two cars back at the room's start (a `HazardBlock`).
UNDERFRAME = 672
RAILS = 720


def car(name, x0, x1, top):
    """A car's body, from its roof (or deck) down to its underframe."""
    return solid(name, x0, top, x1 - x0, UNDERFRAME - top)


def track_bed(w):
    """The rails and the ballast under them: the hazard over the ground."""
    return [entity("HazardBlock", 0, RAILS, w, 32, name="track_bed"), solid("ballast", 0, RAILS + 32, w, 16)]


def sliding_crate(rid, n, x, deck, dx, speed=70.0):
    """A crate loose on a flat car's deck: the shaking slides it `dx` and back."""
    return entity("MovingPlatform", x, deck - 64, 64, 64, id=f"{rid}_loose_crate_{n}", name=f"a loose crate {n}",
                  sweep_dx=float(dx), speed=speed, visual="frontier_loose_crate")


def build_freight(rid, e, title, music=FREIGHT_MUSIC, extra=""):
    return build(rid, e, title, music, dangerous=True, biome="frontier_rails",
                 extra=f"\n    sky_scroll: {FREIGHT_SCROLL},{extra}")


FLAT = 608


def freight_tail():
    """The caboose, two loading cars, and a flat car to the east."""
    rid = TAIL
    w, h = ROOMS_AT[rid][1]
    e = track_bed(w) + [
        solid("tail_end", 0, 0, WALL, RAILS),
        vertical_edge("freight_from_trestle", "up to the trestle", WALL, w - WALL, 0, TRESTLE, "trestle_to_freight"),
        car("caboose", 32, 480, 512),
        solid("cupola", 160, 448, 140, 64),
        solid("caboose_gangway", 480, FLAT, 64, 16),
        solid("box_car_1_roof", 544, 480, 480, 16),
        car("box_car_1_deck", 544, 1024, FLAT),
        solid("box_car_gangway", 1024, FLAT, 64, 16),
        solid("box_car_2_roof", 1088, 480, 480, 16),
        car("box_car_2_deck", 1088, 1568, FLAT),
        solid("flat_car_gangway", 1568, FLAT, 80, 16),
        car("flat_car_1", 1648, w, FLAT),
        solid("crates_low", 1760, FLAT - 64, 128, 64),
        solid("crates_high", 1888, FLAT - 128, 80, 128),
        sliding_crate(rid, 1, 2080, FLAT, 200),
        start(rid, 1200, 480),
        # Hollis Teague, the brakeman, on the caboose's roof.
        resident("npc_frontier_brakeman", "frontier_brakeman", 380, 512),
        edge("freight_tail_to_cars", "along the train", w - WALL, FLAT, CARS, "freight_cars_from_tail"),
    ]
    ladders = """
    intgrid: (climbable: [
        (kind: "Ladder", px: [480, 448], size: [32, 160]),
        (kind: "Ladder", px: [1040, 448], size: [32, 160]),
        (kind: "Ladder", px: [1584, 448], size: [32, 160]),
    ]),"""
    return build_freight(rid, e, "THE NUMBER 9 FREIGHT", extra=ladders)


def freight_cars():
    """The tank and ore cars, a guarded roof over a sorting car, and a flat car."""
    rid = CARS
    w, h = ROOMS_AT[rid][1]
    e = track_bed(w) + [
        edge("freight_cars_from_tail", "back along the train", 0, FLAT, TAIL, "freight_tail_to_cars"),
        car("flat_car_1_end", 0, 360, FLAT),
        car("tank_car", 424, 904, 560),
        solid("tank_dome", 620, 512, 80, 48),
        car("ore_car_west", 960, 992, 560),
        solid("ore_car_bed", 992, 624, 432, UNDERFRAME - 624),
        solid("ore_car_east", 1424, 560, 32, UNDERFRAME - 560),
        solid("ore_gangway", 1456, FLAT, 48, 16),
        solid("sorting_car_roof", 1504, 496, 496, 16),
        car("sorting_car_deck", 1504, 2000, FLAT),
        entity("EnemySpawn", 1730 - 24, 496 - 70, 48, 70, name=f"{rid}_one_armed_bandit_0", brain="combatant",
               character_id="one_armed_bandit", respawn="OnRoomReenter"),
        solid("sorting_car_gangway", 2000, FLAT, 80, 16),
        car("flat_car_2", 2080, w, FLAT),
        solid("crates_stack", 2560, FLAT - 64, 128, 64),
        sliding_crate(rid, 1, 2140, FLAT, 300, 90.0),
        start(rid, 120, FLAT),
        edge("freight_cars_to_head", "on to the head of the train", w - WALL, FLAT, HEAD, "rustler_head_from_cars"),
    ]
    ladders = """
    intgrid: (climbable: [
        (kind: "Ladder", px: [1472, 464], size: [32, 144]),
        (kind: "Ladder", px: [2016, 464], size: [32, 144]),
    ]),"""
    return build_freight(rid, e, "THE NUMBER 9 FREIGHT", extra=ladders)


def rustler_head():
    """The head of the train: the flat car's end, the first box car, then the
    Rustler (the outlaw engine that has taken the train): its tender, its cab,
    its boiler and domes, the pilot beam over the rails. Off its front is
    Clinker Flats' yard."""
    rid = HEAD
    w, h = ROOMS_AT[rid][1]
    e = track_bed(w) + [
        edge("rustler_head_from_cars", "back along the train", 0, FLAT, CARS, "freight_cars_to_head"),
        car("flat_car_2_end", 0, 300, FLAT),
        solid("crate_step", 180, FLAT - 64, 80, 64),
        car("box_car_4", 364, 844, 480),
        entity("EnemySpawn", 605 - 37, 480 - 96, 74, 96, name=f"{rid}_multi_armed_bandit_0", brain="combatant",
               character_id="multi_armed_bandit", respawn="OnRoomReenter"),
        car("rustler_tender", 896, 1312, 528),
        ledge("tender_hatch", 1184, 480, 112),
        # Peyote Lean, the outlaw who rides with Marshal Gallus, keeps the
        # tender: he sees anyone who comes up the train, and shoots.
        entity("EnemySpawn", 1150 - 16, 528 - 48, 32, 48, name=f"{rid}_peyote_lean", brain="combatant",
               character_id="npc_peyote_lean", respawn="OnRoomReenter"),
        solid("rustler_cab_roof", 1312, 432, 240, 16),
        car("rustler_cab_floor", 1312, 1504, 528),
        entity("SurfaceChain", 1504, 496, 16, 16, name="rustler_footplate_ramp",
               points="1472,528; 1504,528; 1552,512; 1584,512", visual="none"),
        ledge("rustler_service_step", 1552, 464, 64),
        car("rustler_boiler", 1552, 2160, 512),
        solid("steam_dome", 1700, 464, 80, 48),
        solid("sand_dome", 1880, 472, 60, 40),
        solid("smokestack", 2040, 384, 60, 128),
        car("rustler_pilot", 2160, w, FLAT),
        start(rid, 120, FLAT),
        edge("rustler_head_to_yard", "jump off into the yard", w - WALL, FLAT, YARD, "yard_from_freight"),
    ]
    return build_freight(rid, e, "THE RUSTLER")


#: Clinker Flats' two levels, in the tall rooms' coordinates: the street (the
#: Row's, the pad's) and the works' floor, 768 over it.
FLATS_LOW = 1408
FLATS_HIGH = 640


def clinker_yard():
    """The loading dock and the two levels of the yard."""
    rid = YARD
    w, h = ROOMS_AT[rid][1]
    dock = FLATS_LOW - 32
    road_x0, road_x1 = 496, 2384
    hatch_y = 1024
    e = [
        solid("ground", 0, FLATS_LOW, w, h - FLATS_LOW),
        solid("dock", 0, dock, 448, FLATS_LOW - dock),
        solid("west_wall", 0, 0, WALL, dock - 96),
        solid("east_wall_mid", w - WALL, FLATS_HIGH + 16, WALL, FLATS_LOW - 96 - FLATS_HIGH - 16),
        solid("east_wall_top", w - WALL, 0, WALL, FLATS_HIGH - 96),
        edge("yard_from_freight", "back onto the freight", 0, dock, HEAD, "rustler_head_to_yard"),
        edge("yard_to_row", "on to the Row", w - WALL, FLATS_LOW, ROW, "row_from_yard"),
        edge("yard_to_works", "on to the works", w - WALL, FLATS_HIGH, WORKS, "works_from_yard"),
        start(rid, 200, dock),
        ramp("tipple_road", road_x0, FLATS_LOW, 1424, hatch_y),
        ledge("tipple_inspection_hatch", 1424, hatch_y, 32),
        ramp("tipple_road_east", 1456, hatch_y, road_x1, FLATS_HIGH),
        solid("tipple_floor", road_x1, FLATS_HIGH, w - road_x1, 16),
        ledge("tipple_inspection_landing", 1456, 1088, 144),
        # Lou Shunter, the yardmaster, on the dock.
        resident("npc_frontier_yardmaster", "frontier_yardmaster", 330, dock),
        sign("yard_sign_name", 300, dock - 300, "CLINKER FLATS. YARD LIMIT.", 320),
        sign("yard_sign_tipple", 1500, 900, "TIPPLE ROAD: TO THE WORKS", 300),
    ]
    ladder = "\n    intgrid: (climbable: [(kind: \"Ladder\", px: [1424, 976], size: [32, 432])]),"
    return build(rid, e, "CLINKER FLATS YARD", FLATS_MUSIC, dangerous=True, biome="frontier_works", extra=ladder)


def clinker_works():
    """The smelter floor and the crane's two gantries."""
    rid = WORKS
    w, h = ROOMS_AT[rid][1]
    floor = FLATS_HIGH
    e = [
        solid("works_floor", 0, floor, w, h - floor),
        *side_walls(w, h, floor, floor),
        edge("works_from_yard", "back to the yard", 0, floor, YARD, "yard_to_works"),
        edge("works_to_railhead", "on to the railhead", w - WALL, floor, RAILHEAD, "railhead_from_works"),
        start(rid, 100, floor),
        ledge("crane_loading_step", 608, floor - 64, 96),
        ledge("crane_gantry_west", 720, floor - 128, 464),
        ledge("crane_gantry_east", 1200, floor - 192, 368),
        chest("a pay packet left on the gantry", "currency:25", 1360, floor - 192),
        # Magda Ferro, the crane driver, at the foot of her crane.
        resident("npc_frontier_crane_driver", "frontier_crane_driver", 1700, floor),
        sign("works_sign_name", 400, floor - 320, "CLINKER FLATS SMELTER WORKS", 360),
        sign("works_sign_slag", 1100, floor - 300, "HOT SLAG. KEEP OFF THE POTS.", 320),
    ]
    ladder = "\n    intgrid: (climbable: [(kind: \"Ladder\", px: [1568, 416], size: [32, 224])]),"
    return build(rid, e, "THE SMELTER WORKS", FLATS_MUSIC, dangerous=True, biome="frontier_works", extra=ladder)


def clinker_row():
    """The shacks under the works: their roofs a jump up, the pump on a hump
    of cinders in the middle of the Row, washing on lines."""
    rid = ROW
    w, h = ROOMS_AT[rid][1]
    floor = RIM
    hump = floor - 64
    e = [
        solid("row", 0, floor, w, h - floor),
        *side_walls(w, h, floor, floor),
        edge("row_from_yard", "back to the yard", 0, floor, YARD, "yard_to_row"),
        edge("row_to_railhead", "on to the railhead", w - WALL, floor, RAILHEAD, "railhead_from_row"),
        start(rid, 100, floor),
        ledge("shack_roof_1", 240, floor - 112, 320),
        ledge("shack_roof_2", 600, floor - 96, 240),
        slope("cinders_up", 896, floor, 1104, hump),
        solid("cinders_top", 1104, hump, 192, floor - hump),
        slope("cinders_down", 1296, hump, 1504, floor),
        ledge("shack_roof_3", 1600, floor - 112, 280),
        ledge("shack_roof_4", 1960, floor - 96, 280),
        # Ida Soames, who does the Row's washing.
        resident("npc_frontier_laundress", "frontier_laundress", 1200, hump),
        sign("row_sign_name", 600, floor - 300, "THE ROW", 160),
        sign("row_sign_laundry", 1800, floor - 260, "WASHING DONE. SOOT NOT GUARANTEED OUT.", 420),
    ]
    return build(rid, e, "THE ROW", FLATS_MUSIC, dangerous=True, biome="frontier_works")


def clinker_railhead():
    """The line east to Dry Dock: the old tramway grade comes down from the
    works' level on trestles to the street, which goes on under it to Pad
    Three; a water tower, the line's signal."""
    rid = RAILHEAD
    w, h = ROOMS_AT[rid][1]
    grade_x0, grade_x1 = 288, 2128
    e = [
        solid("ground", 0, FLATS_LOW, w, h - FLATS_LOW),
        solid("west_wall_top", 0, 0, WALL, FLATS_HIGH - 96),
        solid("west_wall_mid", 0, FLATS_HIGH + 16, WALL, FLATS_LOW - 96 - FLATS_HIGH - 16),
        solid("east_wall", w - WALL, 0, WALL, FLATS_LOW - 96),
        edge("railhead_from_works", "back to the works", 0, FLATS_HIGH, WORKS, "works_to_railhead"),
        edge("railhead_from_row", "back to the Row", 0, FLATS_LOW, ROW, "row_to_railhead"),
        edge("railhead_to_pad", "east to Dry Dock", w - WALL, FLATS_LOW, PAD, "pad_from_railhead"),
        start(rid, 100, FLATS_LOW),
        solid("grade_head", 0, FLATS_HIGH, grade_x0, 16),
        ramp("tramway_grade", grade_x0, FLATS_HIGH, grade_x1, FLATS_LOW),
        sign("railhead_sign_line", 2200, FLATS_LOW - 200, "DRY DOCK AND THE PADS: EAST", 320),
        sign("railhead_sign_grade", 400, FLATS_HIGH - 120, "OLD TRAMWAY GRADE", 260),
    ]
    return build(rid, e, "CLINKER FLATS RAILHEAD", FLATS_MUSIC, dangerous=True, biome="frontier_works")


SLICE_ROOMS = (siding_station, siding_street, lie_down_inn, siding_trestle, sprocket_row, freight_tail, freight_cars,
               rustler_head, clinker_yard, clinker_works, clinker_row, clinker_railhead)

ROOMS = (landing_pad, main_street, wet_whistle, livery, refinery, ore_corral, saddle_lookout, hall_corral) + SLICE_ROOMS

#: The hall's door to its copy and the copy's life switch, on the hall's lower
#: floor between the T-rex's door and the Overflow's (`hall_of_bosses`,
#: `sandbox.ldtk`).
HALL_DOOR_YAML = f"""# The Hall of Bosses' door to its copy of Marshal Gallus's corral. Written by
# {GENERATOR}.
level_id: {HALL}
entities:
  - type: LoadingZone
    px: [1330, 384]
    size: [48, 96]
    fields:
      id: {HALL_DOOR}
      name: "to Marshal Gallus"
      activation: Door
      target_room: {HALL_CORRAL}
      target_zone: {HALL_CORRAL_ENTRY}
      bidirectional: true
  - type: Switch
    px: [1390, 448]
    size: [24, 32]
    fields:
      id: {HALL_SWITCH}
      name: "Marshal Gallus life switch"
      prompt: "Revive or defeat Marshal Gallus"
      target_encounter: {HALL_PLACEMENT}
      action: BossLife
"""


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
    # Nor has its SurfaceChain the `fill` field the slopes use (Hobford's
    # rooms added it to intro.ldtk the same way).
    code, out = run("def", "update-entity", "SurfaceChain", str(WORLD), "--add-field", "fill:Bool:false", "--in-place")
    if code and "already" not in out and "duplicate" not in out.lower():
        return code
    if code := make_rooms(WORLD, paths, keep_position="--relayout" not in argv):
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
