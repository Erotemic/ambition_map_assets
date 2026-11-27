#!/usr/bin/env python3
"""Write the Elemental Mine and its local passages in science.ldtk."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "ambition_ldtk_tools" / "specs"))

from district_kit import (WALL, WORLDS, breakable_wall, door, edge, entity, ledge, make_rooms,
                          prop, resident, room, sign, solid, start, water)

WORLD = WORLDS / "science.ldtk"
OWNER = "game/ambition_map_assets/ambition_content/generators/elemental_mine/make_specs.py"
YARD = "science_mine_yard"
SHAFT = "science_mine_shaft"
ASSAY = "science_mine_assay"
VENT = "science_mine_vent"
BASIN = "science_mine_basin"
POCKET = "science_mine_pocket"
LOWER = "science_mine_lower"
LODE = "science_mine_lode"
RELIEF = "elemental_mine_relief"
RETURN = "elemental_mine_service_release"
BOSS = "elemental_mine.mother_lode"

ROOMS_AT = {
    YARD: ((-4672, 6880), (2112, 832)),
    SHAFT: ((-4768, 7712), (1536, 1664)),
    ASSAY: ((-3232, 7712), (1856, 640)),
    VENT: ((-6496, 8224), (1728, 736)),
    BASIN: ((-6560, 8960), (1792, 784)),
    POCKET: ((-7808, 9024), (1248, 608)),
    LOWER: ((-4768, 9376), (1840, 720)),
    LODE: ((-7072, 10096), (2304, 896)),
}


def build(rid, name, entities, *, deep=False, danger=False, extra="", zoom=None):
    at, size = ROOMS_AT[rid]
    surface = rid == YARD
    if not surface:
        extra += '\n    map_path: "The Elemental Mine",'
        extra += '\n    darkness: 35, ambient: "#121b25",' if deep else '\n    darkness: 18, ambient: "#132027",'
    theme = "eureka" if surface else ("mine_lode" if deep else "mine_cut")
    return rid, room(rid, entities, at=at, size=size, biome=theme, parallax_theme=theme,
                     music="scaling_laws" if surface else ("vault_in_the_dark" if deep else "graphite_and_rain"),
                     bg="#a9d3f0" if surface else "#1c262c", title=name, generator=OWNER,
                     zoom=zoom, extra=extra, dangerous=danger)


def shell(w, h):
    return [solid("roof", 0, 0, w, 64), solid("west_wall", 0, 0, WALL, h),
            solid("east_wall", w - WALL, 0, WALL, h)]


def floor(w, y, h):
    return solid("floor", 0, y, w, h - y)


def scene(kind, x, g, w, h, name=None):
    return prop(name or f"{kind}_{x}_{g}", kind, x, g - h, w, h)


def light(name, x, y, radius=256, color="#f6c78f"):
    return entity("LightSource", x - 16, y - 16, 32, 32, name=name, radius=float(radius), color=color, intensity=0.82)


def power(id, x, g, name):
    return entity("Switch", x, g - 36, 32, 36, id=id, name=name, prompt=f"Pull {name}", action="ToggleFlag")


def screen(id, x, g, name, condition):
    return [solid(f"{id}_lintel", x, 64, 48, g - 112 - 64),
            entity("LockWall", x, g - 112, 48, 112, id=id, name=name, gated_by=condition,
                   look="mine_lock_screen")]


def enemy(id, character, x, feet, w, h):
    return entity("EnemySpawn", x - w // 2, feet - h, w, h, name=id, character_id=character,
                  respawn="OnRoomReenter")


def chest(x, g, name, coins):
    return entity("ChestSpawn", x, g - 58, 76, 58, name=name, reward=f"currency:{coins}")


def checkpoint(rid, x, g, name):
    return entity("ShrineSpawn", x, g - 80, 44, 80, id=f"{rid}_shrine", name=name)


def carrier(id, name, look, w, a, b, speed):
    x, y = a
    return [entity("KinematicPath", x, y, 32, 32, id=f"{id}_road", name=f"{name} path",
                   points=f"{x},{y};{b[0]},{b[1]}", speed=float(speed), mode="PingPong"),
            entity("MovingPlatform", x - w // 2, y - 12, w, 24, id=id, name=name,
                   path_id=f"{id}_road", visual=look, one_way=True)]


def yard():
    g, w, h = 704, 2112, 832
    e = [
        floor(w, g, h), solid("west_cut", 0, 0, WALL, g),
        solid("east_cut_head", w - WALL, 0, WALL, g - 112),
        edge("mine_yard_to_range", "east to the Eureka Test Range", w - WALL, g,
             "eureka_test_range", "range_to_mine", h=112),
        scene("mine_headframe", 160, g, 448, 348),
        scene("mine_hopper", 700, g, 322, 222),
        scene("mine_rail", 1040, g, 520, 48),
        scene("mine_rack", 1420, g, 218, 104),
        door("yard_to_shaft", "take the pit stair", 342, g, SHAFT, "shaft_to_yard"),
        resident("npc_mine_foreman", "mine_foreman", 610, g, brain="stand_still"),
        resident("npc_mine_hand", "mine_hand", 1176, g, brain="townsfolk_roam"),
        resident("npc_mine_geologist", "mine_geologist", 1620, g, brain="stand_still"),
        sign("yard_board", 1328, g - 140, "ORE YARD · WEIGH EACH LOAD BEFORE DUMPING", 470),
        sign("yard_close", 390, g - 201, "DEEP SHIFT SUSPENDED. THE YARD IS OPEN.", 460),
        start(YARD, 1920, g),
    ]
    return build(YARD, "THE ELEMENTAL MINE: ORE YARD", e, zoom=0.82)


def shaft():
    w, h, top, middle, bottom = 1536, 1664, 256, 832, 1536
    ladder = '\n    intgrid: (climbable: [(kind: "Ladder", px: [96, 240], size: [48, 1296])]),'
    e = [
        *shell(w, h), floor(w, bottom, h),
        ledge("pithead_landing", 16, top, 640),
        ledge("vent_landing", 16, middle, 640),
        ledge("middle_rail", 880, middle, 448),
        door("shaft_to_yard", "back to the ore yard", 272, top, YARD, "yard_to_shaft"),
        door("shaft_to_assay", "to the assay gallery", 506, top, ASSAY, "assay_to_shaft"),
        door("shaft_to_vent", "to the ventilation drift", 488, middle, VENT, "vent_to_shaft"),
        door("shaft_to_basin", "to the settling basin", 310, bottom, BASIN, "basin_to_shaft"),
        door("shaft_to_lower", "to the lower workings", 1264, bottom, LOWER, "lower_to_shaft"),
        *carrier("mine_cage", "the shaft cage", "mine_cage", 224, (768, top + 12),
                 (768, bottom + 12), 208),
        scene("mine_headframe", 613, 530, 310, 300),
        scene("mine_brace", 867, 828, 202, 298),
        scene("mine_brace", 990, bottom, 256, 362),
        scene("mine_lamp", 411, 156, 42, 70),
        scene("mine_lamp", 552, 752, 42, 70),
        scene("mine_lamp", 1060, 1385, 42, 70),
        sign("cage_sign", 610, 115, "SHAFT CAGE", 205),
        sign("shaft_air_sign", 635, middle - 172, "VENTILATION LEVEL", 240),
        sign("shaft_ladder_sign", 175, 682, "FIXED LADDER", 175),
        light("shaft_head_lamp", 510, 150), light("shaft_vent_lamp", 482, 745),
        light("shaft_bottom_lamp", 1024, 1380, 320), start(SHAFT, 414, top),
    ]
    return build(SHAFT, "THE MAIN SHAFT", e, extra=ladder, zoom=0.84)


def assay():
    w, h, g = 1856, 640, 512
    e = [
        *shell(w, h), floor(w, g, h),
        door("assay_to_shaft", "back to the shaft", 80, g, SHAFT, "shaft_to_assay"),
        door("assay_to_basin", "down the sample chute stairs", 1424, g, BASIN, "basin_to_assay"),
        door("assay_to_lower", "down the service stairs", 1752, g, LOWER, "lower_to_assay"),
        resident("npc_mine_sampler", "mine_sampler", 332, g, brain="stand_still"),
        scene("mine_rack", 260, g, 200, 100),
        scene("mine_lamp", 351, 366, 44, 75),
        scene("mine_air_line", 695, 296, 704, 72),
        solid("assay_screen", 610, 64, 48, 336), ledge("assay_first_step", 688, g - 48, 124),
        ledge("assay_bench", 824, g - 96, 206), ledge("assay_second_step", 1040, g - 48, 144),
        scene("mine_bismuth", 885, g - 96, 134, 92),
        enemy("assay_bismuth", "bismuth_elemental", 1045, g, 58, 78),
        *screen("mine_service_screen", 1648, g, "the service stair screen", f"world.switch_on {RETURN}"),
        light("assay_bench_lamp", 326, 370), light("assay_shelf_lamp", 914, 324),
        sign("assay_label", 388, 310, "SAMPLE COUNTER. PLEASE DO NOT LICK THE SAMPLES.", 510),
        start(ASSAY, 184, g),
    ]
    return build(ASSAY, "THE ASSAY GALLERY", e, danger=True)


def vent():
    w, h, g = 1728, 736, 608
    e = [
        *shell(w, h), floor(w, g, h),
        door("vent_to_shaft", "back to the shaft", 1512, g, SHAFT, "shaft_to_vent"),
        door("vent_to_basin", "to the settling basin", 96, g, BASIN, "basin_to_vent"),
        power(RELIEF, 225, g, "the deep relief lever"),
        scene("mine_fan", 178, g, 196, 214),
        scene("mine_fan", 1432, g, 196, 214),
        scene("mine_air_line", 605, 333, 623, 72),
        scene("mine_lamp", 250, 463, 47, 75),
        ledge("intake_step", 1112, g - 48, 106), ledge("intake_walk", 854, g - 96, 270),
        ledge("exhaust_step", 735, g - 48, 120),
        solid("low_exhaust", 478, 64, 120, g - 64 - 112),
        enemy("vent_argon", "argon_elemental", 1256, g - 44, 48, 58),
        enemy("vent_bromine", "bromine_elemental", 640, g, 58, 64),
        light("vent_intake_lamp", 1430, 466, 220, "#99d7f5"),
        light("vent_relief_lamp", 267, 470, 242),
        sign("relief_board", 332, g - 145, "DEEP RELIEF · OPENS THE LOWER WORKINGS SCREEN", 470),
        start(VENT, 1390, g),
    ]
    return build(VENT, "THE VENTILATION DRIFT", e, danger=True)


def basin():
    w, h, g, bottom = 1792, 784, 512, 720
    e = [
        *shell(w, h), floor(w, bottom, h),
        solid("west_bank", 0, g, 416, bottom - g),
        solid("east_bank", 1328, g, w - 1328, bottom - g),
        solid("sediment_island", 768, 640, 232, 80),
        water("mine_settling_pool", 416, 608, 912, 112),
        *[ledge(f"bank_step_{i}", x, y, width) for i, (x, y, width) in enumerate([
            (416, 568, 112), (486, 624, 117), (554, 680, 123),
            (1078, 680, 123), (1152, 624, 112), (1220, 568, 108),
        ])],
        door("basin_to_vent", "up to the vents", 112, g, VENT, "vent_to_basin"),
        door("basin_to_pocket", "inspect the old sample stope", 286, g, POCKET, "pocket_to_basin"),
        door("basin_to_shaft", "back to the shaft bottom", 1488, g, SHAFT, "shaft_to_basin"),
        door("basin_to_assay", "up the sample stairs", 1648, g, ASSAY, "assay_to_basin"),
        *carrier("mine_ore_cart", "the ore shuttle", "mine_ore_cart", 192, (469, 476), (1270, 476), 172),
        scene("mine_rail", 374, g + 12, 1040, 34),
        scene("mine_lamp", 358, 380, 48, 78),
        scene("mine_lamp", 1433, 380, 48, 78),
        scene("mine_silver_vein", 800, 640, 188, 120),
        enemy("basin_mercury", "mercury_elemental", 889, 640, 62, 68),
        light("basin_rail_lamp", 362, 380), light("basin_metal_lamp", 885, 558, 200, "#bce3ee"),
        sign("basin_rail_board", 411, 321, "ORE SHUTTLE · KEEP CLEAR OF THE BANK BELOW", 460),
        start(BASIN, 1456, g),
    ]
    return build(BASIN, "THE SETTLING BASIN", e, danger=True)


def pocket():
    w, h, g = 1248, 608, 480
    e = [
        *shell(w, h), floor(w, g, h),
        door("pocket_to_basin", "out to the settling basin", 1008, g, BASIN, "basin_to_pocket"),
        solid("pocket_rock_lintel", 510, 64, 48, 304),
        breakable_wall("mine_sample_wall", 510, 368, 48, 112, hp=3, name="the cracked seam"),
        scene("mine_bismuth", 200, g, 272, 178),
        scene("mine_brace", 596, g, 200, 260),
        chest(192, g, "the old crew's sample locker", 24),
        sign("pocket_etching", 340, 255, "SHIFT 18 · LEFT A LITTLE FOR THE NEXT CREW", 400),
        light("pocket_lamp", 405, 352, 196, "#a2d6e9"), start(POCKET, 952, g),
    ]
    return build(POCKET, "THE OLD SAMPLE STOPE", e, deep=True)


def lower():
    w, h, g = 1840, 720, 592
    e = [
        *shell(w, h), floor(w, g, h),
        door("lower_to_shaft", "up to the shaft", 96, g, SHAFT, "shaft_to_lower"),
        *screen("mine_deep_screen", 456, g, "the deep relief screen", f"world.switch_on {RELIEF}"),
        ledge("deep_cart_spur", 728, g - 48, 272),
        enemy("lower_uranium", "uranium_elemental", 1008, g, 72, 94),
        scene("mine_silver_vein", 791, g - 48, 180, 118),
        scene("mine_brace", 468, g, 165, 258),
        scene("mine_lamp", 1472, 432, 48, 78),
        scene("mine_bismuth", 1390, g, 174, 124),
        power(RETURN, 1322, g, "the service stair release"),
        door("lower_to_assay", "up the service stairs to the assay gallery", 1412, g, ASSAY, "assay_to_lower",
             bidirectional=True),
        checkpoint(LOWER, 1540, g, "the last refuge bench"),
        door("lower_to_lode", "down to the listening cavern", 1712, g, LODE, "lode_to_lower"),
        light("lower_lintel_lamp", 423, 430), light("lower_vein_lamp", 928, 434, 225, "#a6c998"),
        light("last_bench_lamp", 1540, 438, 245),
        sign("deep_screen_record", 316, g - 149, "SCREEN OPENS AT THE VENT RELIEF", 350),
        sign("deep_last_sign", 1520, g - 165, "LAST REFUGE. STEPS ONLY BEYOND THIS POINT.", 470),
        start(LOWER, 198, g),
    ]
    return build(LOWER, "THE LOWER WORKINGS", e, deep=True, danger=True)


def lode():
    w, h, g = 2304, 896, 720
    e = [
        *shell(w, h), floor(w, g, h),
        solid("ledge_by_entry", 16, 656, 320, 64),
        ledge("entry_step", 336, 688, 124),
        ledge("west_crystal_shelf", 512, g - 56, 184),
        ledge("east_crystal_shelf", 1456, g - 56, 160),
        solid("cavern_west_crown", 160, 64, 440, 96),
        solid("cavern_west_eave", 0, 160, 336, 48),
        solid("cavern_east_crown", 1520, 64, 240, 144),
        solid("cavern_east_shoulder", 1376, 64, 144, 64),
        solid("cavern_far_eave", 1904, 64, 400, 128),
        scene("mine_lode_echo", 383, g, 162, 196),
        scene("mine_lode_echo", 1412, g, 179, 220),
        door("lode_to_lower", "up to the lower workings", 92, 656, LOWER, "lower_to_lode"),
        scene("mine_bismuth", 487, g, 226, 168),
        scene("mine_silver_vein", 980, g, 336, 208),
        scene("mine_bismuth", 1490, g, 212, 195),
        light("lode_threshold_light", 380, 530, 310),
        light("lode_blue_reflection", 1112, 514, 420, "#afdef6"),
        light("lode_crown_reflection", 1455, 540, 300, "#d2abc8"),
        entity("BossSpawn", 1012, g - 136, 148, 136, name="Mother Lode", brain="PhaseScript:mother_lode",
               encounter_id=BOSS),
        *screen("mine_listening_screen", 1712, g, "the fractured seam", f"boss.cleared {BOSS}"),
        entity("NpcSpawn", 1920, g - 120, 152, 120, character_id="npc_mine_lode_core",
               dialogue_id="mine_mother_lode", prompt="Listen at the seam"),
        chest(2144, g, "the loose ore the miners can weigh", 65),
        light("lode_echo_light", 1988, 586, 300, "#ead5a8"),
        start(LODE, 204, 656),
    ]
    return build(LODE, "THE LISTENING CAVERN", e, deep=True, danger=True, zoom=0.85)


ROOMS = (yard, shaft, assay, vent, basin, pocket, lower, lode)


def main(argv):
    only = {id for arg in argv if arg.startswith("--rooms=") for id in arg.split("=", 1)[1].split(",")}
    specs = []
    out = Path(tempfile.gettempdir()) / "ambition_elemental_mine_specs"
    out.mkdir(exist_ok=True)
    for make in ROOMS:
        rid, spec = make()
        if only and rid not in only:
            continue
        path = out / f"{rid}.ron"
        path.write_text(spec)
        specs.append(path)
        print(path)
    if unknown := only - {path.stem for path in specs}:
        raise SystemExit(f"Unknown room: {sorted(unknown)}")
    if "--apply" not in argv:
        return 0
    return make_rooms(WORLD, specs, keep_position=True, overwrite_hand_edits="--overwrite-hand-edits" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
