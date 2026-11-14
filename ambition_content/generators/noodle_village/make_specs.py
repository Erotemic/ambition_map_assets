#!/usr/bin/env python3
"""Write the rooms of the Noodle dimension round the Noodly Temple: the
village of Brothlehem, the Pilgrims' Way up to the temple, and the road to
Mount Fizzuvius, the soda volcano.

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/noodle_village/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/noodle_village/make_specs.py --apply  # and makes the rooms

Run it from the repository root.

The flat map is a valley. The temple stands on the hill west of the
village, and the volcano stands on the east side. Brothlehem is between them,
in the floor of the valley, and it is the hub of the dimension: the gate ring
(ALDENTE) stands in its square.

                     [temple stair]--door--> noodly_narthex (the temple)
    [durum terraces]-'  (high)
           |  (low)
    [village square]==[village market]--[fizzy flats]--[Fizzuvius slopes]==[Fizzuvius caldera]
                         | door                         (the rim and the soda tube)
                     [curry house]

- `noodle_village_square`: the gate ring and its terminal, a shrine, the
  notice board. Richard Duckling studies the pilgrims.
- `noodle_village_market`: the drying racks, where the noodles hang to
  dry; their rails are the high road. Marie Curry's curry house is a door.
- `noodle_village_curry_house`: Marie Curry cooks curry udon, and she knows
  what the soda is.
- `noodle_durum_terraces`: fields of durum wheat (the wheat of pasta) on
  terraces, with paddies of broth. The low field climbs west, the high field
  climbs back east.
- `noodle_temple_stair`: the great stair to the temple's door.
- `noodle_fizzy_flats`: the soda springs at the foot of the volcano, and the
  hermit who lives by them.
- `noodle_fizzuvius_slopes`: the flank of the volcano: shelves of rock
  candy with channels of soda between them.
- `noodle_fizzuvius_caldera`: the crater: a lake of soda with corks that
  drift on it, a bubble lift, the rim path, and the Mint.

THE SODA. The volcano's liquid is soda, not lava. A pool of soda is two
things in one box: murky water (IntGrid `Water` value 2: a body sinks into
it slowly, and it hides what is under its surface) and a `DamageVolume` (the
carbonic acid stings: one damage and a knockback out of the pool). The name
of each volume has "acid" in it, so its hit plays the acid splash. Smoking
Mountain's lava is the same `DamageVolume`.

The village square, the market and the stair touch on the flat map and join
by their edges (`specs/check_flat_map.py noodle.ldtk`); the square and the
market join at two heights (the street and the roofs), so the village is a
loop. The volcano's slopes and caldera join at two heights (the rim, and
the soda tube under it), so the volcano is a loop. The temple and the curry
house are buildings: their ways in are doors. The narthex is LDtk-owned, so
its door to the stair is authored in the map, not here (the temple's
`make_specs.py` writes the same door).

Where a room is in the world is its LDtk editor's: `--apply` regenerates each
room where it stands (`area create --keep-position`), and `ROOMS_AT` places
only a room that is new. `--apply --relayout` puts every room back where
`ROOMS_AT` says.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_noodle_village_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))

from district_kit import (  # noqa: E402
    WALL, WORLDS, door, edge, entity, ledge, make_rooms, paint, resident, room, run, sign, solid, start,
)
import gates  # noqa: E402

#: The noodle dimension's world file: the temple's rooms are in it too.
WORLD_LDTK = WORLDS / "noodle.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/noodle_village/make_specs.py"

SQUARE = "noodle_village_square"
MARKET = "noodle_village_market"
CURRY = "noodle_village_curry_house"
TERRACES = "noodle_durum_terraces"
STAIR = "noodle_temple_stair"
FLATS = "noodle_fizzy_flats"
SLOPES = "noodle_fizzuvius_slopes"
CALDERA = "noodle_fizzuvius_caldera"

#: The temple's first room and the zone of its door to the stair (authored
#: in the narthex, which is LDtk-owned).
NARTHEX = "noodly_narthex"
NARTHEX_DOOR = "noodly_narthex_to_stair"

#: The dimension's gate ring (ALDENTE, `data/gate_network.ron`).
RING_LABEL = "Brothlehem Gate"
RING_ZONE = "noodle_village_gate"
RING_TERMINAL = "noodle_village_gate_terminal"

BIOME = "noodly"
BG = "#15131F"
VILLAGE_MUSIC = "pastafarian"
WAY_MUSIC = "ai_dente"
VOLCANO_MUSIC = "pasta_la_vista"
CRATER_MUSIC = "spaghetti_western"

#: The floor of the valley in the world: the walk line of the square, the
#: market, the flats and the foot of the terraces and of the slopes.
VALLEY = 2624
#: Each room: where it is in the world (its top left), and its size. The
#: temple's rooms are at y 0 to 1408 and x 70000 to 83000; the valley is
#: under them, west of them and under their west end.
ROOMS_AT = {
    TERRACES: ((64000, 1408), (1920, 1280)),
    STAIR: ((65920, 1024), (1920, 1024)),
    SQUARE: ((65920, 2048), (1920, 640)),
    MARKET: ((67840, 2048), (1920, 640)),
    CURRY: ((67840, 2880), (1024, 512)),
    FLATS: ((69760, 2112), (1920, 640)),
    SLOPES: ((71680, 1408), (1920, 1280)),
    CALDERA: ((73600, 1408), (1920, 1024)),
}


def local(rid, world_y):
    """`world_y` in the coordinates of the room `rid`."""
    return world_y - ROOMS_AT[rid][0][1]


def build(rid, entities, title, music, dangerous=False):
    at, size = ROOMS_AT[rid]
    return rid, room(rid, entities, at=at, size=size, biome=BIOME, music=music, bg=BG, title=title,
                     generator=GENERATOR, dangerous=dangerous)


def blurb(rid, text, x, y, w=620):
    """What the place is: a line under the title."""
    return sign(f"{rid}_blurb", x, y, text, w)


def ground(name, x0, x1, top, h):
    """Solid ground from `top` to the bottom of the room."""
    return solid(name, x0, top, x1 - x0, h - top)


def walls(rid, side, h, openings):
    """A side wall of the room, with an opening 96 high over each floor in
    `openings` (the side exits)."""
    _, (w, _) = ROOMS_AT[rid]
    x = 0 if side == "west" else w - WALL
    out, y = [], 0
    for n, floor in enumerate(sorted(openings)):
        if floor - 96 > y:
            out.append(solid(f"{side}_wall_{n}", x, y, WALL, floor - 96 - y))
        y = floor + 16
    return out


#: The soda pools: (room, x0, y0, x1, y1) of each, filled in `apply` (the
#: `Water` layer is painted after the rooms are made).
SODA = []
#: The broth: (room, x0, y0, x1, y1) of each paddy (clear water, harmless).
BROTH = []


def soda(rid, n, x0, y0, x1, y1):
    """A pool of soda: murky water (painted later) and the sting of its acid."""
    SODA.append((rid, x0, y0, x1, y1))
    return entity("DamageVolume", x0, y0, x1 - x0, y1 - y0, name=f"{rid} soda acid {n}", damage=1.0)


def broth(rid, x0, y0, x1, y1):
    BROTH.append((rid, x0, y0, x1, y1))


def noodling(rid, n, x, y):
    """A noodling, the monster's lesser appendage: it floats, and its box
    foot is at `y`."""
    return entity("EnemySpawn", x - 20, y - 40, 40, 40, name=f"{rid}_npc_fsm_noodling_{n}", brain="combatant",
                  character_id="npc_fsm_noodling", respawn="OnRoomReenter")


def spaghetti(rid, n, x, floor):
    return entity("EnemySpawn", x - 17, floor - 56, 34, 56, name=f"{rid}_npc_spaghetti_event_{n}",
                  brain="medium_striker", character_id="npc_spaghetti_event", respawn="OnRoomReenter")


def parrot(rid, n, x, y):
    return entity("EnemySpawn", x - 38, y - 60, 76, 60, name=f"{rid}_stochastic_parrot_{n}", brain="sky_parrot",
                  character_id="stochastic_parrot", respawn="OnRoomReenter")


def chest(name, reward, x, floor):
    return entity("ChestSpawn", x, floor - 58, 76, 58, name=name, reward=reward)


def raft(rid, n, x, y, w, sweep, speed):
    """A cork that drifts on the soda: a one-way platform that sweeps
    `sweep` px along and back."""
    return entity("MovingPlatform", x, y, w, 16, id=f"{rid}_cork_{n}", name=f"a cork {n}", sweep_dx=float(sweep),
                  speed=float(speed), one_way=True)


# ---------------------------------------------------------------- the village

#: The square: its street, and the roofs of its houses (x0, x1, ridge),
#: west to east. Each roof is 64 over the one before it and 80 from it.
SQUARE_FLOOR = local(SQUARE, VALLEY)
SQUARE_ROOFS = [("roof_cart", 880, 1000, 512), ("roof_baker", 1000, 1280, 448), ("roof_pilgrims_rest", 1360, 1640, 384),
                ("roof_bell_house", 1720, 1904, 320)]
#: The roads between the square and the market: the street and the roofs.
VILLAGE_HIGH = 320


def square():
    """BROTHLEHEM, THE GATE SQUARE. The ring stands at the west end, by the
    way out to the terraces. The houses' roofs step up east to the market's
    racks."""
    rid = SQUARE
    _, (w, h) = ROOMS_AT[rid]
    g = SQUARE_FLOOR
    ring = gates.ring(RING_LABEL, RING_ZONE, 128, g, "the gate")
    # The ring's picture is the scene's (the ring and the portal props).
    ring = [(t, x, y, ew, eh, dict(f, presentation="SceneArt") if t == "LoadingZone" else f) for t, x, y, ew, eh, f in ring]
    e = [
        ground("street", 0, w, g, h),
        *walls(rid, "west", h, [g]),
        *walls(rid, "east", h, [g, VILLAGE_HIGH]),
        edge("square_west", "out to the durum terraces", 0, g, TERRACES, "terraces_east_low"),
        edge("square_east_low", "along the street to the market", w - WALL, g, MARKET, "market_west_low"),
        edge("square_east_high", "over the roofs to the racks", w - WALL, VILLAGE_HIGH, MARKET, "market_west_high"),
        start(rid, 560, g),
        *gates.as_ron(ring),
        *gates.as_ron(gates.terminal(RING_LABEL, RING_TERMINAL, 440, g)),
        entity("ShrineSpawn", 600, g - 80, 44, 80, id=f"{rid}_shrine", name="the shrine of the square"),
        resident("npc_richard_duckling", "noodle_village_duckling", 780, g),
        *[ledge(name, x0, y, x1 - x0) for name, x0, x1, y in SQUARE_ROOFS],
        sign("square_sign_ring", 272, g - 330, "ALDENTE: the gate of Brothlehem", 360),
        sign("square_sign_board", 1180, g - 200, "WEST: the Pilgrims' Way, up to the Temple. EAST: the market, "
             "then Mount Fizzuvius. NO MINTS ON THE MOUNTAIN.", 560),
        sign("square_sign_rest", 1500, g - 110, "THE PILGRIMS' REST: full (it is always full)", 380),
    ]
    return build(rid, e + [blurb(rid, "A town of pilgrims under the hill of the Noodly Temple. Everyone here came "
                                 "to see Him. Most of them stayed for lunch.", w // 2, 72)],
                 "BROTHLEHEM: THE GATE SQUARE", VILLAGE_MUSIC)


#: The market's drying racks: rails where the noodles hang to dry, a road
#: over the street (x0, x1, y), west to east.
RACKS = [("rack_west", 16, 400, VILLAGE_HIGH), ("rack_crate", 380, 470, 512), ("rack_low", 300, 460, 448),
         ("rack_spaghetti", 480, 800, 384), ("rack_linguine", 880, 1200, 320), ("rack_lasagne", 1280, 1600, 256),
         ("rack_east", 1680, 1904, 320)]
CURRY_DOOR_X = 1360


def market():
    """BROTHLEHEM, THE DRYING RACKS. Long racks of noodles drying in the
    steam; their rails are the high road. The curry house is a door off the
    street. The street goes on east, out of town, to the soda springs."""
    rid = MARKET
    _, (w, h) = ROOMS_AT[rid]
    g = local(rid, VALLEY)
    e = [
        ground("street", 0, w, g, h),
        *walls(rid, "west", h, [g, VILLAGE_HIGH]),
        *walls(rid, "east", h, [g]),
        edge("market_west_low", "along the street to the square", 0, g, SQUARE, "square_east_low"),
        edge("market_west_high", "over the racks to the roofs", 0, VILLAGE_HIGH, SQUARE, "square_east_high"),
        edge("market_east", "out of town, to the soda springs", w - WALL, g, FLATS, "flats_west"),
        start(rid, 120, g),
        *[ledge(name, x0, y, x1 - x0) for name, x0, x1, y in RACKS],
        door("market_curry_door", "into the curry house", CURRY_DOOR_X, g, CURRY, "curry_door"),
        sign("market_sign_curry", CURRY_DOOR_X + 24, g - 200, "THE CURRY HOUSE: M. Curry, prop. Radiantly hot.", 420),
        sign("market_sign_racks", 640, g - 120, "FRESH NOODLES. DRYING NOODLES. NOODLES OF UNCERTAIN AGE.", 520),
        sign("market_sign_out", 1760, g - 150, "TO THE SPRINGS. Bring a towel.", 260),
        chest("the racks' best", "currency:60", 1400, 256),
    ]
    return build(rid, e + [blurb(rid, "The market of Brothlehem, where the noodles hang to dry. Climbing on the "
                                 "racks is not allowed. The racks are the only way to the roofs.", w // 2, 72)],
                 "BROTHLEHEM: THE DRYING RACKS", VILLAGE_MUSIC)


def curry_house():
    """Marie Curry's curry house. She cooks curry udon, and she knows what
    the soda of the volcano is: carbonic acid."""
    rid = CURRY
    _, (w, h) = ROOMS_AT[rid]
    g = 448
    e = [
        ground("floor", 0, w, g, h),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 32),
        door("curry_door", "out to the market", 40, g, MARKET, "market_curry_door"),
        start(rid, 150, g),
        ledge("counter", 520, g - 64, 240),
        ledge("spice_shelf", 800, g - 160, 192),
        resident("npc_marie_curry", "noodle_village_curry", 440, g),
        sign("curry_sign_menu", 640, 96, "TODAY: curry udon. TOMORROW: udon curry.", 420),
        chest("the tip jar", "currency:25", 860, g - 160),
        entity("PickupSpawn", 623, g - 64 - 34 - 4, 34, 34, name="a bowl of curry udon", kind="health:2", respawn="Never"),
    ]
    return build(rid, e, "THE CURRY HOUSE", VILLAGE_MUSIC)


# ------------------------------------------------------- the Pilgrims' Way

#: The terraces: the low field climbs west from the square in steps of 64
#: (x0, x1, top); the high field (one-way ledges) climbs back east to the
#: threshing floor, level with the foot of the stair.
TERRACES_LOW = [(1536, 1920, 1216), (1152, 1536, 1152), (768, 1152, 1088), (384, 768, 1024), (0, 384, 960)]
TERRACES_HIGH_EDGE = 256
#: The fields of the low field that hold a paddy of broth.
PADDY_FIELDS = (1, 3)


def terraces():
    """THE DURUM TERRACES. Durum wheat, the wheat of pasta, on terraces up
    the temple's hill; paddies of broth water the low field. The low field
    climbs west from the square; the high field climbs back east to the
    threshing floor and the way up to the stair."""
    rid = TERRACES
    _, (w, h) = ROOMS_AT[rid]
    low = local(rid, VALLEY)
    e = []
    for n, (x0, x1, top) in enumerate(TERRACES_LOW):
        if n in PADDY_FIELDS:
            # A paddy of broth: a shallow pit in the middle of the field.
            p0, p1 = x0 + 96, x1 - 96
            e += [ground(f"field_{n}_west", x0, p0, top, h), ground(f"paddy_{n}_bed", p0, p1, top + 64, h),
                  ground(f"field_{n}_east", p1, x1, top, h)]
            broth(rid, p0, top + 16, p1, top + 64)
        else:
            e.append(ground(f"field_{n}", x0, x1, top, h))
    # The high field: lasagne terraces, each 64 over the one before it.
    for n in range(11):
        e.append(ledge(f"terrace_{n}", 32 + 160 * n, 896 - 64 * n, 192))
    e += [
        solid("threshing_floor", 1792, TERRACES_HIGH_EDGE, w - 1792, 32),
        *walls(rid, "east", h, [low, TERRACES_HIGH_EDGE]),
        solid("west_wall", 0, 0, WALL, TERRACES_LOW[-1][2]),
        edge("terraces_east_low", "down to Brothlehem", w - WALL, low, SQUARE, "square_west"),
        edge("terraces_east_high", "up to the temple stair", w - WALL, TERRACES_HIGH_EDGE, STAIR, "stair_west"),
        start(rid, 1800, low),
        sign("terraces_sign_paddy", 1344, 1040, "BROTH PADDIES. Wade if you must. Do not drink the irrigation.", 520),
        sign("terraces_sign_wheat", 560, 920, "DURUM WHEAT: hard, like the temple's doors", 420),
        sign("terraces_sign_mill", 1600, 150, "THE THRESHING FLOOR. The semolina mill is closed for prayer.", 440),
        chest("a gleaner's sack", "currency:40", 1810, TERRACES_HIGH_EDGE),
        noodling(rid, 1, 900, 720),
        noodling(rid, 2, 1400, 560),
    ]
    return build(rid, e + [blurb(rid, "The fields of the temple's hill. Pasta begins as wheat; the pilgrims "
                                 "begin as tourists.", w // 2, 72)],
                 "THE PILGRIMS' WAY: THE DURUM TERRACES", WAY_MUSIC, dangerous=True)


#: The stair: its foot (level with the threshing floor), the steps of the
#: great stair (each 64 up and 128 along), and the landing at the door.
STAIR_FOOT = local(STAIR, ROOMS_AT[TERRACES][0][1] + TERRACES_HIGH_EDGE)
STAIR_X0, STAIR_RUN, STAIR_RISE, STAIR_STEPS = 480, 128, 64, 6
STAIR_DOOR_X = 1720


def stair():
    """THE TEMPLE STAIR. The great stair up the last of the hill, to the
    door of the Noodly Temple."""
    rid = STAIR
    _, (w, h) = ROOMS_AT[rid]
    foot = STAIR_FOOT
    landing = foot - STAIR_RISE * STAIR_STEPS
    e = [ground("foot", 0, STAIR_X0, foot, h)]
    for n in range(STAIR_STEPS):
        x0 = STAIR_X0 + STAIR_RUN * n
        e.append(ground(f"step_{n}", x0, x0 + STAIR_RUN, foot - STAIR_RISE * (n + 1), h))
    landing_x = STAIR_X0 + STAIR_RUN * STAIR_STEPS
    e += [
        ground("landing", landing_x, w, landing, h),
        *walls(rid, "west", h, [foot]),
        solid("east_wall", w - WALL, 0, WALL, landing),
        edge("stair_west", "down to the terraces", 0, foot, TERRACES, "terraces_east_high"),
        door("noodle_temple_stair_door", "into the Noodly Temple", STAIR_DOOR_X, landing, NARTHEX, NARTHEX_DOOR),
        start(rid, 200, foot),
        sign("stair_sign_door", STAIR_DOOR_X - 60, landing - 170, "THE NOODLY TEMPLE. Colanders may be worn.", 400),
        sign("stair_sign_steps", 860, landing - 40, "Mind the steps. They are al dente.", 360),
        parrot(rid, 1, 1100, 260),
    ]
    return build(rid, e + [blurb(rid, "The last of the hill, and the door of the temple of the Flying Spaghetti "
                                 "Monster. The pilgrims climb it on their knees; you may walk.", w // 2, 72)],
                 "THE PILGRIMS' WAY: THE TEMPLE STAIR", WAY_MUSIC, dangerous=True)


# ------------------------------------------------------- Mount Fizzuvius

FLATS_FLOOR = local(FLATS, VALLEY)
#: The springs: pits in the floor of the flats (x0, x1), each full of soda
#: from 16 under the floor to its bed.
SPRINGS = [(560, 720), (1000, 1200), (1400, 1520)]
SPRING_BED = FLATS_FLOOR + 96


def flats():
    """THE FIZZY FLATS. The foot of Mount Fizzuvius, where the soda comes
    up through the ground in springs. A rock-candy stone stands in the
    widest spring. The hermit lives by the first."""
    rid = FLATS
    _, (w, h) = ROOMS_AT[rid]
    g = FLATS_FLOOR
    e, x = [], 0
    for n, (x0, x1) in enumerate(SPRINGS):
        e.append(ground(f"crust_{n}", x, x0, g, h))
        e.append(ground(f"spring_{n}_bed", x0, x1, SPRING_BED, h))
        e.append(soda(rid, n, x0, g + 16, x1, SPRING_BED))
        x = x1
    e += [
        ground(f"crust_{len(SPRINGS)}", x, w, g, h),
        solid("candy_stone", 1084, g, 32, SPRING_BED - g),
        *walls(rid, "west", h, [g]),
        *walls(rid, "east", h, [g]),
        edge("flats_west", "back to Brothlehem", 0, g, MARKET, "market_east"),
        edge("flats_east", "up the mountain", w - WALL, g, SLOPES, "slopes_west"),
        start(rid, 120, g),
        resident("npc_weird_hermit", "noodle_fizzy_hermit", 330, g),
        sign("flats_sign_hermit", 330, g - 150, "HERMITAGE. No mints. No visitors. (One visitor.)", 420),
        sign("flats_sign_spring", 640, g - 110, "SODA SPRING. FIZZY. Do not drink, do not swim, do not add mints.", 520),
        noodling(rid, 1, 1100, g - 120),
        noodling(rid, 2, 1460, g - 160),
    ]
    return build(rid, e + [blurb(rid, "The foot of Mount Fizzuvius. The ground is a crust of sugar, and under it the "
                                 "mountain is carbonated.", w // 2, 72)],
                 "MOUNT FIZZUVIUS: THE FIZZY FLATS", VOLCANO_MUSIC, dangerous=True)


#: The slopes: shelves of rock candy east and up (x0, x1, top), with a
#: channel of soda between two pairs of them (x0, x1, surface, bed).
SLOPE_SHELVES = [(0, 320, 1216), (320, 576, 1152), (704, 960, 1088), (960, 1216, 1024), (1344, 1600, 960),
                 (1600, 1760, 896), (1760, 1920, 832)]
SLOPE_CHANNELS = [(576, 704, 1168, 1248), (1216, 1344, 1040, 1120)]
#: The two joins to the caldera: the rim and the soda tube.
RIM = 320
TUBE = 832
#: The upper slope: rock candy outcrops (x0, y), each 160 wide: west from
#: the tube's shelf, then east up to the rim.
SLOPE_OUTCROPS = [(1600, 768), (1408, 704), (1216, 640), (1024, 576), (1216, 512), (1408, 448), (1600, 384)]


def slopes():
    """THE SLOPES OF FIZZUVIUS. The flank of the volcano: shelves of rock
    candy, and the soda that runs down between them in channels. The low
    road ends at the soda tube into the caldera; the outcrops above it
    climb back west and then up to the rim."""
    rid = SLOPES
    _, (w, h) = ROOMS_AT[rid]
    e = [ground(f"shelf_{n}", x0, x1, top, h) for n, (x0, x1, top) in enumerate(SLOPE_SHELVES)]
    for n, (x0, x1, surface, bed) in enumerate(SLOPE_CHANNELS):
        e += [ground(f"channel_{n}_bed", x0, x1, bed, h), soda(rid, n, x0, surface, x1, bed)]
    e += [ledge(f"outcrop_{n}", x, y, 160) for n, (x, y) in enumerate(SLOPE_OUTCROPS)]
    e += [
        solid("rim_shelf", 1760, RIM, w - 1760, 32),
        *walls(rid, "west", h, [SLOPE_SHELVES[0][2]]),
        *walls(rid, "east", h, [RIM, TUBE]),
        edge("slopes_west", "down to the springs", 0, SLOPE_SHELVES[0][2], FLATS, "flats_east"),
        edge("slopes_east_tube", "into the soda tube", w - WALL, TUBE, CALDERA, "caldera_west_tube"),
        edge("slopes_east_rim", "over the rim", w - WALL, RIM, CALDERA, "caldera_west_rim"),
        start(rid, 120, SLOPE_SHELVES[0][2]),
        sign("slopes_sign_danger", 640, 1000, "DANGER: CARBONATED", 260),
        sign("slopes_sign_mint", 1100, 360, "FIZZUVIUS has slept for a thousand years. Someone took the mint out.", 560),
        chest("a pilgrim's lost thermos", "health:2", 1044, 576),
        spaghetti(rid, 1, 1080, 1024),
        spaghetti(rid, 2, 1480, 960),
        parrot(rid, 1, 700, 500),
    ]
    return build(rid, e + [blurb(rid, "The flank of the soda volcano. The rock is rock candy; the streams are not "
                                 "water.", w // 2, 72)],
                 "MOUNT FIZZUVIUS: THE SLOPES", VOLCANO_MUSIC, dangerous=True)


#: The caldera: the west rim, the shore at the tube, the lake of soda
#: (x0, x1, surface, bed), the east shore, the east rim and the crust over
#: the lake (x0, y), each 160 wide.
LAKE = (400, 1520, TUBE + 16, 992)
EAST_RIM_X0 = 1680
CRUST = [(408, 320), (656, 352), (904, 320), (1152, 352), (1400, 320)]
#: The bubble lift stands between the last crust and the east rim, so that
#: it rises through nothing.
LIFT_X = 1568


def caldera():
    """THE CALDERA OF FIZZUVIUS. A lake of soda in the crater. Corks drift
    on it; a bubble lift on the east shore rises when it is stood on; the
    rim path goes back over the lake on the crust. The Mint is on the east
    rim."""
    rid = CALDERA
    _, (w, h) = ROOMS_AT[rid]
    x0, x1, surface, bed = LAKE
    e = [
        ground("west_shore", 0, x0, TUBE, h),
        ground("lake_bed", x0, x1, bed, h),
        soda(rid, 0, x0, surface, x1, bed),
        ground("east_shore", x1, w, TUBE, h),
        solid("west_rim", 0, RIM, 320, 32),
        ledge("east_rim", EAST_RIM_X0, RIM, w - WALL - EAST_RIM_X0),
        *[ledge(f"crust_{n}", x, y, 160) for n, (x, y) in enumerate(CRUST)],
        *walls(rid, "west", h, [RIM, TUBE]),
        solid("east_wall", w - WALL, 0, WALL, TUBE),
        edge("caldera_west_rim", "back over the rim", 0, RIM, SLOPES, "slopes_east_rim"),
        edge("caldera_west_tube", "back through the soda tube", 0, TUBE, SLOPES, "slopes_east_tube"),
        start(rid, 160, TUBE),
        raft(rid, 1, 440, surface - 24, 96, 200, 60),
        raft(rid, 2, 760, surface - 24, 96, 240, 75),
        raft(rid, 3, 1120, surface - 24, 96, 240, 90),
        # The bubble lift: it rests on the shore, and the fizz carries a body
        # that stands on it up to the east rim.
        entity("MovingPlatform", LIFT_X, TUBE - 16, 96, 16, id=f"{rid}_bubble_lift", name="the bubble lift",
               lift_dy=float(RIM - (TUBE - 16)), speed=150.0, one_way=True),
        sign("caldera_sign_lake", 960, surface - 150, "THE LAKE OF FIZZUVIUS. Corks float. You do not.", 460),
        sign("caldera_sign_lift", LIFT_X + 48, TUBE - 120, "BUBBLE LIFT: stand still and think fizzy thoughts", 420),
        sign("caldera_sign_mint", 1740, RIM - 140, "THE MINT. It plugged the vent for a thousand years. Please do "
             "not put it back.", 300),
        chest("the Mint of Fizzuvius", "currency:250", 1780, RIM),
        noodling(rid, 1, 700, surface - 120),
        noodling(rid, 2, 1200, surface - 200),
        parrot(rid, 1, 960, 260),
    ]
    return build(rid, e + [blurb(rid, "The crater of the soda volcano: a lake of soda, still fizzing from the last "
                                 "eruption. Mind the corks.", w // 2, 72)],
                 "MOUNT FIZZUVIUS: THE CALDERA", CRATER_MUSIC, dangerous=True)


ROOMS = (square, market, curry_house, terraces, stair, flats, slopes, caldera)


def main(argv):
    made = []
    SODA.clear()
    BROTH.clear()
    for make in ROOMS:
        rid, text = make()
        path = SPEC_OUT / f"{rid}.ron"
        path.write_text(text)
        made.append(path)
        print(path)
    if "--apply" not in argv:
        return 0
    keep = "--relayout" not in argv
    if code := make_rooms(WORLD_LDTK, made, keep_position=keep, overwrite_hand_edits="--overwrite-hand-edits" in argv):
        return code
    # The liquids: soda is murky (2), broth is clear (1).
    for value, pools in ((2, SODA), (1, BROTH)):
        for rid, x0, y0, x1, y1 in pools:
            if code := paint(WORLD_LDTK, rid, "Water", value, x0, y0, x1 - x0, y1 - y0):
                return code
    code, _ = run("validate", str(WORLD_LDTK))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
