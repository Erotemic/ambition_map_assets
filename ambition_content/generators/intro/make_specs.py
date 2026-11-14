#!/usr/bin/env python3
"""Write the rooms of level 1, Hobford: the Creator's workshop and the hill
country round the village, and the two town rooms under the gate stack that
this script also owns.

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/intro/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/intro/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Design: `docs/planning/game/level-1.md`.

    [workshop]--[Hobford Lane]==========[the high meadow]=========[the gate clearing]
                    | bank path              | hill path               | siding stair
              [the millstream]------------[Hobford]-------------[the woods]------[the freight siding]

    (== is the ridge path as well as the road: two edges, high and low.)

THE KIT. Every required way is made for run, ONE jump, drop through a
one-way floor and the strike, and each level-1 room withholds the rest of a
player's kit (`SMALL_KIT_WITHHELD`, the level field `withheld_verbs`). A jump
rises about 88 px (jump 630 px/s, gravity 2250); a level gap of 112 px or
less is safe at a run (270 px/s). `check_reach` refuses a required step up of
more than 64 px; it compares heights only, so each required way is also
walked by `walked_route_census` under the level's kit.

NO ROUTE WAITS ON A STORY FACT. A wall here is a barrier on a lever, a door
the raid breaks, or a survey line that comes down when the survey is over;
each place it closes off can be reached another way.

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
    WALL, WORLDS, entity, ledge, make_rooms, paint, room, run, sign, solid, start, water,
)

WORLD_LDTK = WORLDS / "intro.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/intro/make_specs.py"

WORKSHOP = "intro_wake_room"
LANE = "intro_hobford_lane"
MEADOW = "intro_high_meadow"
CLEARING = "intro_gate_clearing"
SIDING = "intro_freight_yard"
MILLSTREAM = "intro_millstream"
VILLAGE = "intro_hobford"
WOODS = "intro_woods"
MARKET = "drain_alley"
UNDER_TOWN = "under_town_pipes"
GATE_STACK = "gate_stack_lower"

BG = "#14161C"
COUNTRY_BG = "#9CC3E4"
#: The level's looks (`tools/ambition_sprite2d_renderer`: the scenes in
#: `backgrounds/hobford.py`, a skin, motes, a door and decor for each).
WORKSHOP_LOOK = "creator_workshop"
COUNTRY_LOOK = "hobford"
WOODS_LOOK = "hobford_woods"
WORKSHOP_MUSIC = "something_worth_building"
COUNTRY_MUSIC = "a_possible_morning"
VILLAGE_MUSIC = "doves_of_the_commons"
GOBLIN_MUSIC = "first_goblin_tune_v2_radio"
LAB_MUSIC = "tech_bros_disruption"

#: The gate stack is LDtk-owned: its floor is at y 736 in the world, and its
#: west side at x 4928. The market's street is level with it.
GATE_STACK_WEST = 4928
STREET_WORLD_Y = 736
MARKET_W = 1408

#: The level is in a band of its own below the town. The upper row's ground
#: (the workshop's floor, the lane, the meadow, the clearing) is at world y
#: 2720; the lower row's (the millstream, Hobford, the woods, the siding) at
#: 3328.
UPPER_Y, LOWER_Y = 2048, 2816
COUNTRY_W, COUNTRY_H, COUNTRY_FLOOR = 2400, 768, 672
LOW_H, LOW_FLOOR = 640, 512
WORKSHOP_W, WORKSHOP_H, WORKSHOP_FLOOR = 1600, 448, 352
#: The ridge path: the top tier of the upper row, from the lane to the
#: clearing. It is the second way to the clearing's lever.
RIDGE = 224

#: Each room: where it is in the world (its top left), and its size.
ROOMS_AT = {
    WORKSHOP: ((0, UPPER_Y + COUNTRY_FLOOR - WORKSHOP_FLOOR), (WORKSHOP_W, WORKSHOP_H)),
    LANE: ((WORKSHOP_W, UPPER_Y), (COUNTRY_W, COUNTRY_H)),
    MEADOW: ((WORKSHOP_W + COUNTRY_W, UPPER_Y), (COUNTRY_W, COUNTRY_H)),
    CLEARING: ((WORKSHOP_W + 2 * COUNTRY_W, UPPER_Y), (COUNTRY_W, COUNTRY_H)),
    MILLSTREAM: ((WORKSHOP_W, LOWER_Y), (COUNTRY_W, LOW_H)),
    VILLAGE: ((WORKSHOP_W + COUNTRY_W, LOWER_Y), (COUNTRY_W, LOW_H)),
    WOODS: ((WORKSHOP_W + 2 * COUNTRY_W, LOWER_Y), (COUNTRY_W, LOW_H)),
    SIDING: ((WORKSHOP_W + 3 * COUNTRY_W, LOWER_Y), (1920, LOW_H)),
    # The town under the gate stack (not level 1).
    MARKET: ((GATE_STACK_WEST - MARKET_W, STREET_WORLD_Y - 608), (MARKET_W, 768)),
    UNDER_TOWN: ((GATE_STACK_WEST - MARKET_W, 896), (1600, 640)),
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


def door(zone, name, x, floor, to_room, to_zone):
    return entity("LoadingZone", x, floor - 96, 48, 96, id=zone, name=name, activation="Door",
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
    """Vermin of the drains. They do not fight."""
    return entity("EnemySpawn", x - 24, floor - 22, 48, 22, name=f"{rid}_slug_{n}", brain="puppy_slug",
                  character_id="npc_puppy_slug", disposition="Peaceful", respawn="OnRoomReenter")


def hen(rid, n, x, floor, dialogue="hobford_hen"):
    """A hen of the farm. She walks about and pays the player no mind."""
    return npc("chicken_hen", dialogue, "Look at the hen", x, floor, brain="townsfolk_roam", w=32, h=44)


def walls(w, floor_h, *, west=(), east=(), top=0):
    """The side walls of an open-air room, each with a 96-high opening above
    each floor in `west` and `east` (the edges go in the openings)."""
    out = []
    for side, x, opens in (("west", 0, west), ("east", w - WALL, east)):
        y = top
        for n, floor in enumerate(sorted(opens)):
            if floor - 96 > y:
                out.append(solid(f"{side}_wall_{n}", x, y, WALL, floor - 96 - y))
            y = floor + 16
        if floor_h > y:
            out.append(solid(f"{side}_wall_end", x, y, WALL, floor_h - y))
    return out


#: What level 1 withholds from a player's kit (`RoomMetadata::withheld_verbs`):
#: everything past run, one jump, drop through and the strike. Pogo is held
#: back too; the level teaches the plain strike first.
SMALL_KIT_WITHHELD = (
    "double_jump wall_jump wall_cling wall_climb ledge_grab dash double_dash dodge "
    "fly fly_toggle glide blink precision_blink blink_through_soft_walls "
    "blink_through_hard_walls pogo directional_special shield grab morph"
)
KIT = f'\n    withheld_verbs: "{SMALL_KIT_WITHHELD}",'


def build(rid, entities, title, music, *, look=COUNTRY_LOOK, bg=COUNTRY_BG, dangerous=False, extra=""):
    """A room of level 1: it withholds the large kit."""
    at, size = ROOMS_AT[rid]
    return rid, room(rid, entities, at=at, size=size, biome=look, music=music, bg=bg, title=title,
                     generator=GENERATOR, dangerous=dangerous, extra=KIT + extra)


def undertown(rid, entities, title, *, dangerous=False, extra=""):
    """A room of the town under the gate stack: the cave biome, drawn behind
    with the under-town backdrop. The town is past level 1, so it keeps the
    whole kit."""
    at, size = ROOMS_AT[rid]
    text = room(rid, entities, at=at, size=size, biome="cave", music=LAB_MUSIC, bg=BG, title=title,
                generator=GENERATOR, dangerous=dangerous, extra=extra)
    return rid, text.replace('parallax_theme: "cave"', 'parallax_theme: "undertown"')


# ------------------------------------------------------------ the workshop

#: The charging cart Scout wakes on (`the_cart_of_the_wake_room` measures
#: it): its bed, and the ramp let down from its back end.
CART_BED = (48, 224, 294)
CART_RAMP_FOOT = 326
#: The test plinth: the first jump, a step of 48.
PLINTH = (440, 520, WORKSHOP_FLOOR - 48)
#: Up to the loft: a crate (48), then the loft boards (64 more).
LOFT_CRATE = (600, 664, WORKSHOP_FLOOR - 48)
LOFT = (640, 940, WORKSHOP_FLOOR - 112)
#: The bench, and the Creator at it. The raid comes in at the barn door
#: beside him, so the raiders are in earshot of the conversation they break.
BENCH = (1080, 1200, WORKSHOP_FLOOR - 48)
CREATOR_X = 1240
BARN_DOOR_X = 1320
RAID = "intro_workshop_raid"


def workshop():
    """THE WORKSHOP. The Creator's barn outside Hobford: the charging cart,
    the test plinth, the parts loft, his bench, the barn door. The raid
    starts in his conversation (`encounter.start`, at the node it breaks), or
    when Scout goes to the barn door without talking to him (the trigger in
    front of the door): the goblins are coming either way. The barn door is
    barred for the test and is broken in the raid."""
    rid = WORKSHOP
    w, h, g = WORKSHOP_W, WORKSHOP_H, WORKSHOP_FLOOR
    x0, x1, bed = CART_BED
    check_reach(rid, [("floor", g), ("plinth", PLINTH[2]), ("floor", g), ("crate", LOFT_CRATE[2]), ("loft", LOFT[2]),
                      ("floor", g), ("bench", BENCH[2]), ("floor", g)])
    e = [
        solid("roof", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 96 - 32),
        solid("floor", 0, g, w, h - g),
        # The cart: its bed is a platform that stands still (`speed: 0`; a
        # moving platform with no speed moves), and its back end is let down
        # as a ramp to the floor.
        entity("MovingPlatform", x0, bed, x1 - x0, 12, id="intro_cart", name="the charging cart", speed=0.0,
               visual="intro_cart", one_way=True),
        entity("MovingPlatform", x1, bed + 4, 7, 54, id="intro_cart_ramp_step_01", name="Cart ramp step 1", speed=0.0,
               visual="intro_cart_ramp", one_way=True),
        entity("SurfaceChain", x1, bed - 16, 16, 16, name="Cart ramp", points=f"{x1},{bed}; {CART_RAMP_FOOT},{g}",
               visual="none"),
        entity("PlayerStart", 122, 248, 28, 46, name="wake_room_spawn"),
        # The hub's door comes out here (one way: nothing leads back).
        entity("LoadingZone", 112, 198, 48, 96, id="wake_room_arrival", name="wake room arrival", activation="Door",
               presentation="SceneArt"),
        sign("workshop_sign_cart", 176, 120, "DO NOT SWITCH ON UNTIL FINISHED", 300),
        solid("test_plinth", PLINTH[0], PLINTH[2], PLINTH[1] - PLINTH[0], g - PLINTH[2]),
        sign("workshop_sign_plinth", 480, PLINTH[2] - 60, "LOAD TEST", 140),
        solid("loft_crate", LOFT_CRATE[0], LOFT_CRATE[2], LOFT_CRATE[1] - LOFT_CRATE[0], g - LOFT_CRATE[2]),
        ledge("parts_loft", LOFT[0], LOFT[2], LOFT[1] - LOFT[0]),
        # On the loft: the torque gauge he sends Scout for, and an oil can at
        # the far end of the boards.
        entity("PickupSpawn", 892, LOFT[2] - 28, 24, 24, name="the torque gauge", kind="flag:intro_torque_gauge_found"),
        entity("PickupSpawn", 664, LOFT[2] - 28, 24, 24, name="a can of oil", kind="health:2"),
        sign("workshop_sign_loft", 790, LOFT[2] - 60, "GAUGES GO BACK ON THE SHELF", 300),
        solid("bench", BENCH[0], BENCH[2], BENCH[1] - BENCH[0], g - BENCH[2]),
        sign("workshop_sign_bench", 1140, BENCH[2] - 60, "LOGS. DO NOT TIDY.", 220),
        npc("npc_creator", "creator_intro", "Talk to the Creator", CREATOR_X, g),
        entity("EncounterTrigger", CREATOR_X + 32, 32, BARN_DOOR_X - CREATOR_X - 32, g - 32, id=RAID,
               name=f"{RAID}_trigger"),
        # The raid stays won: its clear greens this switch, which disarms the
        # trigger the fight carries bodies back over. A blow on the whistle a
        # raider dropped calls the raid again.
        entity("Switch", 1000, g - 32, 24, 32, id=f"{RAID}_again", name="a raider's whistle",
               prompt="Blow the whistle", target_encounter=RAID, action="ResetEncounter"),
        entity("LockWall", BARN_DOOR_X, 32, 24, g - 32, id="intro_barn_door", name="the barn door",
               gated_by=f"encounter.cleared {RAID}"),
        sign("workshop_sign_door", BARN_DOOR_X + 12, 140, "TEST IN PROGRESS. DOOR BARRED.", 320),
        entity("CutsceneTrigger", BARN_DOOR_X + 24, 32, 80, g - 32, cutscene="creator_final_fragment"),
        edge("workshop_to_lane", "out into the lane", w - WALL, g, LANE, "lane_from_workshop"),
    ]
    return build(rid, e, "THE WORKSHOP", WORKSHOP_MUSIC, look=WORKSHOP_LOOK, bg=BG, dangerous=True,
                 extra='\n    entry_cutscene: "intro_wake",')


# ------------------------------------------------------------- the lane

#: The survey line across the ridge path above Alice's station: it is taken
#: down when Bob's end of the survey is closed (`bob_field_survey_received`).
#: The ridge east of it is reached from the meadow as well.
SURVEY_LINE = "alice_survey_line"
SURVEY_LINE_X = 760
#: The terraces up the slope west of Alice's station: one-way boards, each
#: 64 above the last, alternating west and east so each jump is straight up.
TERRACES = [(560, 608), (400, 544), (560, 480), (400, 416), (560, 352), (400, 288)]
TERRACE_W = 192
ALICE_X = 940


def lane():
    """HOBFORD LANE. The first open air: the lane outside the barn, a hedge
    bank, the bank path down to the millstream, the cart track east. Above
    the lane the slope goes up in shored terraces to the ridge path; Alice's
    survey line crosses the ridge above her station."""
    rid = LANE
    w, h, g = COUNTRY_W, COUNTRY_H, COUNTRY_FLOOR
    check_reach(rid, [("lane", g), *[(f"terrace {n}", top) for n, (_, top) in enumerate(TERRACES)], ("ridge", RIDGE)])
    check_reach(rid, [("lane", g), ("hedge bank", g - 48), ("lane", g)])
    e = [
        *walls(w, g, west=[g], east=[g, RIDGE]),
        solid("ground", 0, g, w, h - g),
        edge("lane_from_workshop", "into the workshop", 0, g, WORKSHOP, "workshop_to_lane"),
        *[ledge(f"terrace_{n}", x, top, TERRACE_W) for n, (x, top) in enumerate(TERRACES)],
        ledge("ridge_path", 300, RIDGE, w - WALL - 300),
        entity("LockWall", SURVEY_LINE_X, 32, 16, RIDGE - 32, id=SURVEY_LINE, name="the survey line",
               gated_by="bob_field_survey_received"),
        sign("lane_sign_line", SURVEY_LINE_X, RIDGE - 110, "SURVEY LINE. PLEASE DON'T STEP ON IT.", 380),
        npc("npc_alice", "alice_lane", "Talk to Alice", ALICE_X, g, brain="meets_the_player"),
        sign("lane_sign_station", ALICE_X + 120, g - 150, "SURVEY STATION. MIND THE TRIPOD.", 340),
        hen(rid, 1, 260, g),
        hen(rid, 2, 420, g),
        solid("hedge_bank", 1360, g - 48, 112, 48),
        door("lane_to_millstream", "the bank path down to the mill", 1640, g, MILLSTREAM, "millstream_from_lane"),
        sign("lane_sign_mill", 1664, g - 140, "MILL", 120),
        sign("lane_sign_track", 2200, g - 160, "TRACK TO THE RING", 260),
        edge("lane_to_meadow", "up the cart track", w - WALL, g, MEADOW, "meadow_from_lane"),
        edge("lane_to_meadow_high", "along the ridge", w - WALL, RIDGE, MEADOW, "meadow_from_lane_high"),
        start(rid, 120, g),
    ]
    return build(rid, e, "HOBFORD LANE", COUNTRY_MUSIC, dangerous=True)


# ----------------------------------------------------------- the meadow

#: The way up from the meadow to the ridge: the shepherd's hut (a step of
#: 64) and the limbs of the oak beside it.
HUT = (1000, 1200, COUNTRY_FLOOR - 64)
OAK_LIMBS = [(1080, 544), (920, 480), (1080, 416), (920, 352), (1080, 288)]
LIMB_W = 140


def meadow():
    """THE HIGH MEADOW. Pasture on the hill: dry-stone walls to hop, a turf
    bank, the shepherd's hut and the oak whose limbs go up to the ridge path,
    the hill path down to Hobford. East is the gate clearing."""
    rid = MEADOW
    w, h, g = COUNTRY_W, COUNTRY_H, COUNTRY_FLOOR
    check_reach(rid, [("meadow", g), ("hut roof", HUT[2]), *[(f"limb {n}", y) for n, (_, y) in enumerate(OAK_LIMBS)],
                      ("ridge", RIDGE)])
    check_reach(rid, [("meadow", g), ("wall", g - 48), ("meadow", g), ("bank", g - 64), ("meadow", g)])
    e = [
        *walls(w, g, west=[g, RIDGE], east=[g, RIDGE]),
        solid("ground", 0, g, w, h - g),
        edge("meadow_from_lane", "down the cart track", 0, g, LANE, "lane_to_meadow"),
        edge("meadow_from_lane_high", "along the ridge", 0, RIDGE, LANE, "lane_to_meadow_high"),
        ledge("ridge_path", WALL, RIDGE, w - 2 * WALL),
        solid("stone_wall_1", 600, g - 48, 32, 48),
        solid("shepherds_hut", HUT[0], HUT[2], HUT[1] - HUT[0], g - HUT[2]),
        *[ledge(f"oak_limb_{n}", x, y, LIMB_W) for n, (x, y) in enumerate(OAK_LIMBS)],
        door("meadow_to_hobford", "the hill path down to Hobford", 1420, g, VILLAGE, "hobford_from_meadow"),
        sign("meadow_sign_hobford", 1444, g - 140, "HOBFORD", 140),
        solid("stone_wall_2", 1600, g - 48, 32, 48),
        solid("turf_bank", 1800, g - 64, 320, 64),
        npc("npc_companion_dog", "hobford_dog", "Greet the dog", 1900, g - 64, brain="companion_dog_roam", w=64, h=64),
        sign("meadow_sign_ring", 2240, g - 160, "THE RING", 160),
        edge("meadow_to_clearing", "on to the ring", w - WALL, g, CLEARING, "clearing_from_meadow"),
        edge("meadow_to_clearing_high", "along the ridge", w - WALL, RIDGE, CLEARING, "clearing_from_meadow_high"),
        start(rid, 120, g),
    ]
    return build(rid, e, "THE HIGH MEADOW", COUNTRY_MUSIC, dangerous=True)


# ------------------------------------------------------ the gate clearing

#: The boom across the road beside the guard post: too high to jump, and
#: lifted by the lever in the post's yard. The post's roof is reached from
#: the ridge path; the siding's back stair comes up in the yard as well.
BARRIER_X = 1560
BARRIER_H = 176
POST_ROOF = (1380, BARRIER_X, COUNTRY_FLOOR - 192)
BARRIER_LEVER = "hobford_barrier_lever"
GATE_ZONE = "hobford_gate_zone"
GATE_TERMINAL = "hobford_gate_terminal"


def clearing():
    """THE GATE CLEARING. The old ring in its ruin of standing stones, with
    new steel on it: the guard post, the boom across the road, the freight
    rail's stair down to the siding. The ring is behind the boom."""
    rid = CLEARING
    w, h, g = COUNTRY_W, COUNTRY_H, COUNTRY_FLOOR
    check_reach(rid, [("clearing", g), ("stone", g - 48), ("clearing", g)])
    ring_x = 1780
    e = [
        *walls(w, g, west=[g, RIDGE]),
        solid("ground", 0, g, w, h - g),
        edge("clearing_from_meadow", "back down the track", 0, g, MEADOW, "meadow_to_clearing"),
        edge("clearing_from_meadow_high", "along the ridge", 0, RIDGE, MEADOW, "meadow_to_clearing_high"),
        # The ridge path ends over the guard post: a drop from its end lands
        # on the roof, and the roof's east end is over the boom.
        ledge("ridge_path", WALL, RIDGE, 1600 - WALL),
        solid("standing_stone_1", 560, g - 48, 48, 48),
        solid("standing_stone_2", 880, g - 48, 48, 48),
        door("clearing_to_siding", "the stair down to the freight siding", 1180, g, SIDING, "siding_from_clearing"),
        sign("clearing_sign_siding", 1204, g - 140, "FREIGHT SIDING", 220),
        ledge("guard_post_roof", POST_ROOF[0], POST_ROOF[2], POST_ROOF[1] - POST_ROOF[0]),
        sign("clearing_sign_post", 1470, POST_ROOF[2] - 60, "GATE OFFICE. PERSONS BY APPOINTMENT.", 360),
        entity("LockWall", BARRIER_X, g - BARRIER_H, 24, BARRIER_H, id="hobford_barrier", name="the barrier",
               gated_by=f"world.switch_on {BARRIER_LEVER}"),
        entity("Switch", 1630, g - 32, 24, 32, id=BARRIER_LEVER, name="the barrier lever", prompt="Lift the barrier",
               action="ToggleFlag"),
        # The ring: a dialed ring of the gate network (`gate_network.ron`,
        # `gate_portals.ron`), the props it is drawn with, and its terminal.
        entity("Prop", ring_x, g - 288, 288, 288, name="Hobford Ring", kind="triangle_gate_ring"),
        entity("Prop", ring_x, g - 288, 288, 288, name="Hobford Portal", kind="triangle_gate_portal"),
        entity("LoadingZone", ring_x + 72, g - 288, 144, 288, id=GATE_ZONE, name="the ring", activation="Door",
               presentation="SceneArt"),
        entity("Prop", 1690, g - 56, 64, 56, name="Hobford Dialer", kind="gate_dialer_triangle"),
        entity("Switch", 1710, g - 44, 24, 32, id=GATE_TERMINAL, name="Hobford Ring terminal", prompt="Dial the gate",
               action="GateTerminal"),
        sign("clearing_sign_ring", ring_x + 144, g - 340, "HOBFORD RING. FREIGHT WINDOW ON THE BOARD.", 420),
        door("clearing_post_yard_door", "the back stair down to the siding", 2200, g, SIDING, "siding_to_post_yard"),
        start(rid, 120, g),
    ]
    return build(rid, e, "THE GATE CLEARING", COUNTRY_MUSIC, dangerous=True)


# ------------------------------------------------------ the freight siding

YARD_FIGHT = "intro_freight_yard_fight"
#: The freight stacked on the platform: (name, x0, x1, top). Solid crates on
#: the floor and one-way pallets over them.
FREIGHT = [("crate_a", 700, 796, LOW_FLOOR - 48), ("crate_b", 1240, 1336, LOW_FLOOR - 48)]
PALLETS = [("pallets_a", 820, 980, LOW_FLOOR - 112), ("pallets_b", 1360, 1520, LOW_FLOOR - 112)]


def siding():
    """THE FREIGHT SIDING. The new platform under the clearing, where the
    goblins wait for the freight window with their handcart and the crate
    from the barn. The fight starts on the platform; its bell keeps it won
    (an encounter with no linked switch starts again whenever a player walks
    back into its trigger)."""
    rid = SIDING
    _, (w, h) = ROOMS_AT[rid]
    g = LOW_FLOOR
    check_reach(rid, [("platform", g), ("crate a", FREIGHT[0][3]), ("pallets a", PALLETS[0][3])])
    e = [
        *walls(w, g, west=[g]),
        solid("platform", 0, g, w, h - g),
        edge("siding_from_woods", "back along the trail", 0, g, WOODS, "woods_to_siding"),
        door("siding_from_clearing", "up the stair to the clearing", 120, g, CLEARING, "clearing_to_siding"),
        entity("CutsceneTrigger", 300, 32, 64, g - 32, cutscene="foreman_siding"),
        entity("EncounterTrigger", 440, 32, 64, g - 32, id=YARD_FIGHT, name=f"{YARD_FIGHT}_trigger"),
        *[solid(n, x0, top, x1 - x0, g - top) for n, x0, x1, top in FREIGHT],
        *[ledge(n, x0, top, x1 - x0) for n, x0, x1, top in PALLETS],
        sign("siding_sign_platform", 960, 120, "FREIGHT ONLY. NO PERSONS ON THE PLATFORM.", 420),
        entity("CutsceneTrigger", 1480, 32, 64, g - 32, cutscene="work_order"),
        entity("ChestSpawn", 1560, g - 58, 76, 58, name="the goblins' crate", reward="flag:intro_creator_notes_recovered"),
        sign("siding_sign_crate", 1598, g - 120, "1 LAB OF RESEARCH. PAID.", 280),
        entity("Switch", 1700, g - 32, 24, 32, id=f"{YARD_FIGHT}_again", name="the platform bell",
               prompt="Ring the platform bell", target_encounter=YARD_FIGHT, action="ResetEncounter"),
        door("siding_to_post_yard", "the back stair up to the gate office", 1800, g, CLEARING, "clearing_post_yard_door"),
        start(rid, 200, g),
    ]
    return build(rid, e, "THE FREIGHT SIDING", GOBLIN_MUSIC, dangerous=True)


# ------------------------------------------------------- the millstream

#: The stream: its banks are level with the ground, its bed is 96 down, and
#: stepping stones cross it flush with the banks. Rocks in the bed at each
#: bank are the way out of the water.
STREAM = (500, 1300, LOW_FLOOR + 96)
STONES = [(600, 664), (760, 824), (920, 984), (1080, 1144), (1220, 1270)]


def millstream():
    """THE MILLSTREAM. The bank path comes down from the lane; stepping
    stones cross the stream; past it the mill, whose porch and upper floor
    are a climb. Under the west bank a cracked wall faces the water."""
    rid = MILLSTREAM
    w, h, g = COUNTRY_W, LOW_H, LOW_FLOOR
    s0, s1, s_bed = STREAM
    check_reach(rid, [("bed", s_bed), ("rock", s_bed - 48), ("bank", g)])
    check_reach(rid, [("bank", g), ("porch", g - 48), ("upper floor", g - 112), ("loft window", g - 176)])
    e = [
        *walls(w, g, east=[g]),
        door("millstream_from_lane", "the bank path up to the lane", 120, g, LANE, "lane_to_millstream"),
        # The west bank, with a dry hollow under it behind a cracked wall.
        solid("west_bank", 0, g, 420, h - g),
        solid("hollow_roof", 420, g, s0 - 420, 16),
        solid("hollow_floor", 420, s_bed, s0 - 420, h - s_bed),
        entity("BreakablePlatform", s0 - 16, g + 16, 16, s_bed - g - 16, id="millstream_cracked_wall",
               name="a cracked wall", max_hp=3.0, respawn="Persistent", collision="Solid", trigger="OnHit"),
        entity("PickupSpawn", 440, s_bed - 28, 24, 24, name="a jar of coins", kind="currency:25"),
        solid("stream_bed", s0, s_bed, s1 - s0, h - s_bed),
        water(f"{rid}_stream", s0, g + 8, s1 - s0, s_bed - g - 8),
        solid("rock_west", s0, s_bed - 48, 48, 48),
        solid("rock_east", s1 - 48, s_bed - 48, 48, 48),
        *[solid(f"stone_{n}", x0, g, x1 - x0, s_bed - g) for n, (x0, x1) in enumerate(STONES)],
        solid("east_bank", s1, g, w - s1, h - g),
        ledge("mill_porch", 1520, g - 48, 160),
        ledge("mill_upper_floor", 1600, g - 112, 220),
        ledge("mill_loft_window", 1720, g - 176, 120),
        entity("PickupSpawn", 1800, g - 176 - 28, 24, 24, name="a few coins", kind="currency:10"),
        sign("millstream_sign_mill", 1700, g - 260, "HOBFORD MILL. FLOUR, FEED, NO CREDIT.", 380),
        edge("millstream_to_hobford", "on into Hobford", w - WALL, g, VILLAGE, "hobford_from_millstream"),
        start(rid, 240, g),
    ]
    return build(rid, e, "THE MILLSTREAM", COUNTRY_MUSIC, dangerous=True)


# --------------------------------------------------------------- Hobford

#: The houses of the street: (name, porch x, roof x0, roof x1). A porch is 48
#: over the street and a roof 64 over its porch.
HOUSES = [("cottage", 260, 300, 540), ("smithy", 860, 900, 1160), ("inn", 1460, 1500, 1800)]


def village():
    """HOBFORD. A short street: cottages, the old smithy that sells gate
    goods now, the well, the inn, the notice board. The hill path goes up to
    the meadow; east the road goes into the woods."""
    rid = VILLAGE
    w, h, g = COUNTRY_W, LOW_H, LOW_FLOOR
    check_reach(rid, [("street", g), ("porch", g - 48), ("roof", g - 112), ("loft", g - 176)])
    e = [
        *walls(w, g, west=[g], east=[g]),
        solid("street", 0, g, w, h - g),
        edge("hobford_from_millstream", "back to the millstream", 0, g, MILLSTREAM, "millstream_to_hobford"),
        *[ledge(f"{n}_porch", px, g - 48, 80) for n, px, _, _ in HOUSES],
        *[ledge(f"{n}_roof", x0, g - 112, x1 - x0) for n, _, x0, x1 in HOUSES],
        ledge("smithy_loft", 1000, g - 176, 120),
        entity("PickupSpawn", 1060, g - 176 - 28, 24, 24, name="a dropped purse", kind="currency:20"),
        solid("well", 1250, g - 48, 64, 48),
        sign("hobford_sign_smithy", 1030, g - 150, "GATE GOODS: LAMP OIL, SALT, BATTERIES", 380),
        sign("hobford_sign_inn", 1650, g - 150, "THE PLOUGH", 160),
        sign("hobford_board_1", 2000, g - 200, "FREIGHT WINDOW: TOMORROW, NOON.", 360),
        sign("hobford_board_2", 2000, g - 170, "LOST: ONE SPECKLED HEN. ASK AT THE PLOUGH.", 420),
        sign("hobford_board_3", 2000, g - 140, "STRANGERS AT THE RING: SEE THE GATE OFFICE.", 440),
        door("hobford_from_meadow", "the hill path up to the meadow", 2160, g, MEADOW, "meadow_to_hobford"),
        edge("hobford_to_woods", "the road into the woods", w - WALL, g, WOODS, "woods_from_hobford"),
        start(rid, 120, g),
    ]
    return build(rid, e, "HOBFORD", VILLAGE_MUSIC)


# ------------------------------------------------------------ the woods

BOB_X = 1240
#: The hollow oak: a climb up inside its trunk to a nook (a secret).
HOLLOW = [(1700, LOW_FLOOR - 64), (1600, LOW_FLOOR - 128), (1700, LOW_FLOOR - 192)]


def woods():
    """HOBFORD WOODS. Roots and a fallen trunk, Bob's survey camp in a
    clearing, a hollow oak, and the goblins' trail east to the siding, where
    one goblin keeps a lookout."""
    rid = WOODS
    w, h, g = COUNTRY_W, LOW_H, LOW_FLOOR
    check_reach(rid, [("floor", g), ("root", g - 48), ("floor", g), ("trunk", g - 64), ("floor", g)])
    check_reach(rid, [("floor", g), *[(f"hollow {n}", y) for n, (_, y) in enumerate(HOLLOW)]])
    e = [
        *walls(w, g, west=[g], east=[g]),
        solid("floor", 0, g, w, h - g),
        edge("woods_from_hobford", "back to Hobford", 0, g, VILLAGE, "hobford_to_woods"),
        solid("root_1", 420, g - 48, 64, 48),
        ledge("fallen_trunk", 640, g - 64, 240),
        solid("root_2", 1000, g - 48, 64, 48),
        npc("npc_bob", "bob_woods", "Talk to Bob", BOB_X, g),
        sign("woods_sign_camp", BOB_X + 100, g - 150, "SURVEY CAMP. DON'T TOUCH THE STAFF.", 360),
        *[ledge(f"hollow_oak_{n}", x, y, 96) for n, (x, y) in enumerate(HOLLOW)],
        entity("PickupSpawn", 1740, HOLLOW[-1][1] - 28, 24, 24, name="a can of oil", kind="health:2"),
        hen(rid, 1, 1880, g, dialogue="hobford_lost_hen"),
        raider(rid, 1, 2160, g),
        edge("woods_to_siding", "along the goblins' trail", w - WALL, g, SIDING, "siding_from_woods"),
        start(rid, 120, g),
    ]
    return build(rid, e, "HOBFORD WOODS", COUNTRY_MUSIC, look=WOODS_LOOK, dangerous=True)


# ------------------------------------------- the town under the gate stack

STREET = 608
BOSS = "first_system_boss"
#: Oiler's post: he stands at his workshop, and the volume round it starts
#: his line when a player comes up to him.
OILER_X = 1100


def market():
    """THE DRAIN MARKET. A street under the gate stack, in the town past
    level 1: stalls with awnings over it, Oiler's workshop, the news board,
    the drain cover down to the culvert. East is the gate stack."""
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
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("east_wall", w - WALL, 32, WALL, g - 96 - 32),
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
        npc("npc_oiler", "oiler_intro", "Talk to Oiler", OILER_X, g, brain="meets_the_player"),
        entity("ShrineSpawn", OILER_X + 80, g - 80, 44, 80, id="drain_alley_oiler_bench", name="Oiler's bench"),
        entity("CutsceneTrigger", OILER_X - 140, g - 176, 288, 176, cutscene="oiler_notices"),
        sign("market_sign_oiler", OILER_X + 40, g - 200, "OILER: REPAIRS. KNEES, PIPES, DOORS. NO SHARKS.", 420),
        entity("LoadingZone", 1300, g - 96, 48, 96, id="drain_from_boss_return", name="the service door", activation="Door",
               target_room=BOSS, target_zone="boss_return_to_drain", bidirectional=True),
        sign("market_sign_food", 300, g - 230, "No swordguns inside the food court", 380),
        sign("market_sign_ripples", 1180, 120, "Report unstable ripples to platform staff", 420),
        sign("market_sign_gates", 1330, g - 160, "GATES", 120),
    ]
    return undertown(rid, e, "THE DRAIN MARKET", extra='\n    entry_cutscene: "drain_market_arrival",')


#: The culvert's far walk.
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
    of the way, crossed on stepping stones and, at its widest, on a raft, to
    a dead end where a goblin lookout listens."""
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
        solid("east_wall", w - WALL, 32, WALL, h - 32),
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
        start(rid, 140, upper),
        slug(rid, 1, 420, mid),
        slug(rid, 2, 600, mid),
        raider(rid, 1, 1480, DRAIN_WALK, character="goblin"),
        sign("culvert_sign_cover", 120, upper - 140, "MARKET", 140),
        sign("culvert_sign_sump", 1040, stone - 120, "SUMP. KEEP OUT.", 220),
    ]
    return undertown(rid, e, "THE CULVERT", dangerous=True)


ROOMS = (workshop, lane, meadow, clearing, siding, millstream, village, woods, market, culvert)


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
