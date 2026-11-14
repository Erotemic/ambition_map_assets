#!/usr/bin/env python3
"""Write the rooms of level 1: the creator's basement, the service stair, the
Drain Market and the drains under it.

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/intro/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/intro/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Design: `docs/planning/game/level-1.md`.

    [basement lab | loading bay]--[service stair]--[Drain Market]--(gate stack)
                                                    | manhole
                                                [the culvert]--[Alice's station]--[Bob's end]

THE KIT. Every required way is made for run, ONE jump, drop through a
one-way floor and the strike. A jump rises about 88 px (jump 630 px/s,
gravity 2250); a level gap of 112 px or less is safe at a run (270 px/s).
`check_reach` refuses a required step up of more than 64 px. The robot's
shipped kit is larger (air jump, wall jump, dash, flight); the level does not
need it.

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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_intro_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))

from district_kit import (  # noqa: E402
    WALL, WORLDS, entity, ledge, make_rooms, paint, room, run, sign, solid, start,
)

WORLD_LDTK = WORLDS / "intro.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/intro/make_specs.py"

LAB = "intro_wake_room"
STAIR = "intro_escape_shaft"
MARKET = "drain_alley"
GATE_STACK = "gate_stack_lower"

BG = "#14161C"
LAB_MUSIC = "tech_bros_disruption"

#: The gate stack is LDtk-owned: its floor is at y 736 in the world, and its
#: west side at x 4928. The market's street is level with it, and each room
#: west of the market is placed from there.
GATE_STACK_WEST = 4928
STREET_WORLD_Y = 736

LAB_W, LAB_H, LAB_FLOOR = 2240, 448, 352
STAIR_W, STAIR_H, STAIR_FLOOR, STAIR_TOP = 1280, 768, 704, 192
MARKET_W = 1408

#: Each room: where it is in the world (its top left), and its size.
ROOMS_AT = {
    LAB: ((0, STREET_WORLD_Y - STAIR_TOP + STAIR_FLOOR - LAB_FLOOR), (LAB_W, LAB_H)),
    STAIR: ((LAB_W, STREET_WORLD_Y - STAIR_TOP), (STAIR_W, STAIR_H)),
    MARKET: ((GATE_STACK_WEST - MARKET_W, STREET_WORLD_Y - 608), (MARKET_W, 768)),
    # The drains under the market, west to east.
    "under_town_pipes": ((GATE_STACK_WEST - MARKET_W, 896), (1600, 640)),
    "alice_relay": ((GATE_STACK_WEST - MARKET_W + 1600, 896), (1024, 640)),
    "bob_relay": ((GATE_STACK_WEST - MARKET_W + 2624, 896), (1024, 640)),
    "intro_freight_yard": ((GATE_STACK_WEST - MARKET_W + 3648, 896), (1920, 640)),
}

#: The highest step up that a required way may ask (one jump rises ~88).
MAX_STEP = 64


def check_reach(rid, floors):
    """Refuse a required way whose step up is more than `MAX_STEP`.

    `floors` is the required way, in order: the top of each surface the
    player stands on to go on."""
    for (a_name, a), (b_name, b) in zip(floors, floors[1:]):
        if a - b > MAX_STEP:
            raise SystemExit(f"{rid}: from {a_name} ({a}) up to {b_name} ({b}) is {a - b} px, more than one jump")


def edge(zone, name, x, floor, to_room, to_zone, h=96):
    return entity("LoadingZone", x, floor - h, 16, h, id=zone, name=name, activation="EdgeExit",
                  target_room=to_room, target_zone=to_zone, bidirectional=True)


def npc(character, dialogue, prompt, x, floor, brain=None, w=32, h=48):
    fields = dict(character_id=character, prompt=prompt, dialogue_id=dialogue)
    if brain:
        fields["brain_override"] = brain
    return entity("NpcSpawn", x - w // 2, floor - h, w, h, **fields)


def raider(rid, n, x, floor, character="npc_lab_raider"):
    return entity("EnemySpawn", x - 16, floor - 48, 32, 48, name=f"{rid}_raider_{n}", brain="medium_striker",
                  character_id=character, respawn="OnRoomReenter")


def slug(rid, n, x, floor):
    """Vermin of the rubble. They do not fight."""
    return entity("EnemySpawn", x - 24, floor - 22, 48, 22, name=f"{rid}_slug_{n}", brain="puppy_slug",
                  character_id="npc_puppy_slug", disposition="Peaceful", respawn="OnRoomReenter")


def build(rid, entities, title, music, *, dangerous=False, extra=""):
    at, size = ROOMS_AT[rid]
    return rid, room(rid, entities, at=at, size=size, biome="lab", music=music, bg=BG, title=title,
                     generator=GENERATOR, dangerous=dangerous, extra=extra)


def undertown(rid, entities, title, *, dangerous=False, extra=""):
    """A room of the town under the gate stack: the cave biome, drawn
    behind with the under-town backdrop."""
    at, size = ROOMS_AT[rid]
    text = room(rid, entities, at=at, size=size, biome="cave", music=LAB_MUSIC, bg=BG, title=title,
                generator=GENERATOR, dangerous=dangerous, extra=extra)
    return rid, text.replace('parallax_theme: "cave"', 'parallax_theme: "undertown"')


# ------------------------------------------------- 1-2. the lab and the bay

#: The diagnostic cart the robot wakes on (`the_cart_of_the_wake_room`
#: measures it): its bed, and the ramp let down from its back end.
CART_BED = (48, 224, 294)
CART_RAMP_FOOT = 326
#: The first jump: the creator's workbench, a step of 48.
BENCH = (544, 672, LAB_FLOOR - 48)
#: The first gap: a cable trench, 96 wide and 48 deep. A fall costs a jump.
TRENCH = (864, 960, LAB_FLOOR + 48)
#: The lab ends and the loading bay begins at this x.
BAY_X = 1040
#: The bay door: it stands until the raid is beaten.
BAY_DOOR_X = 2096
RAID_FIGHT = "intro_bay_raid"


def lab():
    """THE BASEMENT LAB and THE LOADING BAY. One floor, so the creator keeps
    beside the robot from the cart to the bay door. The raid starts where the
    lab opens on the bay; the bay door is shut until the last raider falls,
    and the creator's last words play in its doorway."""
    rid = LAB
    w, h, g = LAB_W, LAB_H, LAB_FLOOR
    x0, x1, bed = CART_BED
    t0, t1, t_bed = TRENCH
    b0, b1, b_top = BENCH
    check_reach(rid, [("floor", g), ("bench", b_top), ("floor", g), ("trench", t_bed), ("floor", g)])
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 96 - 32),
        solid("floor_lab", 0, g, t0, h - g),
        solid("trench_bed", t0, t_bed, t1 - t0, h - t_bed),
        solid("floor_bay", t1, g, w - t1, h - g),
        solid("bench", b0, b_top, b1 - b0, g - b_top),
        # The cart: its bed is a platform that stands still, and its back end
        # is let down as a ramp to the floor.
        # A platform that stands still: `speed: 0` (with no speed it moves).
        entity("MovingPlatform", x0, bed, x1 - x0, 12, id="intro_cart", name="Diagnostic Cart", speed=0.0,
               visual="intro_cart", one_way=True),
        entity("MovingPlatform", x1, bed + 4, 7, 54, id="intro_cart_ramp_step_01", name="Cart ramp step 1", speed=0.0,
               visual="intro_cart_ramp", one_way=True),
        entity("SurfaceChain", x1, bed - 16, 16, 16, name="Cart ramp", points=f"{x1},{bed}; {CART_RAMP_FOOT},{g}",
               visual="none"),
        entity("PlayerStart", 122, 248, 28, 46, name="wake_room_spawn"),
        # The hub's door comes out here (one way: nothing leads back).
        entity("LoadingZone", 112, 198, 48, 96, id="wake_room_arrival", name="wake room arrival", activation="Door",
               presentation="SceneArt"),
        npc("npc_creator", "creator_intro", "Talk to the Creator", 456, g, brain="follows_closely"),
        entity("Prop", 336, 224, 128, 128, name="Neural Console", kind="lab_neural_console"),
        entity("Prop", 704, 224, 128, 128, name="Genesis Vat", kind="lab_genesis_vat"),
        entity("Prop", 1840, 224, 128, 128, name="Power Core", kind="lab_power_core"),
        sign("lab_sign_cart", 176, 120, "DO NOT SWITCH ON UNTIL FINISHED", 300),
        sign("lab_sign_bench", 608, 176, "MY BENCH. MY TOOLS. ASK FIRST.", 300),
        # The bay.
        entity("CutsceneTrigger", BAY_X + 48, 32, 64, g - 32, cutscene="intro_raid"),
        entity("EncounterTrigger", BAY_X + 176, 32, 64, g - 32, id=RAID_FIGHT, name=f"{RAID_FIGHT}_trigger"),
        raider(rid, 1, 1520, g),
        raider(rid, 2, 1600, g),
        ledge("crates_low", 1360, g - 64, 128),
        solid("crate_stack", 1680, g - 48, 64, 48),
        ledge("crates_high", 1840, g - 112, 128),
        sign("bay_sign_deliveries", 1560, 120, "DELIVERIES: NONE EXPECTED", 320),
        entity("LockWall", BAY_DOOR_X, 32, 32, g - 32, id="intro_bay_door", name="the bay door",
               gated_by=f"encounter.cleared {RAID_FIGHT}"),
        entity("CutsceneTrigger", BAY_DOOR_X + 40, 32, 72, g - 32, cutscene="creator_final_fragment"),
        sign("bay_sign_stair", BAY_DOOR_X + 56, g - 160, "STAIR UP", 140),
        edge("raid_to_escape", "to the service stair", w - WALL, g, STAIR, "escape_from_raid"),
    ]
    return build(rid, e, "THE BASEMENT LAB", LAB_MUSIC, dangerous=True,
                 extra='\n    entry_cutscene: "intro_wake",')


# ---------------------------------------------------- 3. the service stair

#: The three tiers of the wrecked stair, bottom to top.
TIER_2 = 512
TIER_3 = 320
#: The holes in the stair: a pit in the bottom floor, a hole in the middle
#: landing (a fall goes back down a tier), and the gap where a girder fell.
PIT = (736, 832, STAIR_FLOOR + 64)
LANDING_HOLE = (640, 736)
GIRDER_GAP = (560, 656)


def stair():
    """THE SERVICE STAIR. The raiders came down it and blew its door; half
    the flights are gone. Three tiers: east along the bottom, west along the
    middle landing, east along the fallen girders to the street."""
    rid = STAIR
    w, h, g = STAIR_W, STAIR_H, STAIR_FLOOR
    p0, p1, p_bed = PIT
    l0, l1 = LANDING_HOLE
    gg0, gg1 = GIRDER_GAP
    # Flight A climbs from the bottom floor at the east wall, westward, onto
    # the middle landing; flight B climbs from the landing's west end onto
    # the girders; two crates lift the girders to the top landing.
    flight_a = [(1216, 1264, g - 48), (1168, 1216, g - 96), (1120, 1168, g - 144)]
    flight_b = [(352, 400, TIER_2 - 48), (304, 352, TIER_2 - 96), (256, 304, TIER_2 - 144)]
    top_crate = (1000, 1064, TIER_3 - 64)
    check_reach(rid, [("floor", g), ("rubble", g - 48), ("floor", g), *[("flight A", t) for *_, t in flight_a],
                      ("landing", TIER_2), *[("flight B", t) for *_, t in flight_b], ("girders", TIER_3),
                      ("crate", top_crate[2]), ("top landing", STAIR_TOP)])
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 96 - 32),
        solid("east_wall", w - WALL, STAIR_TOP + 16, WALL, g - STAIR_TOP - 16),
        solid("east_wall_top", w - WALL, 32, WALL, STAIR_TOP - 96 - 32),
        # The bottom: rubble to jump, a pit to cross (a fall costs a jump).
        solid("floor_west", 0, g, p0, h - g),
        solid("pit_bed", p0, p_bed, p1 - p0, h - p_bed),
        solid("floor_east", p1, g, w - p1, h - g),
        solid("rubble", 448, g - 48, 64, 48),
        *[solid(f"flight_a_{n}", a, top, b - a, g - top) for n, (a, b, top) in enumerate(flight_a)],
        # The middle landing, with the hole in it.
        solid("landing_west", 400, TIER_2, l0 - 400, 32),
        solid("landing_east", l1, TIER_2, 1120 - l1, 32),
        *[solid(f"flight_b_{n}", a, top, b - a, TIER_2 - top) for n, (a, b, top) in enumerate(flight_b)],
        # The girders: one-way, so a body on flight B comes up through them.
        ledge("girder_west", 160, TIER_3, gg0 - 160),
        ledge("girder_east", gg1, TIER_3, top_crate[0] - gg1),
        solid("top_crate", top_crate[0], top_crate[2], top_crate[1] - top_crate[0], 32),
        solid("top_landing", top_crate[1], STAIR_TOP, w - top_crate[1], 32),
        edge("escape_from_raid", "down to the loading bay", 0, g, LAB, "raid_to_escape"),
        edge("escape_to_drain", "up to the street", w - WALL, STAIR_TOP, MARKET, "drain_from_escape"),
        start(rid, 160, g),
        raider(rid, 1, 880, TIER_2),
        slug(rid, 1, 300, g),
        slug(rid, 2, 980, g),
        slug(rid, 3, 760, TIER_3),
        sign("stair_sign_up", 1180, STAIR_TOP - 120, "STREET LEVEL", 200),
        sign("stair_sign_door", 150, g - 150, "14 CULVERT LANE. PRIVATE.", 280),
    ]
    return build(rid, e, "THE SERVICE STAIR", LAB_MUSIC, dangerous=True)


# ------------------------------------------------------ 4. the Drain Market

STREET = 608
UNDER_TOWN = "under_town_pipes"
BOB = "bob_relay"
BOSS = "first_system_boss"
#: Oiler's post: he stands at his workshop, and the volume round it starts
#: his line when a player comes up to him.
OILER_X = 1100


def market():
    """THE DRAIN MARKET. A street under the gate stack: stalls with awnings
    over it, Oiler's workshop, the news board, the drain covers down to the
    culvert. East is the gate stack."""
    rid = MARKET
    _, (w, h) = ROOMS_AT[rid]
    g = STREET
    # The awnings step up from the soup stall to the gantry over the street:
    # nothing on them is needed to cross the market.
    awnings = [("awning_soup", 640, 784, g - 64), ("awning_fish", 744, 888, g - 128), ("awning_top", 840, 984, g - 192)]
    gantry = ("gantry", 520, 800, g - 256)
    check_reach(rid, [("street", g), *[(n, top) for n, _, _, top in awnings], (gantry[0], gantry[3])])
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("street", 0, g, w, h - g),
        solid("west_wall", 0, 32, WALL, g - 96 - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 96 - 32),
        edge("drain_from_escape", "down the service stair", 0, g, STAIR, "escape_to_drain"),
        edge("drain_to_gate_stack", "to the gate stack", w - WALL, g, GATE_STACK, "gate_stack_from_drain"),
        start(rid, 120, g),
        npc("npc_news_board", "news_board_lab_incident", "Read the news board", 300, g),
        entity("LoadingZone", 496, g - 96, 48, 96, id="under_town_to_drain", name="down the drain cover", activation="Door",
               target_room=UNDER_TOWN, target_zone="under_town_from_drain", bidirectional=True),
        sign("market_sign_drain", 520, g - 140, "DRAINS: STAFF ONLY", 220),
        *[ledge(n, x0, top, x1 - x0) for n, x0, x1, top in awnings],
        ledge(*gantry[:1], gantry[1], gantry[3], gantry[2] - gantry[1]),
        sign("market_sign_soup", 712, g - 40, "SOUP", 100),
        entity("ChestSpawn", 880, awnings[2][3] - 58, 76, 58, name="a purse on the awning", reward="currency:30"),
        entity("LoadingZone", 900, g - 96, 48, 96, id="drain_from_bob_return", name="down the other drain cover",
               activation="Door", target_room=BOB, target_zone="bob_return_to_drain", bidirectional=True),
        npc("npc_oiler", "oiler_intro", "Talk to Oiler", OILER_X, g, brain="meets_the_player"),
        entity("ShrineSpawn", OILER_X + 80, g - 80, 44, 80, id="drain_alley_oiler_bench", name="Oiler's bench"),
        entity("CutsceneTrigger", OILER_X - 140, g - 176, 288, 176, cutscene="oiler_notices"),
        sign("market_sign_oiler", OILER_X + 40, g - 200, "OILER: REPAIRS. KNEES, PIPES, DOORS. NO SHARKS.", 420),
        entity("LoadingZone", 1300, g - 96, 48, 96, id="drain_from_boss_return", name="the service door", activation="Door",
               target_room=BOSS, target_zone="boss_return_to_drain", bidirectional=True),
        entity("LoadingZone", 176, g - 96, 48, 96, id="drain_from_alice", name="Alice's hatch", activation="Door",
               target_room=ALICE, target_zone="alice_hatch", bidirectional=True),
        sign("market_sign_food", 300, g - 230, "No swordguns inside the food court", 380),
        sign("market_sign_ripples", 1180, 120, "Report unstable ripples to platform staff", 420),
        sign("market_sign_gates", 1330, g - 160, "GATES", 120),
    ]
    return undertown(rid, e, "THE DRAIN MARKET", extra='\n    entry_cutscene: "drain_market_arrival",')


# ------------------------------------------------- 5. the culvert

ALICE = "alice_relay"
#: The walk out of the drains into Alice's station and on to Bob's end.
DRAIN_WALK = 480
#: The sump: (room, x0, y0, x1, y1) of each pit of drain water, painted
#: murky after the rooms are made. It stings (a `DamageVolume`).
SUMP = []


def sump(rid, n, x0, y0, x1, y1):
    SUMP.append((rid, x0, y0, x1, y1))
    return entity("DamageVolume", x0, y0, x1 - x0, y1 - y0, name=f"{rid} sump {n}", damage=1.0)


def culvert():
    """THE CULVERT. The storm drain under the market. From the drain cover
    the upper walk drops to the middle walk; past it the sump runs the rest
    of the way, crossed on stepping stones and, at its widest, on a raft. A
    goblin lookout stands on the far walk, listening."""
    rid = UNDER_TOWN
    _, (w, h) = ROOMS_AT[rid]
    upper, mid, stone, bed = 256, 416, 448, 624
    stones = [(816, 880), (976, 1040), (1296, 1360)]
    # The way back up from the middle walk to the drain cover.
    back_up = [("crate_ledge", 480, 560, 352), ("pipe_ledge", 400, 480, 288)]
    check_reach(rid, [("middle walk", mid), *[(n, top) for n, _, _, top in back_up], ("upper walk", upper)])
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, h - 32),
        solid("east_wall", w - WALL, 32, WALL, DRAIN_WALK - 96 - 32),
        solid("upper_walk", WALL, upper, 400 - WALL, 32),
        entity("LoadingZone", 96, upper - 96, 48, 96, id="under_town_from_drain", name="up to the market",
               activation="Door", target_room=MARKET, target_zone="under_town_to_drain", bidirectional=True),
        *[ledge(n, x0, top, x1 - x0) for n, x0, x1, top in back_up],
        solid("middle_walk", WALL, mid, 720 - WALL, h - mid),
        # Behind a cracked wall at the west end of the middle walk: a dry
        # corner somebody keeps things in.
        entity("BreakablePlatform", 240, upper + 32, 32, mid - upper - 32, id="culvert_cracked_wall",
               name="a cracked wall", max_hp=3.0, respawn="Persistent", collision="Solid", trigger="OnHit"),
        entity("PickupSpawn", 108, mid - 34 - 4, 24, 24, name="a can of oil", kind="health:2"),
        solid("sump_bed", 720, bed, 1360 - 720, h - bed),
        sump(rid, 0, 720, bed - 48, 1360, bed),
        *[solid(f"stone_{n}", x0, stone, x1 - x0, bed - stone) for n, (x0, x1) in enumerate(stones)],
        entity("MovingPlatform", 1056, stone, 96, 16, id=f"{rid}_raft", name="a raft of crates", sweep_dx=144.0,
               speed=60.0, one_way=True),
        solid("east_walk", 1360, DRAIN_WALK, w - 1360, h - DRAIN_WALK),
        edge("under_town_to_alice", "along the drain", w - WALL, DRAIN_WALK, ALICE, "alice_from_under_town"),
        start(rid, 140, upper),
        slug(rid, 1, 420, mid),
        slug(rid, 2, 600, mid),
        raider(rid, 1, 1480, DRAIN_WALK, character="goblin"),
        sign("culvert_sign_cover", 120, upper - 140, "MARKET", 140),
        sign("culvert_sign_sump", 1040, stone - 120, "SUMP. KEEP OUT.", 220),
    ]
    return undertown(rid, e, "THE CULVERT", dangerous=True)


# ------------------------------------------------- 6-7. Alice and Bob

BOB_ROOM = "bob_relay"
#: The survey line across Alice's high walk: it is taken down when Bob has
#: the last reading (`bob_field_survey_received`).
SURVEY_LINE = "alice_survey_line"


def alice():
    """ALICE'S STATION. Alice at her instrument, mid-traverse: she does not
    leave it. The low walk goes on to Bob; the high walk goes to her hatch up
    into the market, across the survey line."""
    rid = ALICE
    _, (w, h) = ROOMS_AT[rid]
    g, high = DRAIN_WALK, 224
    climb = [("ledge_1", 320, 432, g - 64), ("ledge_2", 400, 512, g - 128), ("ledge_3", 480, 576, g - 192)]
    check_reach(rid, [("walk", g), *[(n, top) for n, _, _, top in climb], ("high walk", high)])
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("walk", 0, g, w, h - g),
        solid("west_wall", 0, 32, WALL, g - 96 - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 96 - 32),
        edge("alice_from_under_town", "back along the drain", 0, g, UNDER_TOWN, "under_town_to_alice"),
        edge("alice_to_bob", "on to Bob's end", w - WALL, g, BOB_ROOM, "bob_from_alice"),
        start(rid, 120, g),
        npc("npc_alice", "alice_station", "Talk to Alice", 220, g, brain="stand_still"),
        sign("alice_sign_station", 220, g - 150, "SURVEY STATION A", 240),
        *[ledge(n, x0, top, x1 - x0) for n, x0, x1, top in climb],
        solid("high_walk", 560, high, w - WALL - 560, 32),
        entity("LockWall", 656, 32, 16, high - 32, id=SURVEY_LINE, name="the survey line",
               gated_by="bob_field_survey_received"),
        sign("alice_sign_line", 760, high - 130, "SURVEY LINE. DO NOT CROSS.", 300),
        entity("LoadingZone", 900, high - 96, 48, 96, id="alice_hatch", name="up through Alice's hatch",
               activation="Door", target_room=MARKET, target_zone="drain_from_alice", bidirectional=True),
    ]
    return undertown(rid, e, "ALICE'S STATION", dangerous=True)


def bob():
    """BOB'S END. Bob holds the staff at the far end of the traverse. On
    the way to him the drain floor is broken into the sump; Eve sits by a
    pipe in the middle, listening to it."""
    rid = BOB_ROOM
    _, (w, h) = ROOMS_AT[rid]
    g, bed = DRAIN_WALK, 576
    pits = [(256, 352), (544, 640)]
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 96 - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 96 - 32),
    ]
    x = 0
    for n, (x0, x1) in enumerate(pits):
        e += [solid(f"walk_{n}", x, g, x0 - x, h - g), solid(f"pit_{n}_bed", x0, bed, x1 - x0, h - bed),
              sump(rid, n, x0, bed - 48, x1, bed)]
        x = x1
    e += [
        solid(f"walk_{len(pits)}", x, g, w - x, h - g),
        edge("bob_from_alice", "back to Alice's station", 0, g, ALICE, "alice_to_bob"),
        entity("LoadingZone", 940, g - 96, 48, 96, id="bob_return_to_drain", name="up the drain cover", activation="Door",
               target_room=MARKET, target_zone="drain_from_bob_return", bidirectional=True),
        start(rid, 120, g),
        npc("npc_eve", "eve_drain_pipe", "Talk to Eve", 450, g, brain="stand_still"),
        npc("npc_bob", "bob_station", "Talk to Bob", 820, g, brain="stand_still"),
        sign("bob_sign_station", 820, g - 150, "SURVEY STATION B", 240),
        sign("bob_sign_cover", 940, g - 140, "MARKET", 140),
        # Bob's grate: the survey crew keeps the key, and he opens it when the
        # traverse is closed. Past it the drain runs under the checkpoint.
        entity("LockWall", w - 48, 32, 16, g - 32, id="bob_grate", name="Bob's grate",
               gated_by="bob_field_survey_received"),
        edge("bob_to_yard", "on under the checkpoint", w - WALL, g, YARD, "yard_from_bob"),
    ]
    return undertown(rid, e, "BOB'S END", dangerous=True)


# ------------------------------------------------- 9. the freight yard

YARD = "intro_freight_yard"
YARD_FIGHT = "intro_freight_yard_fight"
#: The door of the yard comes out in the gate stack behind its checkpoint.
GATE_STACK_FROM_YARD = "gate_stack_from_yard"


def yard():
    """THE FREIGHT YARD. The goblins' camp behind the gate stack, where the
    crate waits for a gate. The fight shuts the yard (its seal); after it the
    inner gate is open, and behind it are the crate and the door up into the
    gate stack, behind the checkpoint."""
    rid = YARD
    _, (w, h) = ROOMS_AT[rid]
    g = DRAIN_WALK
    crates = [("crate_a", 560, 624, g - 48), ("crate_b", 1000, 1096, g - 48)]
    ledges = [("crate_stack_a", 700, 860, g - 112), ("crate_stack_b", 1160, 1320, g - 112)]
    check_reach(rid, [("yard", g), ("crate_a", crates[0][3]), ("stack_a", ledges[0][3])])
    e = [
        solid("ceiling", 0, 0, w, 32),
        solid("yard", 0, g, w, h - g),
        solid("west_wall", 0, 32, WALL, g - 96 - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 32),
        edge("yard_from_bob", "back along the drain", 0, g, BOB_ROOM, "bob_to_yard"),
        start(rid, 80, g),
        entity("CutsceneTrigger", 200, 32, 64, g - 32, cutscene="salvage_lead_yard"),
        # The fight's seal (an encounter wall: no `gated_by`) and its strip.
        entity("LockWall", 136, 32, 16, g - 32, id="intro_freight_yard_seal", name="the yard gate"),
        entity("EncounterTrigger", 320, 32, 64, g - 32, id=YARD_FIGHT, name=f"{YARD_FIGHT}_trigger"),
        *[solid(n, x0, top, x1 - x0, g - top) for n, x0, x1, top in crates],
        *[ledge(n, x0, top, x1 - x0) for n, x0, x1, top in ledges],
        sign("yard_sign_camp", 900, 120, "NO ENTRY. GOBLINS AT WORK.", 360),
        entity("LockWall", 1504, 32, 32, g - 32, id="intro_yard_inner_gate", name="the inner gate",
               gated_by=f"encounter.cleared {YARD_FIGHT}"),
        entity("CutsceneTrigger", 1584, 32, 96, g - 32, cutscene="creator_notebooks"),
        sign("yard_sign_crate", 1632, g - 120, "ONE LAB OF RESEARCH. PAID.", 300),
        entity("LoadingZone", 1800, g - 96, 48, 96, id="yard_to_gate_stack", name="up into the gate stack",
               activation="Door", target_room=GATE_STACK, target_zone=GATE_STACK_FROM_YARD, bidirectional=True),
    ]
    return undertown(rid, e, "THE FREIGHT YARD", dangerous=True)


ROOMS = (lab, stair, market, culvert, alice, bob, yard)


def main(argv):
    made = []
    SUMP.clear()
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
    # The sump is murky water (2): a body sinks into it, and it hides what is
    # under its surface.
    for rid, x0, y0, x1, y1 in SUMP:
        if code := paint(WORLD_LDTK, rid, "Water", 2, x0, y0, x1 - x0, y1 - y0):
            return code
    code, _ = run("validate", str(WORLD_LDTK))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
