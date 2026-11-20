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
- `frontier_saddle_lookout`: the top of the east mesa, the beaten Marshal.
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

#: The Marshal's placement. His defeat is saved under this id, and it opens
#: the corral's grille (`boss.cleared <id>`).
PLACEMENT = "frontier.marshal_gallus"

BG = "#3A2418"
#: The rooms name the Frontier's cue; `music_cues.ron` binds each room to
#: its section (the town, the saloon, the refinery, the mesa top).
TOWN_MUSIC = "leaden_saddle"
SALOON_MUSIC = TOWN_MUSIC
REFINERY_MUSIC = TOWN_MUSIC

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
}

#: The street's floor, and the boardwalk one small step over it.
STREET = 640
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
        *side_walls(w, h, None, floor),
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
        # The stair to the balcony over the bar: a landing a jump up, then the
        # balcony a jump over it.
        ledge("whistle_stair", 672, floor - 80, 112),
        ledge("whistle_balcony", 240, balcony, 448),
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
        ledge("livery_ladder_rung", 464, floor - 64, 96),
        # Gus Bell, by the stalls.
        resident("npc_frontier_liveryman", "frontier_liveryman", 300, floor),
        ledge("livery_hayloft", 560, loft, w - WALL - 560),
        sign("livery_sign_rules", 300, 120, "MULES BY THE DAY. RETURN WITH THE SAME NUMBER OF LEGS.", 560),
    ]
    return build(rid, e, "BELL'S LIVERY", TOWN_MUSIC, biome="frontier_interior")


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
        # Over the tank terrace, the pipe rack's catwalk.
        ledge("pipe_rack_walk", 880, t1 - 128, 320),
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
    return build(rid, e, "THE REFINERY", REFINERY_MUSIC, dangerous=True, biome="frontier_refinery")


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
        chest("the gate tolls", "currency:150", 1340, top),
        sign("lookout_sign", 1100, top - 240, "THE LEADEN SADDLE: THE TOWN, THE PADS, THE PASS", 520),
    ]
    return build(rid, e, "THE MESA TOP", TOWN_MUSIC)


ROOMS = (landing_pad, main_street, wet_whistle, livery, refinery, ore_corral, saddle_lookout, hall_corral)

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
