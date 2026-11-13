#!/usr/bin/env python3
"""Write the rooms of the Boss dimension: the final boss's stage
(`docs/planning/game/final-boss.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/boss_stage/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/boss_stage/make_specs.py --apply  # and makes the rooms
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/boss_stage/make_specs.py --apply --hall  # and the hall's door

Run it from the repository root. Change the script, not the rooms.

The bossofthegame's last show. Its ring's address is LEGACY
(`data/gate_network.ron`, hidden): it dials straight to the lobby, one door
from the stage. The world file is `boss.ldtk`. The rooms join by doors:

    [ the lobby ] -door-> [ the main stage ] -door (shut until he retires)-> [ the green room ]
         ^                                                                          |
         +-------------------------- one way, home ---------------------------------+

- `boss_lobby`: the ring and its terminal at the west end, the tour's
  posters, and steps up to a landing with the stage door.
- `boss_main_stage`: the arena. Full Stack, the giant amp-stack robot, stands
  at the centre and the Boss stands on its shoulders. Tiered risers at each
  side (low, middle, high) and a lighting truss over each side reach the
  height of its top. The way on to the green room is in an alcove past the
  east wall, behind a grille that his retirement opens.
- `boss_green_room`: where he retires (a `CutsceneTrigger`,
  `boss_retirement`); a door home to the lobby.
- `hall_bossofthegame_stage`: the Hall of Bosses' practice copy of the stage
  (placement `hall.bossofthegame`), by a door on the hall's lower floor.

The robot's numbers (`platformer_defaults.ron`): a jump rises 83 px, a jump
and a double jump 139 px; the body is 30 x 48. Each tier here is 128 over
the one under it: a double jump.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_boss_stage_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))

from district_kit import SANDBOX_LDTK, WALL, WORLDS, add_entities, door, ensure_world, entity, ledge, make_rooms, pad, room, run, sign, solid, start  # noqa: E402

import gates  # noqa: E402

WORLD = WORLDS / "boss.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/boss_stage/make_specs.py"
UID_OFFSET = 1400000

LOBBY = "boss_lobby"
STAGE = "boss_main_stage"
GREEN = "boss_green_room"
#: The Hall of Bosses' practice copy of the stage, behind a door of the hall.
HALL_STAGE = "hall_bossofthegame_stage"
HALL_STAGE_ENTRY = "hall_bossofthegame_stage_entry"
HALL = "hall_of_bosses"
HALL_DOOR = "hall_to_bossofthegame_portal"
HALL_SWITCH = "hall_bossofthegame_life_switch"
HALL_PLACEMENT = "hall.bossofthegame"

#: The Boss's placement. His defeat is saved under this id, and it opens the
#: way to the green room (`boss.cleared <id>`).
PLACEMENT = "boss_stage.bossofthegame"

#: The dark red hall of the boss lair: the dimension's look until it has a
#: stage of its own.
BIOME = "boss"
BG = "#1A0A10"
LOBBY_MUSIC = "scaling_laws"
GREEN_MUSIC = "a_possible_morning"

#: Each room: where it is in the world, and its size.
ROOMS_AT = {
    LOBBY: ((0, 0), (1600, 768)),
    STAGE: ((2000, -384), (2560, 1152)),
    GREEN: ((4992, 0), (1280, 640)),
    HALL_STAGE: ((0, 2048), (2560, 1152)),
}

#: The stage: its floor, and the alcove of the way on past the east wall.
STAGE_FLOOR = 1088
ALCOVE_X = 2432
ALCOVE_TOP = STAGE_FLOOR - 160
#: Each tier is a double jump over the one under it.
TIER = 128
#: Full Stack's body box (its feet on the floor, its middle at the stage's
#: middle). The catalog row `npc_full_stack` has the same size.
STACK_W, STACK_H = 400, 480


def lobby():
    rid = LOBBY
    w, h = ROOMS_AT[rid][1]
    floor = 704
    landing = floor - 192
    e = [
        solid("ground", 0, floor, w, h - floor),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        solid("east_wall", w - WALL, 32, WALL, floor - 32),
        start(rid, 560, floor),
        # The ring (LEGACY) and its terminal: the way in and the way home.
        *gates.as_ron(gates.ring("Lobby Gate", "boss_lobby_gate", 96, floor, "the gate")),
        *gates.as_ron(gates.terminal("Lobby Gate", "boss_lobby_gate_terminal", 400, floor)),
        sign("lobby_sign_gate", 240, floor - 360, "LEGACY: the last stop on the network", 380),
        # Home from the green room, one way.
        pad("boss_lobby_green_arrival", "from the green room", 680, floor),
        sign("lobby_sign_poster", 860, floor - 300, "TONIGHT ONLY: THE BOSSOFTHEGAME, FINAL TOUR", 520),
        sign("lobby_sign_support", 860, floor - 268, "with special guest FULL STACK", 360),
        sign("lobby_sign_rules", 860, floor - 236, "NO REFUNDS. NO RESPAWNS. (THERE ARE RESPAWNS.)", 480),
        # Three steps up to the landing of the stage door.
        solid("step_1", 1040, floor - 64, w - WALL - 1040, 64),
        solid("step_2", 1136, floor - 128, w - WALL - 1136, 64),
        solid("step_3", 1232, landing, w - WALL - 1232, 64),
        door("boss_lobby_stage_door", "to the main stage", 1440, landing, STAGE, "boss_stage_entry"),
        sign("lobby_sign_stage", 1460, landing - 140, "MAIN STAGE", 220),
    ]
    at = ROOMS_AT[rid][0]
    return rid, room(rid, e, at=at, size=(w, h), biome=BIOME, music=LOBBY_MUSIC, bg=BG, title="THE LOBBY",
                     generator=GENERATOR)


def placed(etype, x, y, w, h, ref, **fields) -> str:
    """An entity another entity names by `ref` (a mount its rider rides)."""
    return entity(etype, x, y, w, h, **fields).replace(f'( type: "{etype}", ', f'( type: "{etype}", ref: "{ref}", ', 1)


def stage_floor_plan(rid, placement, *, entry, home_room, home_zone):
    """The stage: the risers, the truss, Full Stack and the Boss on it. The
    main game's and the hall's copy share it."""
    w, h = ROOMS_AT[rid][1]
    floor = STAGE_FLOOR
    # The low riser is a double jump off the floor; each tier over it is
    # another; the truss is at the height of the robot's top.
    truss = floor - STACK_H
    high, mid, low = truss + TIER, truss + 2 * TIER, truss + 3 * TIER
    mount = f"{rid}_full_stack"
    stack_x = w // 2 - STACK_W // 2
    return [
        solid("stage_floor", 0, floor, w, h - floor),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        door(entry, "back", 48, floor, home_room, home_zone),
        start(rid, 176, floor),
        # The risers, west: low by the robot, high by the wall, each a double
        # jump over the one under it; the truss over them reaches the height
        # of the robot's top.
        ledge("riser_west_low", 560, low, 240),
        ledge("riser_west_mid", 320, mid, 240),
        ledge("riser_west_high", 80, high, 240),
        ledge("truss_west", 360, truss, 640),
        # And east, the same.
        ledge("riser_east_low", 1760, low, 240),
        ledge("riser_east_mid", 2000, mid, 240),
        ledge("riser_east_high", 2176, high, 240),
        ledge("truss_east", 1560, truss, 640),
        # Full Stack at the middle of the stage, behind the playable plane,
        # and the Boss on its top (the catalog's saddle, 60 right of its
        # middle).
        placed("EnemySpawn", stack_x, floor - STACK_H, STACK_W, STACK_H, mount, name="Full Stack", brain="stand_still",
               character_id="npc_full_stack", disposition="Peaceful", respawn="OnRoomReenter", depth_plane="Behind"),
        entity("BossSpawn", w // 2 + 60 - 27, floor - STACK_H - 96, 54, 96, name="the bossofthegame",
               brain="PhaseScript:bossofthegame", mounted_on=mount, encounter_id=placement),
    ]


def stage():
    rid = STAGE
    w, h = ROOMS_AT[rid][1]
    floor = STAGE_FLOOR
    e = stage_floor_plan(rid, PLACEMENT, entry="boss_stage_entry", home_room=LOBBY, home_zone="boss_lobby_stage_door") + [
        # The way on: an alcove past the east wall, behind a grille that the
        # Boss's retirement opens.
        solid("east_wall", ALCOVE_X, 32, WALL, ALCOVE_TOP - 32),
        solid("alcove_roof", ALCOVE_X + WALL, ALCOVE_TOP - 32, w - ALCOVE_X - 2 * WALL, 32),
        solid("alcove_back", w - WALL, 32, WALL, floor - 32),
        entity("LockWall", ALCOVE_X, ALCOVE_TOP, WALL, floor - ALCOVE_TOP, id="boss_stage_green_grille",
               name="the grille of the green room", gated_by=f"boss.cleared {PLACEMENT}", look="temple_gate_iron"),
        door("boss_stage_green_door", "to the green room", ALCOVE_X + 48, floor, GREEN, "boss_green_stage_door"),
    ]
    at = ROOMS_AT[rid][0]
    return rid, room(rid, e, at=at, size=(w, h), biome=BIOME, music=LOBBY_MUSIC, bg=BG, title="THE MAIN STAGE",
                     generator=GENERATOR, dangerous=True, extra='\n    entry_cutscene: "boss_vibe_kill",')


def hall_stage():
    """The Hall of Bosses' copy of the stage: a practice boss of its own
    (`hall.bossofthegame`), its door back to the hall and no way on."""
    rid = HALL_STAGE
    w, h = ROOMS_AT[rid][1]
    e = stage_floor_plan(rid, HALL_PLACEMENT, entry=HALL_STAGE_ENTRY, home_room=HALL, home_zone=HALL_DOOR) + [
        solid("east_wall", w - WALL, 32, WALL, STAGE_FLOOR - 32),
    ]
    at = ROOMS_AT[rid][0]
    return rid, room(rid, e, at=at, size=(w, h), biome=BIOME, music=LOBBY_MUSIC, bg=BG, title="THE BOSSOFTHEGAME (PRACTICE)",
                     generator=GENERATOR, dangerous=True, extra="\n    practice: true,")


def green_room():
    rid = GREEN
    w, h = ROOMS_AT[rid][1]
    floor = 576
    e = [
        solid("ground", 0, floor, w, h - floor),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        solid("east_wall", w - WALL, 32, WALL, floor - 32),
        door("boss_green_stage_door", "back to the stage", 48, floor, STAGE, "boss_stage_green_door"),
        start(rid, 160, floor),
        # A low dais at the far end, where he sits down.
        solid("dais", 760, floor - 48, w - WALL - 760, 48),
        sign("green_sign", 640, 120, "GREEN ROOM: PERFORMERS ONLY", 420),
        # He retires here: the scene plays once, as the player comes in.
        entity("CutsceneTrigger", 240, floor - 160, 160, 160, cutscene="boss_retirement"),
        door("boss_green_lobby_door", "home to the lobby", w - 112, floor - 48, LOBBY, "boss_lobby_green_arrival",
             bidirectional=False),
    ]
    at = ROOMS_AT[rid][0]
    return rid, room(rid, e, at=at, size=(w, h), biome=BIOME, music=GREEN_MUSIC, bg=BG, title="THE GREEN ROOM",
                     generator=GENERATOR)


ROOMS = (lobby, stage, green_room, hall_stage)

#: The sandbox's defs have no `CutsceneTrigger` (the intro's world has it):
#: the green room's retirement is one.
CUTSCENE_TRIGGER_DEF = """entities:
  - identifier: CutsceneTrigger
    color: "#B07AFF"
    width: 64
    height: 64
    docs: "Starts a cutscene when a player body is inside the rectangle, in this level's room. `cutscene` is the id of a script in the cutscene library; the script must have a seen flag, so it plays once."
    fields:
      - { name: cutscene, type: String, default: "" }
"""


def ensure_cutscene_trigger_def() -> int:
    if '"identifier": "CutsceneTrigger"' in WORLD.read_text():
        return 0
    spec = SPEC_OUT / "cutscene_trigger_def.yaml"
    spec.write_text(CUTSCENE_TRIGGER_DEF)
    code, _ = run("def", "register-entity", str(spec), "--ldtk", str(WORLD), "--in-place", "--no-source-patch")
    return code


#: The hall's door to its copy and the copy's life switch, on the hall's lower
#: floor east of the Overflow's door (`hall_of_bosses`, `sandbox.ldtk`).
HALL_DOOR_YAML = f"""# The Hall of Bosses' door to its copy of the final boss's stage. Written by
# {GENERATOR}.
level_id: {HALL}
entities:
  - type: LoadingZone
    px: [1616, 384]
    size: [48, 96]
    fields:
      id: {HALL_DOOR}
      name: "to the bossofthegame"
      activation: Door
      target_room: {HALL_STAGE}
      target_zone: {HALL_STAGE_ENTRY}
      bidirectional: true
  - type: Switch
    px: [1676, 448]
    size: [24, 32]
    fields:
      id: {HALL_SWITCH}
      name: "bossofthegame life switch"
      prompt: "Revive or defeat the bossofthegame"
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
    if code := ensure_cutscene_trigger_def():
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
