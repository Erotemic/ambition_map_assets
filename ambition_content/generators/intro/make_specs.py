#!/usr/bin/env python3
r"""Write the rooms of level 1, Hobford: the Creator's workshop and the hill
country round the village, and the two town rooms under the gate stack that
this script also owns.

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/intro/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/intro/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Design: `docs/planning/game/level-1.md`.

                                                                                                                   [the fell's top]
                                                                                                    the drove road up /
    [workshop]--[Hobford Lane]                                  [the high meadow]--[the gate clearing]              /
                       \ the bank path down             the hill path up /                   \ the freight track down
                        [the millstream]--[Hobford]--[the woods]                              [the freight siding]--[the fell]

    One line of rooms, west to east: the barn on the west hill, the valley,
    the gate on the east hill, and past the siding the fell, the mountain
    beside the gate's hill. Each room joins the next by an edge at one
    height; a hill room (the lane, the meadow, the clearing) holds both
    heights and climbs between them on slopes.

THE KIT. Every required way is made for run, ONE jump, drop through a
one-way floor and the strike, and each level-1 room withholds the rest of a
player's kit (`SMALL_KIT_WITHHELD`, the level field `withheld_verbs`). A jump
rises about 88 px (jump 630 px/s, gravity 2250); a level gap of 112 px or
less is safe at a run (270 px/s). `check_reach` refuses a required step up of
more than 64 px; it compares heights only, so each required way is also
walked by `walked_route_census` under the level's kit.

NO ROUTE WAITS ON A STORY FACT. A wall here is a barrier on a lever beside
it, a door the raid breaks, or a survey line pegged across the lane, low
enough to step over, that comes up when the survey is over.

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
from district_scenery import piece  # noqa: E402

WORLD_LDTK = WORLDS / "intro.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/intro/make_specs.py"

WORKSHOP = "intro_wake_room"
LANE = "intro_hobford_lane"
MEADOW = "intro_high_meadow"
CLEARING = "intro_gate_clearing"
SIDING = "intro_freight_yard"
FELL = "intro_fell"
MILLSTREAM = "intro_millstream"
VILLAGE = "intro_hobford"
WOODS = "intro_woods"
SALT_RUN = "intro_salt_run"
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
#: The country without the gate, behind the rooms where the gate itself
#: stands in the play (level field `backdrop`; the skin stays the country's).
GATESIDE = '\n    backdrop: "hobford_gateside",'
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

#: THE NAMES TABLE. Level 1's place names are placeholders (Jon,
#: 2026-11-14), so every sign, room title and zone name says them from here;
#: the dialogue's are in `dialogue/sandbox/names.yarn`. Ids never carry them.
VILLAGE_NAME = "Hobford"

#: The level is in a band of its own below the town: the hilltops' ground
#: (the workshop's floor, the top of the lane, the meadow and the clearing)
#: is at world y 2720, the valley's (the millstream, Hobford, the woods, the
#: siding) at 3328. A valley room is the lower band; a hill room spans both.
UPPER_Y, LOWER_Y = 2048, 2816
COUNTRY_W, COUNTRY_FLOOR = 2400, 672
LOW_H, LOW_FLOOR = 640, 512
WORKSHOP_W, WORKSHOP_H, WORKSHOP_FLOOR = 1920, 448, 352
#: A hill room: from the top of the upper band to the bottom of the lower.
#: Its hilltop floor is `COUNTRY_FLOOR`, its valley floor `VALLEY_FLOOR`.
HILL_H = LOWER_Y + LOW_H - UPPER_Y
VALLEY_FLOOR = LOWER_Y + LOW_FLOOR - UPPER_Y
LANE_W, MEADOW_W, CLEARING_W, SIDING_W = 3328, 3104, 4368, 1920
#: The fell: the mountain east of the siding. It rises 768 over the upper
#: band, so its summit stands well above the gate's hill; its valley floor is
#: the siding's.
FELL_W, FELL_Y = 3600, UPPER_Y - 768
FELL_H = LOWER_Y + LOW_H - FELL_Y
FELL_FLOOR = LOWER_Y + LOW_FLOOR - FELL_Y

#: Where the country's rooms begin in the world: the lane's west edge. The
#: workshop is west of it, ending there.
COUNTRY_X = 1600

#: The salt run, under the valley: its west end under the millstream's
#: hollow (400 into the millstream), its east end under the woods' hollow
#: oak. Its top is the valley rooms' bottom.
SALT_RUN_X = COUNTRY_X + LANE_W + 400
SALT_RUN_W = 3 * COUNTRY_W - 400 - (COUNTRY_W - 1840)


def _line(*rooms):
    """Each room of the line: its top left in the world and its size, from
    the west, each one's west side at the last one's east side."""
    out, x = {}, COUNTRY_X
    for rid, y, size in rooms:
        out[rid] = ((x, y), size)
        x += size[0]
    return out


#: Each room: where it is in the world (its top left), and its size.
ROOMS_AT = {
    WORKSHOP: ((COUNTRY_X - WORKSHOP_W, UPPER_Y + COUNTRY_FLOOR - WORKSHOP_FLOOR), (WORKSHOP_W, WORKSHOP_H)),
    **_line(
        (LANE, UPPER_Y, (LANE_W, HILL_H)),
        (MILLSTREAM, LOWER_Y, (COUNTRY_W, LOW_H)),
        (VILLAGE, LOWER_Y, (COUNTRY_W, LOW_H)),
        (WOODS, LOWER_Y, (COUNTRY_W, LOW_H)),
        (MEADOW, UPPER_Y, (MEADOW_W, HILL_H)),
        (CLEARING, UPPER_Y, (CLEARING_W, HILL_H)),
        (SIDING, LOWER_Y, (SIDING_W, LOW_H)),
        (FELL, FELL_Y, (FELL_W, FELL_H)),
    ),
    # The salt run: under the valley, from behind the mill wheel to the
    # woods' hollow oak.
    SALT_RUN: ((SALT_RUN_X, LOWER_Y + LOW_H), (SALT_RUN_W, LOW_H)),
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


#: The steepest a path may climb (about 23°): a walker stands on 50°, but a
#: path is walked, not scrambled, and steeper pitches (28°, 30°) snagged a
#: walker on the corner where the slope meets the block at its top.
MAX_SLOPE = 0.42
#: Each slope runs on flat this far over the block top at each end, so a
#: body crossing the join stands exactly at the block's height.
SLOPE_STUB = 32


def slope(name, x0, y0, x1, y1):
    """A path that climbs or falls: the top of the ground from (x0, y0) to
    (x1, y1), west to east, drawn as the hill it is (the earth under it is
    filled). Each end meets the flat top of a block, where a walker, and the
    navigation graph, steps on and off it; the line goes on `SLOPE_STUB` along
    each block top."""
    if x1 <= x0 or abs(y1 - y0) > MAX_SLOPE * (x1 - x0):
        raise SystemExit(f"{name}: ({x0},{y0}) to ({x1},{y1}) is steeper than {MAX_SLOPE} or not west to east")
    # The blocks a slope joins are IntGrid cells, so their ends are on the
    # 16 px grid. An end off it leaves a block corner standing out of the
    # slope (2992..3424 under a line from 3418): a step a climber walks into.
    if any(v % 16 for v in (x0, y0, x1, y1)):
        raise SystemExit(f"{name}: ({x0},{y0}) to ({x1},{y1}) has an end off the 16 px grid")
    points = f"{x0 - SLOPE_STUB},{y0}; {x0},{y0}; {x1},{y1}; {x1 + SLOPE_STUB},{y1}"
    return entity("SurfaceChain", x0, min(y0, y1) - 16, 16, 16, name=name, points=points, fill=True)


def hill_walls(w, west, east):
    """The side walls of a hill room over the floor each side's edge stands
    on (the ground under each floor is the room's)."""
    return [solid(f"{side}_wall", x, 0, WALL, floor - 96)
            for side, x, floor in (("west", 0, west), ("east", w - WALL, east))]


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


def sheep(x, floor):
    """A sheep of the shepherd's flock. It grazes a long while and ambles
    slowly to another place it can walk to; it cannot jump a wall."""
    return npc("npc_fell_sheep", "hobford_sheep", "Look at the sheep", x, floor, w=56, h=34)


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
#: back too; the level teaches the plain strike first. The shot (`ranged`) is
#: held back: level 1 is melee only.
SMALL_KIT_WITHHELD = (
    "double_jump wall_jump wall_cling wall_climb ledge_grab dash double_dash dodge "
    "fly fly_toggle glide blink precision_blink blink_through_soft_walls "
    "blink_through_hard_walls pogo directional_special shield grab morph ranged"
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
#: it): its bed, and the ramp let down from its back end. It stands beside
#: the Creator, so the first view holds Scout waking and him at his bench.
CART_BED = (720, 896, 294)
CART_RAMP_FOOT = 998
#: The test plinth: the first jump, a step of 48, west of the cart.
PLINTH = (540, 620, WORKSHOP_FLOOR - 48)
#: Up to the loft at the west end: a crate (48), then the loft boards (64
#: more). The gauge is at the far end of the boards.
LOFT_CRATE = (396, 460, WORKSHOP_FLOOR - 48)
LOFT = (120, 420, WORKSHOP_FLOOR - 112)
#: The Creator, and his bench between him and the barn door.
CREATOR_X = 700
BENCH = (1100, 1220, WORKSHOP_FLOOR - 48)
#: The barn door, and the yard outside it. The raiders come up the yard, out
#: of shot while Scout is in the barn (its camera zone ends at the door), and
#: walk in at the door when it breaks: the camera already holds the door.
BARN_DOOR_X = 1320
DOOR_H = 112
#: The yard's gate stands until the raid's last raider has run out through it
#: with the case (`intro_raider_runs_with_the_case`, when the other two have
#: fallen, opens it first), so no one leaves the yard mid-fight. The Creator's last words
#: open it too, for a raid whose last two fell together.
YARD_GATE_X = 1840
CASE_TAKEN = "intro_case_taken"
RAID = "intro_workshop_raid"
#: The story calls the raid: the Creator hears the cart (his talk), or Scout
#: goes to the barn door without talking to him (`intro_raid_at_the_door`).
#: The room starts the raid while this is set (`while_live_when`); a won raid
#: spawns finished, so it does not start again.
RAIDERS_COMING = "intro_raiders_coming"
#: The raiders break the barn door's bar, a beat after they are called, so
#: the door is down when they reach it.
DOOR_BROKEN = "intro_barn_door_broken"


def workshop():
    """THE WORKSHOP. The Creator's barn outside Hobford: the loft, the test
    plinth, the charging cart, his bench, the barred barn door, and the yard
    outside. The raid is called in his conversation, at the end of his
    questions, or when Scout goes to the barn door without talking to him
    (the cutscene in front of it); the room's line starts it then. The
    goblins come up the yard either way and break the door's bar."""
    rid = WORKSHOP
    w, h, g = WORKSHOP_W, WORKSHOP_H, WORKSHOP_FLOOR
    x0, x1, bed = CART_BED
    check_reach(rid, [("floor", g), ("plinth", PLINTH[2]), ("floor", g), ("crate", LOFT_CRATE[2]), ("loft", LOFT[2]),
                      ("floor", g), ("bench", BENCH[2]), ("floor", g)])
    front = BARN_DOOR_X + 24
    e = [
        # The barn: its roof ends at its front wall; the yard is open.
        solid("roof", 0, 0, front, 32),
        solid("west_wall", 0, 32, WALL, g - 32),
        solid("barn_front", BARN_DOOR_X, 32, 24, g - DOOR_H - 32),
        solid("yard_east_wall", w - WALL, 0, WALL, g - 96),
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
        entity("PlayerStart", x0 + 74, 248, 28, 46, name="wake_room_spawn"),
        # The hub's door comes out here (one way: nothing leads back).
        entity("LoadingZone", x0 + 64, 198, 48, 96, id="wake_room_arrival", name="wake room arrival", activation="Door",
               presentation="SceneArt"),
        sign("workshop_sign_cart", x0 + 128, 120, "DO NOT SWITCH ON UNTIL FINISHED", 300),
        solid("test_plinth", PLINTH[0], PLINTH[2], PLINTH[1] - PLINTH[0], g - PLINTH[2]),
        sign("workshop_sign_plinth", 580, PLINTH[2] - 60, "LOAD TEST", 140),
        sign("intro_training_landing", (PLINTH[0] + PLINTH[1]) // 2, PLINTH[2] - 12, "▼", 24),
        solid("loft_crate", LOFT_CRATE[0], LOFT_CRATE[2], LOFT_CRATE[1] - LOFT_CRATE[0], g - LOFT_CRATE[2]),
        ledge("parts_loft", LOFT[0], LOFT[2], LOFT[1] - LOFT[0]),
        # On the loft: the torque gauge he sends Scout for, at the far end of
        # the boards, and an oil can by the crate.
        entity("PickupSpawn", 148, LOFT[2] - 28, 24, 24, name="the torque gauge", kind="flag:intro_torque_gauge_found"),
        entity("PickupSpawn", 372, LOFT[2] - 28, 24, 24, name="a can of oil", kind="health:2"),
        sign("workshop_sign_loft", 270, LOFT[2] - 60, "GAUGES GO BACK ON THE SHELF", 300),
        npc("npc_creator", "creator_intro", "Talk to the Creator", CREATOR_X, g),
        sign("intro_practice_station", 700, g - 90, "PRACTICE", 140),
        entity("EnemySpawn", 463, g - 56, 34, 56, name="workshop_practice_bag",
               brain="sandbag_infinite", character_id="practice_sandbag", respawn="OnRoomReenter"),
        sign("workshop_sign_sandbag", 480, g - 100, "STRIKE TEST", 140),
        sign("intro_bench_station", 1060, g - 90, "TEST NOTES", 160),
        sign("intro_raider_station", 1260, g - 80, "KEEP CLEAR", 140),
        # The bench top is a board on trestles: bodies go under it, so it
        # stands between the Creator and the door without barring the way.
        ledge("bench", BENCH[0], BENCH[2], BENCH[1] - BENCH[0]),
        sign("workshop_sign_bench", 1160, BENCH[2] - 60, "LOGS. DO NOT TIDY.", 220),
        # The raid: its trigger is in the roof, where no body goes, so only
        # the room's line starts it (`while_live`, when the story calls it).
        entity("EncounterTrigger", 64, 0, 32, 32, id=RAID, name=f"{RAID}_trigger"),
        # Stop an approach before the doorway. The arriving raiders need
        # space between their mark and Scout when control returns.
        entity("CutsceneTrigger", BENCH[1] - 64, 32, BARN_DOOR_X - BENCH[1] + 64, g - 32,
               cutscene="intro_raid_at_the_door"),
        # A blow on the whistle a raider dropped calls the raid again: the
        # reset puts it back to the start, and the room's line starts it.
        entity("Switch", 680, g - 32, 24, 32, id=f"{RAID}_again", name="a raider's whistle",
               prompt="Blow the whistle", target_encounter=RAID, action="ResetEncounter"),
        entity("LockWall", BARN_DOOR_X, g - DOOR_H, 24, DOOR_H, id="intro_barn_door", name="the barn door",
               gated_by=f"world.flag_set {DOOR_BROKEN}"),
        sign("workshop_sign_door", BARN_DOOR_X - 150, 120, "TEST IN PROGRESS. DOOR BARRED.", 320),
        # Inside the barn the camera stops at the barn's front wall, so the
        # yard is out of shot until Scout goes out into it: the raiders come
        # up the yard unseen and are first seen in the doorway.
        entity("CameraZone", 0, 0, front, h, id="intro_barn_camera", name="the barn", mode="Default",
               clamp_mode="zone_bounds"),
        # His last words, the moment the fight is won, wherever in the barn
        # or the yard Scout is: a fight carries Scout out into the yard, and a
        # strip at the door was already behind him.
        entity("CutsceneTrigger", WALL, 32, w - 2 * WALL, g - 32, cutscene="creator_final_fragment", after_encounter=RAID),
        entity("LockWall", YARD_GATE_X, g - 96, 24, 96, id="intro_yard_gate", name="the yard gate",
               gated_by=f"world.flag_set {CASE_TAKEN}"),
        edge("workshop_to_lane", "out into the lane", w - WALL, g, LANE, "lane_from_workshop"),
    ]
    return build(rid, e, "THE WORKSHOP", WORKSHOP_MUSIC, look=WORKSHOP_LOOK, bg=BG, dangerous=True,
                 extra=('\n    entry_cutscene: "intro_wake",'
                        f'\n    while_live: "encounter.start encounter:{RAID}",'
                        f'\n    while_live_when: "world.flag_set {RAIDERS_COMING}",'))


# ------------------------------------------------------------- the lane

#: Alice's survey line, pegged across the lane west of her station: a step
#: over, and Scout is asked not to tread on it. It comes up when Bob's end
#: of the survey is closed (`bob_field_survey_received`).
SURVEY_LINE = "alice_survey_line"
SURVEY_LINE_X = 700
ALICE_X = 940
#: The bank path down from the barn's level to the stream's: two pitches,
#: and a landing between them where the mill's sign stands.
BANK_TOP = 1200
BANK_LANDING = (1952, 2368, COUNTRY_FLOOR + 304)
BANK_FOOT = 3120


#: How far up the camera looks on a hilltop (world px, negative is up): the
#: lane, the meadow's top and the clearing's road each have a lookout zone.
LOOKOUT_LIFT = -180


def stake_board(name, cx, ground, first, second):
    """A board on stakes with its middle at `cx`, standing on `ground`, and
    its two lines of words on it."""
    return [piece("hill_stake_board", cx - 100, ground - 100, name=name),
            sign(f"{name}_1", cx, ground - 92, first, 180),
            sign(f"{name}_2", cx, ground - 68, second, 180)]


def lane():
    """HOBFORD LANE. The first open air: the lane outside the barn, high on
    the west hill, with the valley below it (the village roofs, the mill) and
    the gate far off on the east hill. Alice's station is beside the lane and
    her survey line is pegged across it. Past her the bank path goes down to
    the mill in two pitches."""
    rid = LANE
    w, h, hi, lo = LANE_W, HILL_H, COUNTRY_FLOOR, VALLEY_FLOOR
    l0, l1, ly = BANK_LANDING
    e = [
        *hill_walls(w, hi, lo),
        solid("barn_level", 0, hi, BANK_TOP, h - hi),
        edge("lane_from_workshop", "into the workshop", 0, hi, WORKSHOP, "workshop_to_lane"),
        hen(rid, 1, 260, hi),
        hen(rid, 2, 420, hi),
        entity("LockWall", SURVEY_LINE_X, hi - 24, 16, 24, id=SURVEY_LINE, name="the survey line",
               gated_by="bob_field_survey_received"),
        *stake_board("lane_sign_line", SURVEY_LINE_X - 110, hi, "SURVEY LINE", "DON'T STEP ON IT"),
        piece("hill_survey_station", 960, 560),
        npc("npc_alice", "alice_lane", "Talk to Alice", ALICE_X, hi, brain="meets_the_player"),
        *stake_board("lane_sign_station", ALICE_X - 110, hi, "SURVEY STATION", "MIND THE TRIPOD"),
        slope("bank_path_upper", BANK_TOP, hi, l0, ly),
        solid("bank_landing", l0, ly, l1 - l0, h - ly),
        # The way down to the mill, on a fingerpost on the landing.
        piece("hill_fingerpost", (l0 + l1) // 2 - 75, ly - 120, name="the mill's fingerpost"),
        sign("lane_sign_mill", (l0 + l1) // 2 + 3, ly - 109, "THE MILL", 90),
        slope("bank_path_lower", l1, ly, BANK_FOOT, lo),
        solid("valley_floor", BANK_FOOT, lo, w - BANK_FOOT, h - lo),
        edge("lane_to_millstream", "down to the mill", w - WALL, lo, MILLSTREAM, "millstream_from_lane"),
        start(rid, 120, hi),
        # The first view outside: on the hilltop the camera looks out, not
        # down. Framed on Scout, the hill's earth filled the lower half and
        # hid the valley, the village and the gate in the background; lifted,
        # the ground is low in the frame and the world is above it.
        entity("CameraZone", 0, 0, l0, h, id="intro_lane_lookout", name="the lookout", mode="Default",
               target_offset_y=LOOKOUT_LIFT),
    ]
    return build(rid, e, f"{VILLAGE_NAME.upper()} LANE", COUNTRY_MUSIC, dangerous=True)


# ----------------------------------------------------------- the meadow

#: The hill path from the woods up to the hilltop: two pitches, and the
#: shepherd's terrace between them with his hut (a step of 64) on it.
HILL_FOOT, HILL_TOP = 400, 2512
TERRACE = (1152, 1760, VALLEY_FLOOR - 304)
HUT = (1392, 1568, VALLEY_FLOOR - 304 - 64)


def meadow():
    """THE HIGH MEADOW. The hill path climbs out of the woods to the pasture
    on the east hill: the shepherd's terrace halfway up, with his hut, the
    oak and the dog; at the top a dry-stone wall to hop, and the road on to
    the gate."""
    rid = MEADOW
    w, h, hi, lo = MEADOW_W, HILL_H, COUNTRY_FLOOR, VALLEY_FLOOR
    t0, t1, ty = TERRACE
    check_reach(rid, [("terrace", ty), ("hut roof", HUT[2]), ("terrace", ty)])
    check_reach(rid, [("hilltop", hi), ("wall", hi - 48), ("hilltop", hi)])
    e = [
        *hill_walls(w, lo, hi),
        solid("valley_floor", 0, lo, HILL_FOOT, h - lo),
        edge("meadow_from_woods", "back down into the woods", 0, lo, WOODS, "woods_to_meadow"),
        slope("hill_path_lower", HILL_FOOT, lo, t0, ty),
        solid("shepherds_terrace", t0, ty, t1 - t0, h - ty),
        piece("hill_meadow_oak", 1180, ty - 472),
        solid("shepherds_hut", HUT[0], HUT[2], HUT[1] - HUT[0], ty - HUT[2]),
        piece("hill_meadow_hut", HUT[0], HUT[2]),
        npc("npc_companion_dog", "hobford_dog", "Greet the dog", 1680, ty, brain="companion_dog_roam", w=64, h=64),
        slope("hill_path_upper", t1, ty, HILL_TOP, hi),
        solid("hilltop", HILL_TOP, hi, w - HILL_TOP, h - hi),
        solid("stone_wall", 2720, hi - 48, 32, 48),
        piece("hill_meadow_wall", 2720, hi - 48),
        sign("meadow_sign_gate", 2950, hi - 160, "THE GATE", 160),
        edge("meadow_to_clearing", "on to the gate", w - WALL, hi, CLEARING, "clearing_from_meadow"),
        entity("CameraZone", HILL_TOP, 0, w - HILL_TOP, h, id="intro_meadow_lookout", name="the hilltop",
               mode="Default", target_offset_y=LOOKOUT_LIFT),
        start(rid, 120, lo),
    ]
    return build(rid, e, "THE HIGH MEADOW", COUNTRY_MUSIC, dangerous=True)


# ------------------------------------------------------ the gate clearing

#: The boom across the road beside the guard post: too high to jump, and
#: lifted by the lever beside it on the road's side.
BARRIER_X = 1560
BARRIER_H = 176
#: The freight track from the gate down to the siding: two pitches, and a
#: landing between them where the signal post stands.
FREIGHT_TOP, FREIGHT_FOOT = 2256, 4176
FREIGHT_LANDING = (3008, 3424, COUNTRY_FLOOR + 304)
BARRIER_LEVER = "hobford_barrier_lever"
#: Set by the lever, and never cleared: the barrier stays up once lifted, so
#: a second pull cannot shut a body out on either side of it.
BARRIER_LIFTED = "hobford_barrier_lifted"
GATE_ZONE = "hobford_gate_zone"
GATE_TERMINAL = "hobford_gate_terminal"


def clearing():
    """THE GATE CLEARING. The hilltop: the old ring in its ruin of standing
    stones, with new steel on it, the guard post and the boom across the
    road. Past the ring the freight track goes down the hill to the siding."""
    rid = CLEARING
    w, h, hi, lo = CLEARING_W, HILL_H, COUNTRY_FLOOR, VALLEY_FLOOR
    check_reach(rid, [("clearing", hi), ("stone", hi - 48), ("clearing", hi)])
    ring_x = 1780
    e = [
        *hill_walls(w, hi, lo),
        solid("road", 0, hi, FREIGHT_TOP, h - hi),
        entity("CameraZone", 0, 0, FREIGHT_TOP, h, id="intro_clearing_lookout", name="the hilltop",
               mode="Default", target_offset_y=LOOKOUT_LIFT),
        edge("clearing_from_meadow", "back down the hill path", 0, hi, MEADOW, "meadow_to_clearing"),
        solid("standing_stone_1", 560, hi - 48, 48, 48),
        solid("standing_stone_2", 880, hi - 48, 48, 48),
        *[piece("hill_standing_stone", x, hi - 48, name=f"standing stone {n}") for n, x in enumerate((560, 880), start=1)],
        piece("hill_gate_office", 1370, 460),
        # On the office's front, between the eaves and the window: a line
        # does not wrap, so two short ones over the office's middle.
        sign("clearing_sign_post", 1470, hi - 178, "GATE OFFICE", 100),
        sign("clearing_sign_hours", 1470, hi - 160, "BY APPOINTMENT", 120),
        # The gatekeeper, at the office door on the road's side of the barrier.
        npc("npc_valley_gatekeeper", "valley_gatekeeper", "Talk to the gatekeeper", 1420, hi),
        entity("LockWall", BARRIER_X, hi - BARRIER_H, 24, BARRIER_H, id="hobford_barrier", name="the barrier",
               gated_by=f"world.flag_set {BARRIER_LIFTED}", look="hill_gate_barrier"),
        entity("Switch", BARRIER_X - 56, hi - 32, 24, 32, id=BARRIER_LEVER, name="the barrier lever",
               prompt="Lift the barrier", action="ToggleFlag", on_activate=f"world.set_flag {BARRIER_LIFTED} true"),
        # The ring: a dialed ring of the gate network (`gate_network.ron`,
        # `gate_portals.ron`), the props it is drawn with, and its terminal.
        entity("Prop", ring_x, hi - 288, 288, 288, name="Clearing Gate Ring", kind="triangle_gate_ring"),
        entity("Prop", ring_x, hi - 288, 288, 288, name="Clearing Gate Portal", kind="triangle_gate_portal"),
        entity("LoadingZone", ring_x + 72, hi - 288, 144, 288, id=GATE_ZONE, name="the gate", activation="Door",
               presentation="SceneArt"),
        entity("Prop", 1690, hi - 56, 64, 56, name="Clearing Gate Dialer", kind="gate_dialer_triangle"),
        entity("Switch", 1710, hi - 44, 24, 32, id=GATE_TERMINAL, name=f"{VILLAGE_NAME} gate terminal", prompt="Dial the gate",
               action="GateTerminal"),
        sign("clearing_sign_ring", ring_x + 144, hi - 340, f"{VILLAGE_NAME.upper()} GATE. FREIGHT WINDOW ON THE BOARD.", 420),
        sign("clearing_sign_siding", FREIGHT_TOP - 40, hi - 140, "FREIGHT SIDING", 220),
        slope("freight_track_upper", FREIGHT_TOP, hi, FREIGHT_LANDING[0], FREIGHT_LANDING[2]),
        solid("freight_landing", FREIGHT_LANDING[0], FREIGHT_LANDING[2], FREIGHT_LANDING[1] - FREIGHT_LANDING[0],
              h - FREIGHT_LANDING[2]),
        sign("clearing_sign_signal", (FREIGHT_LANDING[0] + FREIGHT_LANDING[1]) // 2, FREIGHT_LANDING[2] - 140,
             "FREIGHT ONLY. WALK ON THE LEFT.", 320),
        slope("freight_track_lower", FREIGHT_LANDING[1], FREIGHT_LANDING[2], FREIGHT_FOOT, lo),
        solid("siding_bank_foot", FREIGHT_FOOT, lo, w - FREIGHT_FOOT, h - lo),
        edge("clearing_to_siding", "down the freight track to the siding", w - WALL, lo, SIDING, "siding_from_clearing"),
        start(rid, 120, hi),
    ]
    return build(rid, e, "THE GATE CLEARING", COUNTRY_MUSIC, dangerous=True, extra=GATESIDE)


# ------------------------------------------------------ the freight siding

YARD_FIGHT = "intro_freight_yard_fight"
#: The freight stacked on the platform: (name, x0, x1, top). Solid crates on
#: the floor and one-way pallets over them.
#: The freight crates are solid on whole 16 px cells, so the crates drawn
#: over them cover the blocks' tiles.
FREIGHT = [("crate_a", 688, 784, LOW_FLOOR - 48), ("crate_b", 1232, 1328, LOW_FLOOR - 48)]
PALLETS = [("pallets_a", 820, 980, LOW_FLOOR - 112), ("pallets_b", 1360, 1520, LOW_FLOOR - 112)]


def siding():
    """THE FREIGHT SIDING. The new platform at the foot of the freight track
    below the gate, where the
    goblins wait for the freight window with their handcart and the crate
    from the barn. The fight starts on the platform; its bell keeps it won
    (an encounter with no linked switch starts again whenever a player walks
    back into its trigger)."""
    rid = SIDING
    _, (w, h) = ROOMS_AT[rid]
    g = LOW_FLOOR
    check_reach(rid, [("platform", g), ("crate a", FREIGHT[0][3]), ("pallets a", PALLETS[0][3])])
    e = [
        *walls(w, g, west=[g], east=[g]),
        solid("platform", 0, g, w, h - g),
        edge("siding_from_clearing", "up the freight track to the gate", 0, g, CLEARING, "clearing_to_siding"),
        entity("CutsceneTrigger", 300, 32, 64, g - 32, cutscene="foreman_siding"),
        entity("EncounterTrigger", 440, 32, 64, g - 32, id=YARD_FIGHT, name=f"{YARD_FIGHT}_trigger"),
        # The freight crates are solid, and drawn as crates; the loading
        # stages are decks on trestle legs a walker goes under, not boards
        # in the air.
        *[solid(n, x0, top, x1 - x0, g - top) for n, x0, x1, top in FREIGHT],
        *[piece("hill_freight_crates", x0, top, name=f"freight {n}") for n, x0, x1, top in FREIGHT],
        *[ledge(n, x0, top, x1 - x0) for n, x0, x1, top in PALLETS],
        *[piece("hill_loading_stage", x0, top, name=f"loading stage {n}") for n, x0, x1, top in PALLETS],
        # The platform's notice, its words on its board.
        piece("hill_siding_notice", 450, g - 112, name="the platform notice"),
        sign("siding_sign_platform", 570, g - 106, "FREIGHT ONLY", 120),
        sign("siding_sign_persons", 570, g - 86, "NO PERSONS ON THE PLATFORM", 220),
        entity("CutsceneTrigger", 1480, 32, 64, g - 32, cutscene="work_order"),
        entity("ChestSpawn", 1560, g - 58, 76, 58, name="the goblins' crate", reward="flag:intro_creator_notes_recovered"),
        # The label pasted on the crate's lid, clear of the loading stage.
        sign("siding_sign_crate", 1620, g - 84, "1 LAB OF RESEARCH. PAID.", 200),
        entity("Switch", 1700, g - 32, 24, 32, id=f"{YARD_FIGHT}_again", name="the platform bell",
               prompt="Ring the platform bell", target_encounter=YARD_FIGHT, action="ResetEncounter"),
        # The drove road's fingerpost, the way on its arm.
        piece("hill_fingerpost", w - 190, g - 120, name="the drove road's fingerpost"),
        sign("siding_sign_fell", w - 112, g - 109, "THE FELL", 90),
        edge("siding_to_fell", "the drove road up the fell", w - WALL, g, FELL, "fell_from_siding"),
        start(rid, 200, g),
    ]
    return build(rid, e, "THE FREIGHT SIDING", GOBLIN_MUSIC, dangerous=True, extra=GATESIDE)


# ------------------------------------------------------- the millstream

#: The stream: its banks are level with the ground, its bed is 96 down, and
#: stepping stones cross it flush with the banks. Rocks in the bed at each
#: bank are the way out of the water.
STREAM = (500, 1300, LOW_FLOOR + 96)
#: The stepping stones, on the 16 px grid as the blocks they are.
STONES = [(592, 672), (752, 832), (912, 992), (1072, 1152), (1216, 1280)]


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
        *walls(w, g, west=[g], east=[g]),
        edge("millstream_from_lane", "up the bank path to the lane", 0, g, LANE, "lane_to_millstream"),
        # The west bank, with a dry hollow under it behind a cracked wall.
        solid("west_bank", 0, g, 420, h - g),
        solid("hollow_roof", 420, g, s0 - 420, 16),
        solid("hollow_floor", 420, s_bed, s0 - 420, h - s_bed),
        entity("BreakablePlatform", s0 - 16, g + 16, 16, s_bed - g - 16, id="millstream_cracked_wall",
               name="a cracked wall", max_hp=3.0, respawn="Persistent", collision="Solid", trigger="OnHit"),
        entity("PickupSpawn", 440, s_bed - 28, 24, 24, name="a jar of coins", kind="currency:25"),
        # At the back of the hollow, a hatch: the salt run under the valley.
        entity("LoadingZone", 424, s_bed - 80, 48, 80, id="millstream_to_salt_run", name="down the hatch",
               activation="Door", target_room=SALT_RUN, target_zone="salt_run_from_millstream", bidirectional=True,
               presentation="SceneArt"),
        piece("hill_salt_run_hatch", 424, s_bed - 2),
        solid("stream_bed", s0, s_bed, s1 - s0, h - s_bed),
        water(f"{rid}_stream", s0, g + 8, s1 - s0, s_bed - g - 8),
        solid("rock_west", 496, s_bed - 48, 64, 48),
        piece("hill_stream_rock", 496, s_bed - 48),
        solid("rock_east", s1 - 48, s_bed - 48, 48, 48),
        *[solid(f"stone_{n}", x0, g, x1 - x0, s_bed - g) for n, (x0, x1) in enumerate(STONES)],
        *[piece("hill_stepping_stone" if x1 - x0 == 80 else "hill_stepping_stone_narrow", x0, g, name=f"stepping stone {n}")
          for n, (x0, x1) in enumerate(STONES)],
        solid("east_bank", s1, g, w - s1, h - g),
        piece("hill_village_mill", 1500, 220),
        # The miller, on the bank by his door.
        npc("npc_valley_miller", "valley_miller", "Talk to the miller", 1440, g),
        ledge("mill_porch", 1520, g - 48, 160),
        ledge("mill_upper_floor", 1600, g - 112, 220),
        ledge("mill_loft_window", 1720, g - 176, 120),
        entity("PickupSpawn", 1800, g - 176 - 28, 24, 24, name="a few coins", kind="currency:10"),
        sign("millstream_sign_mill", 1700, g - 260, f"{VILLAGE_NAME.upper()} MILL. FLOUR, FEED, NO CREDIT.", 380),
        edge("millstream_to_hobford", f"on into {VILLAGE_NAME}", w - WALL, g, VILLAGE, "hobford_from_millstream"),
        start(rid, 240, g),
    ]
    return build(rid, e, "THE MILLSTREAM", COUNTRY_MUSIC, dangerous=True)


# --------------------------------------------------------------- Hobford

#: The houses of the street: (name, porch x, roof x0, roof x1). A porch is 48
#: over the street and a roof 64 over its porch.
HOUSES = [("cottage", 260, 300, 540), ("smithy", 860, 900, 1160), ("inn", 1460, 1500, 1800)]


def village():
    """HOBFORD. A short street: cottages, the old smithy that sells gate
    goods now, the well, the inn, the notice board. West is the mill; east
    the road goes into the woods. The trader keeps the smithy and the
    innkeeper the Plough."""
    rid = VILLAGE
    w, h, g = COUNTRY_W, LOW_H, LOW_FLOOR
    check_reach(rid, [("street", g), ("porch", g - 48), ("roof", g - 112), ("loft", g - 176)])
    e = [
        *walls(w, g, west=[g], east=[g]),
        solid("street", 0, g, w, h - g),
        # The houses, the well and the board, drawn on the room's boards
        # (`hobford_props.py` in the sprite renderer).
        piece("hill_village_cottage", 240, 300),
        piece("hill_village_smithy", 840, 270),
        piece("hill_village_inn", 1440, 300),
        piece("hill_village_well", 1236, 370),
        piece("hill_village_notice_board", 1840, 280),
        edge("hobford_from_millstream", "back to the millstream", 0, g, MILLSTREAM, "millstream_to_hobford"),
        *[ledge(f"{n}_porch", px, g - 48, 80) for n, px, _, _ in HOUSES],
        *[ledge(f"{n}_roof", x0, g - 112, x1 - x0) for n, _, x0, x1 in HOUSES],
        ledge("smithy_loft", 1000, g - 176, 120),
        entity("PickupSpawn", 1060, g - 176 - 28, 24, 24, name="a dropped purse", kind="currency:20"),
        solid("well", 1248, g - 48, 64, 48),
        # The smith who sells gate goods, at his door; the innkeeper at the
        # Plough's, where the board sends people about lost things.
        npc("npc_valley_trader", "valley_trader", "Talk to the trader", 1000, g),
        npc("npc_valley_innkeeper", "valley_innkeeper", "Talk to the innkeeper", 1580, g),
        # On the smithy's front under the thatch, in two lines over its door.
        sign("hobford_sign_smithy", 1077, g - 100, "GATE GOODS", 100),
        sign("hobford_sign_goods", 1077, g - 82, "OIL, SALT, BATTERIES", 170),
        sign("hobford_sign_inn", 1650, g - 150, "THE PLOUGH", 160),
        sign("hobford_board_1", 2090, g - 200, "FREIGHT WINDOW: TOMORROW, NOON.", 360),
        sign("hobford_board_2", 2090, g - 170, "LOST: ONE SPECKLED HEN. ASK AT THE PLOUGH.", 420),
        sign("hobford_board_3", 2090, g - 140, "STRANGERS AT THE GATE: SEE THE GATE OFFICE.", 440),
        edge("hobford_to_woods", "the road into the woods", w - WALL, g, WOODS, "woods_from_hobford"),
        start(rid, 120, g),
    ]
    return build(rid, e, VILLAGE_NAME.upper(), VILLAGE_MUSIC)


# ------------------------------------------------------------ the woods

BOB_X = 1240
#: The hollow oak: a climb up inside its trunk to a nook (a secret).
HOLLOW = [(1700, LOW_FLOOR - 64), (1600, LOW_FLOOR - 128), (1700, LOW_FLOOR - 192)]


def woods():
    """HOBFORD WOODS. Roots and a fallen trunk, Bob's survey camp in a
    clearing, a hollow oak, and at the east end the goblins' trail out of the
    trees and up the hill, where one goblin keeps a lookout."""
    rid = WOODS
    w, h, g = COUNTRY_W, LOW_H, LOW_FLOOR
    check_reach(rid, [("floor", g), ("root", g - 48), ("floor", g), ("trunk", g - 64), ("floor", g)])
    check_reach(rid, [("floor", g), *[(f"hollow {n}", y) for n, (_, y) in enumerate(HOLLOW)]])
    e = [
        *walls(w, g, west=[g], east=[g]),
        solid("floor", 0, g, w, h - g),
        edge("woods_from_hobford", f"back to {VILLAGE_NAME}", 0, g, VILLAGE, "hobford_to_woods"),
        solid("root_1", 416, g - 48, 80, 48),
        piece("hill_woods_root", 416, g - 48, name="root 1"),
        ledge("fallen_trunk", 640, g - 64, 240),
        piece("hill_woods_fallen_trunk", 640, g - 64, name="the fallen trunk"),
        solid("root_2", 992, g - 48, 80, 48),
        piece("hill_woods_root", 992, g - 48, name="root 2"),
        npc("npc_bob", "bob_woods", "Talk to Bob", BOB_X, g),
        *stake_board("woods_sign_camp", BOB_X + 150, g, "SURVEY CAMP", "HANDS OFF THE STAFF"),
        *[ledge(f"hollow_oak_{n}", x, y, 96) for n, (x, y) in enumerate(HOLLOW)],
        # Between the oak's roots, a gap a body fits down: the salt run.
        entity("LoadingZone", 1640, g - 96, 48, 96, id="woods_to_salt_run", name="down among the roots",
               activation="Door", target_room=SALT_RUN, target_zone="salt_run_from_woods", bidirectional=True,
               presentation="SceneArt"),
        piece("hill_woods_hollow_oak", 1440, 20),
        entity("PickupSpawn", 1740, HOLLOW[-1][1] - 28, 24, 24, name="a can of oil", kind="health:2"),
        hen(rid, 1, 1880, g, dialogue="hobford_lost_hen"),
        raider(rid, 1, 2160, g),
        edge("woods_to_meadow", "up the hill path to the gate", w - WALL, g, MEADOW, "meadow_from_woods"),
        start(rid, 120, g),
    ]
    return build(rid, e, f"{VILLAGE_NAME.upper()} WOODS", COUNTRY_MUSIC, look=WOODS_LOOK, dangerous=True)


# --------------------------------------------------------- the salt run

#: The run's floor, west to east: (x0, x1, top). From the hatch the old mill
#: race steps down to the channel, climbs out under the village, passes the
#: foot of the well, and runs on to the oak's roots, which climb to a shelf
#: under the oak. Each step is a walk down or one jump up, both ways.
RUN_FLOOR = [
    (0, 320, 192), (320, 480, 240), (480, 640, 288), (640, 800, 336),
    (800, 1504, 400),
    (1504, 1696, 352), (1696, 2400, 352), (2400, 3104, 400), (3104, 3456, 448), (3456, 4096, 400),
    (4096, 4544, 400), (4544, 4880, 400),
    (4880, SALT_RUN_W, 192),
]
#: Headroom over the run's floor: a jump and a body under the roof.
RUN_HEADROOM = 192
#: The channel's water: ankle deep.
RACE = (800, 1504, 32)
#: The foot of the well, under the village's well (its x in the world, less
#: the run's): the shaft opens in the roof over a puddle.
WELL_FOOT = 7328 + 1248 - SALT_RUN_X
#: Up to the shelf under the oak: boards the smugglers wedged between the
#: roots, (x0, x1, top).
ROOTS = [(4704, 4832, 336), (4560, 4688, 272), (4704, 4832, 208)]
#: The smugglers' lamps, west of the well and none past it (the hatch's
#: sign says so): (x, y of the bracket's top). Each is a lantern on its
#: bracket and the light it gives (`LightSource`, DR2).
LAMPS = [(250, 92), (980, 236), (1360, 236), (2060, 196)]
LAMP_RADIUS = 260


def lamp(n, x, y):
    """A lantern on its bracket at (x, y), and its light at the glass."""
    return [
        piece("hill_salt_run_lantern", x, y, name=f"lantern {n}"),
        entity("LightSource", x + 15 - 16, y + 26 - 16, 32, 32, name=f"salt_run_lamp_{n}", radius=float(LAMP_RADIUS),
               color="#ffc070", intensity=0.95),
    ]


#: The run is dark: it is under the hill (dark rooms, DR1).
UNDERGROUND_DARK = '\n    darkness: 75,\n    ambient: "#0a0806",'


def salt_run():
    """THE SALT RUN. An old smugglers' passage under the valley, from a
    hatch behind the mill wheel to the hollow oak in the woods: salt came
    this way and not through the gate's toll. The mill race steps down to
    its channel; under the village the run passes the foot of the well; at
    the east end boards between the oak's roots climb to a shelf and the
    way up."""
    rid = SALT_RUN
    _, (w, h) = ROOMS_AT[rid]
    floors = [("hatch", RUN_FLOOR[0][2])] + [(f"floor {n}", top) for n, (_, _, top) in enumerate(RUN_FLOOR[1:-1])]
    check_reach(rid, floors + [(f"root {n}", top) for n, (_, _, top) in enumerate(ROOTS)] + [("shelf", RUN_FLOOR[-1][2])])
    # And back: west from the channel up the race's steps to the hatch.
    check_reach(rid, [(n, top) for n, top in reversed(floors[:6])])
    e = [solid("west_end", 0, 0, WALL, h), solid("east_end", w - WALL, 0, WALL, h)]
    for n, (x0, x1, top) in enumerate(RUN_FLOOR):
        e.append(solid(f"floor_{n}", x0, top, x1 - x0, h - top))
        roof = top - RUN_HEADROOM
        # The root chamber and the shelf are open to the oak.
        if x0 >= ROOTS[1][0] - 16:
            continue
        if x0 <= WELL_FOOT < x1:
            # The well's shaft: an opening in the roof, straight up.
            e.append(solid(f"roof_{n}_west", x0, 0, WELL_FOOT - x0, roof))
            e.append(solid(f"roof_{n}_east", WELL_FOOT + 64, 0, x1 - WELL_FOOT - 64, roof))
        elif roof > 0:
            e.append(solid(f"roof_{n}", x0, 0, x1 - x0, roof))
    x0, x1, depth = RACE
    race_top = next(top for a, _, top in RUN_FLOOR if a == x0)
    e += [
        # The ways out are the smugglers' ladders up to a trapdoor (the scene
        # draws them; no door in the rock).
        piece("hill_salt_run_ladder", 64, 0, name="the hatch ladder"),
        entity("LoadingZone", 64, RUN_FLOOR[0][2] - 96, 48, 96, id="salt_run_from_millstream", name="up the hatch",
               activation="Door", target_room=MILLSTREAM, target_zone="millstream_to_salt_run", bidirectional=True,
               presentation="SceneArt"),
        sign("salt_run_sign_hatch", 300, 40, "SALT RUN. MILL TO OAK. NO LIGHTS PAST THE WELL.", 480),
        # A spare lantern by the hatch (the Lantern, TN3): past the well the
        # light is the one you carry.
        entity("PickupSpawn", 200, RUN_FLOOR[0][2] - 28, 24, 24, name="a spare lantern", kind="ability:lantern",
               respawn="Persistent"),
        water(f"{rid}_race", x0, race_top - depth, x1 - x0, depth),
        slug(rid, 1, 1000, race_top),
        slug(rid, 2, 1300, race_top),
        # Under the inn, the smugglers' tally on the wall.
        sign("salt_run_sign_tally", 2100, 352 - 150, "IN CHALK: 112 SACKS. 0 TOLLS.", 360),
        *[part for n, (x, y) in enumerate(LAMPS) for part in lamp(n, x, y)],
        # Daylight down the well's shaft, faint and cool.
        entity("LightSource", WELL_FOOT + 16, 300, 32, 32, name="salt_run_well_light", radius=220.0, color="#cfe0ff",
               intensity=0.7),
        # The foot of the well: what fell down it.
        entity("PickupSpawn", WELL_FOOT + 20, 448 - 28, 24, 24, name="a bucket of coins", kind="currency:30"),
        sign("salt_run_sign_well", WELL_FOOT + 32, 448 - 150, "SOMEBODY UP THERE THREW A WISH DOWN HERE", 440),
        *[ledge(f"root_board_{n}", a, top, b - a) for n, (a, b, top) in enumerate(ROOTS)],
        sign("salt_run_sign_note", 4400, 400 - 160,
             "A NOTE: IF YOU CAN READ THIS, YOU ARE NOT WORTH YOUR SALT. TURN BACK.", 560),
        piece("hill_salt_run_ladder", w - WALL - 112, 0, name="the roots ladder"),
        entity("LoadingZone", w - WALL - 112, RUN_FLOOR[-1][2] - 96, 48, 96, id="salt_run_from_woods",
               name="up through the roots", activation="Door", target_room=WOODS, target_zone="woods_to_salt_run",
               bidirectional=True, presentation="SceneArt"),
        start(rid, 160, RUN_FLOOR[0][2]),
    ]
    return build(rid, e, "THE SALT RUN", "vault_in_the_dark", look="cave", bg="#0c0a08", dangerous=True,
                 extra=UNDERGROUND_DARK)


# -------------------------------------------------------------- the fell

#: The drove road up the fell, west to east: each flat is (x0, x1, top),
#: joined by a slope or by one step up. The climb is the ground's: slopes,
#: a terrace with the sheepfold, a scree ledge and two crags, and the top.
FELL_FOOT = (0, 400, FELL_FLOOR)
FOLD = (1040, 1440, FELL_FLOOR - 256)
SCREE = (2080, 2400, FELL_FLOOR - 512)
CRAGS = [(2400, 2560, FELL_FLOOR - 576), (2560, 2720, FELL_FLOOR - 640)]
SUMMIT = (3200, FELL_W, FELL_FLOOR - 832)
CAIRN = (3376, 3440)
#: The sheepfold's wall: a hop on the terrace (x, width), on the 16 px grid
#: as the block it is.
FOLD_WALL = (1216, 48)
#: The fell's dressing (`hill_village_props.py`): each piece's width and
#: where the ground under its middle is in its frame. A `_slope` piece's
#: foot rises east with the drove road (0.4).
DRESSING = {
    "hill_fell_rocks": (128, 52), "hill_fell_rocks_slope": (128, 52),
    "hill_fell_gorse": (96, 52), "hill_fell_gorse_slope": (96, 52),
}


def dress(kind, x, ground, n):
    """Dressing piece `kind` whose middle stands at `x` on `ground`."""
    width, foot = DRESSING[kind]
    return piece(kind, x - width // 2, ground - foot, name=f"fell {kind.removeprefix('hill_fell_')} {n}")


def drove_road(x0, y0, x1, y1, x):
    """The ground on a slope from (x0, y0) to (x1, y1) at `x`."""
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def fell():
    """THE FELL. The mountain beside the gate's hill: the old drove road
    climbs it from the siding, past the sheepfold where the shepherd keeps
    the flock in summer, over the scree and two crags, to the top, where
    the whole valley and the gate are in view. A climb by the ground, not
    by platforms (Jon's note 8)."""
    rid = FELL
    w, h = FELL_W, FELL_H
    f0, f1, fy = FELL_FOOT
    d0, d1, dy = FOLD
    s0, s1, sy = SCREE
    t0, t1, ty = SUMMIT
    check_reach(rid, [("fold", dy), ("fold wall", dy - 48), ("fold", dy)])
    check_reach(rid, [("scree", sy), *[(f"crag {n}", top) for n, (_, _, top) in enumerate(CRAGS)]])
    check_reach(rid, [("top", ty), ("cairn", ty - 48), ("top", ty)])
    e = [
        solid("west_wall", 0, 0, WALL, fy - 96),
        solid("east_wall", w - WALL, 0, WALL, h),
        edge("fell_from_siding", "down to the siding", 0, fy, SIDING, "siding_to_fell"),
        solid("fell_foot", f0, fy, f1 - f0, h - fy),
        sign("fell_sign_road", 260, fy - 140, "DROVE ROAD. SHUT THE GATES BEHIND YOU", 380),
        slope("drove_road_lower", f1, fy, d0, dy),
        solid("sheepfold_terrace", d0, dy, d1 - d0, h - dy),
        solid("sheepfold_wall", FOLD_WALL[0], dy - 48, FOLD_WALL[1], 48),
        piece("hill_fell_fold_wall", FOLD_WALL[0], dy - 48),
        npc("npc_valley_shepherd", "valley_shepherd", "Talk to the shepherd", 1340, dy),
        slope("drove_road_middle", d1, dy, s0, sy),
        solid("scree_ledge", s0, sy, s1 - s0, h - sy),
        *[solid(f"crag_{n}", x0, top, x1 - x0, h - top) for n, (x0, x1, top) in enumerate(CRAGS)],
        slope("drove_road_upper", CRAGS[-1][1], CRAGS[-1][2], t0, ty),
        solid("summit", t0, ty, t1 - WALL - t0, h - ty),
        solid("cairn", CAIRN[0], ty - 48, CAIRN[1] - CAIRN[0], 48),
        piece("hill_fell_cairn", CAIRN[0], ty - 48),
        entity("PickupSpawn", (CAIRN[0] + CAIRN[1]) // 2 - 12, ty - 48 - 28, 24, 24, name="a tin left on the cairn",
               kind="currency:30"),
        sign("fell_sign_top", 3260, ty - 150, "THE TOP. THE VIEW IS FREE", 300),
        # The top is a lookout: framed on Scout, the fell's own rock fills the
        # frame; lifted, the valley and the gate's hill are in view.
        entity("CameraZone", CRAGS[-1][1], 0, w - CRAGS[-1][1], h, id="intro_fell_lookout", name="the top",
               mode="Default", target_offset_y=LOOKOUT_LIFT),
        start(rid, 120, fy),
        # The hillside: gorse and rocks along the road, the flock in the fold
        # and on the top, boulders on the scree.
        dress("hill_fell_rocks", 330, fy, 1),
        *[dress(kind, x, drove_road(f1, fy, d0, dy, x), n)
          for n, (kind, x) in enumerate([("hill_fell_gorse_slope", 560), ("hill_fell_rocks_slope", 820)])],
        *[sheep(x, dy) for x in (1090, 1160, 1400)],
        *[dress(kind, x, drove_road(d1, dy, s0, sy, x), n)
          for n, (kind, x) in enumerate([("hill_fell_gorse_slope", 1600), ("hill_fell_rocks_slope", 1900)], start=3)],
        dress("hill_fell_rocks", 2200, sy, 5),
        dress("hill_fell_gorse", 2340, sy, 6),
        *[dress(kind, x, drove_road(CRAGS[-1][1], CRAGS[-1][2], t0, ty, x), n)
          for n, (kind, x) in enumerate([("hill_fell_gorse_slope", 2850), ("hill_fell_rocks_slope", 3080)], start=7)],
        *[sheep(x, ty) for x in (3300, 3500)],
    ]
    return build(rid, e, "THE FELL", COUNTRY_MUSIC)


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


#: East to west: a relayout moves the rooms east, and each one's new place
#: is free once the rooms east of it have moved.
ROOMS = (fell, siding, clearing, meadow, woods, village, millstream, lane, workshop, market, culvert, salt_run)


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
