#!/usr/bin/env python3
"""Write the lower floor of Castle Godwin (the Evil dimension): the kitchens
under the gatehouse, the Complaints Department, the cells, and the Prototype
Workshop off the lab tower's foot.

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/castle_kitchens/make_specs.py                     # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/castle_kitchens/make_specs.py --apply             # and makes the rooms
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/castle_kitchens/make_specs.py --apply --relayout  # back to WHERE

Run it from the repository root.

Jon (2026-10-30): "build out the world detail ... adding art, flavor,
character"; then: "focus on compositions of levels ... large interconnected
regions ... It needs to feel like a connected world, not a series of
disconnected doors." The castle's staff live on its lower floor, and the
floor joins the castle by its edges on a faithful flat map: a stair down from
the gatehouse (a hole in its floor, `castle_godwin/make_specs.py`) into the
kitchens; east along the floor to the Complaints Department, the cells, and
into the lab tower partway up; the workshop off the tower's foot. With the
barracks into the tower above, the castle is a loop.

Mrs Hargreave the cook, Osgood the night porter, Brigid Dunmore of the
Henchpersons' Guild (`dialogue/sandbox/castle_godwin.yarn`); Agnes Mudge
holding ticket 4,117; Ambrose Quill, the cells' trusty; Dr. Gideon Sprocket.

Where a room is in the world is its LDtk editor's once it exists: `--apply`
keeps each room where it stands; `WHERE` places a new room, or every room
with `--relayout`. `specs/check_flat_map.py evil.ldtk` checks the joins.

The art is the sprite tools' `targets/props/castle_kitchens_props.py`,
`castle_cells_props.py` and `evil_workshop_props.py`.
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
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_castle_kitchens_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))

from district_kit import WALL, WORLDS, edge, entity, ledge, make_rooms, paint, resident, room, run, sign, solid, start  # noqa: E402
from district_scenery import piece  # noqa: E402

WORLD = WORLDS / "evil.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/castle_kitchens/make_specs.py"
KITCHENS = "castle_godwin_kitchens"
COMPLAINTS = "castle_godwin_complaints"
CELLS = "castle_godwin_cells"
#: Behind a false wall at the kitchens' west end: the Guild's secret room.
GUILD = "castle_godwin_guild_room"
GW = 960
WORKSHOP = "castle_godwin_workshop"
GATEHOUSE = "castle_godwin_gatehouse"
TOWER = "castle_godwin_tower"
W, H, FLOOR, CEILING = 1280, 576, 512, 48
CW, CH, CFLOOR = 960, 448, 384
#: The cells: as wide as the gap to the tower, and 64 taller than the rooms
#: by them so their vault meets the barracks' floor (the trapdoor's shaft,
#: x 160..224 under the barracks' 2000..2064).
LW, LH, LFLOOR, LCEILING = 720, 640, 576, 112
TRAPDOOR = (160, 224)
TRAPDOOR_GATE_TOP = 16
TRAPDOOR_CLIMB_TOP = 32
TRAPDOOR_LEVER = "castle_godwin_trapdoor_lever"
#: Where each room goes when it is new (or with `--relayout`): the floor of
#: each at world y 1344, the tower's join to the cells. The kitchens under
#: the gatehouse's stair (their x 40..104 under its x 1240..1304); the
#: complaints and the cells east of them, the cells' east edge on the
#: tower's west; the workshop's floor level with the tower's foot (1728),
#: its west edge on the tower's east.
WHERE = {
    KITCHENS: (3200, 832),
    # West of the kitchens, under the gatehouse's west end.
    GUILD: (3200 - GW, 832),
    COMPLAINTS: (3200 + W, 1344 - CFLOOR),
    CELLS: (3200 + W + CW, 1344 - LFLOOR),
    WORKSHOP: (7184, 1728 - FLOOR),
}
#: The stair up to the gatehouse: the shaft in the kitchens' ceiling (x0, x1).
STAIR = (40, 104)
WORKSHOP_LADDER = (384, 336, 32, 176)
#: A Risen Conscript with no legs (the Crawling Conscript), and its box: low
#: and wide, its body on the floor.
LEGLESS, LEGLESS_BOX = "npc_evil_zombie_crawler", (52, 28)


def legless(rid, n, x, floor):
    """A Crawling Conscript with its middle at `x` on `floor`. It is
    hostile, in among the staff."""
    w, h = LEGLESS_BOX
    return entity("EnemySpawn", x - w // 2, floor - h, w, h, name=f"{rid}_legless_{n}", brain="combatant", character_id=LEGLESS,
                  respawn="OnRoomReenter")


def kitchens():
    s0, s1 = STAIR
    e = [
        piece("castle_kitchens_room", 16, CEILING, name="kitchens_room"),
        solid("floor", 0, FLOOR, W, H - FLOOR),
        solid("ceiling_west", 0, 0, s0, CEILING),
        solid("ceiling_east", s1, 0, W - s1, CEILING),
        # The west wall is false at the floor: a secret way (its zone id
        # `secret_`: the map shows the room behind it only once it is found).
        solid("west_wall", 0, CEILING, WALL, FLOOR - 112 - CEILING),
        edge("secret_kitchens_west", "a draught from the wall", 0, FLOOR, GUILD, "secret_guild_east"),
        solid("east_wall", W - WALL, CEILING, WALL, FLOOR - 112 - CEILING),
        entity("LoadingZone", s0, 0, s1 - s0, 16, id="kitchens_stair", name="up the stair to the gatehouse",
               activation="EdgeExit", target_room=GATEHOUSE, target_zone="castle_godwin_gatehouse_stair", bidirectional=True),
        edge("kitchens_east", "on to the Complaints Department", W - WALL, FLOOR, COMPLAINTS, "complaints_west"),
        start(KITCHENS, 160, FLOOR),
        ledge("pantry_crates", 336, 448, 112),
        ledge("pantry_shelf", 352, 384, 128),
        ledge("pantry_hearth_walk", 496, 352, 368),
        ledge("pantry_dining_walk", 880, 384, 288),
        ledge("dumbwaiter_crates", 1168, 448, 80),
        resident("npc_castle_osgood", "castle_osgood", 280, FLOOR),
        resident("npc_castle_hargreave", "castle_hargreave", 860 - 20, FLOOR),
        resident("npc_castle_dunmore", "castle_dunmore", 1040, FLOOR),
        # Under the cook's table, after the scraps.
        legless(KITCHENS, 1, 600, FLOOR),
        sign("kitchens_sign_menu", 660, 240, "TODAY: gruel. TOMORROW: gruel (evil)", 400),
        sign("kitchens_sign_guild", 1010, 417, "HENCHPERSONS' GUILD, LOCAL 666", 300),
        sign("kitchens_sign_meeting", 1010, 445, "Meeting at the kettle", 300),
    ]
    return room(KITCHENS, e, at=WHERE[KITCHENS], size=(W, H), biome="castle_godwin", music="doves_of_the_commons", bg="#1A1416",
                title="THE CASTLE KITCHENS", generator=GENERATOR)


def complaints():
    e = [
        piece("complaints_room", 16, CEILING, name="complaints_room"),
        solid("floor", 0, CFLOOR, CW, CH - CFLOOR),
        solid("ceiling", 0, 0, CW, CEILING),
        solid("west_wall", 0, CEILING, WALL, CFLOOR - 112 - CEILING),
        solid("east_wall", CW - WALL, CEILING, WALL, CFLOOR - 112 - CEILING),
        edge("complaints_west", "back to the kitchens", 0, CFLOOR, KITCHENS, "kitchens_east"),
        edge("complaints_east", "on to the cells", CW - WALL, CFLOOR, CELLS, "cells_west"),
        start(COMPLAINTS, 120, CFLOOR),
        ledge("complaints_suggestions_crate", 368, 352, 48),
        ledge("complaints_counter", 416, 320, 464),
        ledge("complaints_forms_crate", 880, 352, 64),
        resident("npc_evil_mudge", "evil_mudge", 200, CFLOOR),
        sign("complaints_sign_ticket", 316, 290, "TAKE A NUMBER", 200),
        sign("complaints_sign_hours", 660, 340, "OPEN: by appointment. APPOINTMENTS: by complaint", 470),
        sign("complaints_sign_serving", 615, 70, "NOW SERVING", 160),
        sign("complaints_sign_box", 384, 248, "SUGGESTIONS", 160),
    ]
    return room(COMPLAINTS, e, at=WHERE[COMPLAINTS], size=(CW, CH), biome="castle_godwin", music="doves_of_the_commons",
                bg="#1A1416", title="THE COMPLAINTS DEPARTMENT", generator=GENERATOR)


def workshop():
    e = [
        piece("workshop_room", 16, CEILING, name="workshop_room"),
        solid("floor", 0, FLOOR, W, H - FLOOR),
        solid("ceiling", 0, 0, W, CEILING),
        solid("west_wall", 0, CEILING, WALL, FLOOR - 112 - CEILING),
        solid("east_wall", W - WALL, CEILING, WALL, FLOOR - CEILING),
        edge("workshop_west", "back into the lab tower", 0, FLOOR, TOWER, "castle_godwin_tower_foot"),
        start(WORKSHOP, 140, FLOOR),
        ledge("workshop_boiler_walk", 416, 336, 480),
        ledge("workshop_receiving_deck", 976, 336, 128),
        ledge("workshop_test_stand", 1056, 400, 80),
        ledge("workshop_loading_step", 1136, 464, 64),
        resident("npc_castle_sprocket", "castle_sprocket", 790, FLOOR),
        entity("ChestSpawn", 1000, 336 - 58, 76, 58, name="a crate of spare parts", reward="currency:40"),
        sign("workshop_sign_kettle", 1000, 390, "MARK 47: almost", 180),
        sign("workshop_sign_button", 1220, FLOOR - 110, "DO NOT", 100),
        sign("workshop_sign_tools", 255, 220, "RETURN THE BIG SPANNER", 300),
    ]
    return room(WORKSHOP, e, at=WHERE[WORKSHOP], size=(W, H), biome="castle_godwin", music="doves_of_the_commons", bg="#1A1416",
                title="THE PROTOTYPE WORKSHOP", generator=GENERATOR)


def cells():
    """The cells: where the complaints end up, down the chute from the
    suggestions box, and the people who made them. Ambrose Quill, the
    trusty, out of the open cell (`castle_godwin.yarn`)."""
    t0, t1 = TRAPDOOR
    e = [
        piece("castle_cells_room", 16, LCEILING, name="cells_room"),
        solid("floor", 0, LFLOOR, LW, LH - LFLOOR),
        solid("vault_west", 0, 0, t0, LCEILING),
        solid("vault_east", t1, 0, LW - t1, LCEILING),
        solid("west_wall", 0, LCEILING, WALL, LFLOOR - 112 - LCEILING),
        solid("east_wall", LW - WALL, LCEILING, WALL, LFLOOR - 112 - LCEILING),
        edge("cells_west", "back to the Complaints Department", 0, LFLOOR, COMPLAINTS, "complaints_east"),
        edge("cells_east", "into the lab tower", LW - WALL, LFLOOR, TOWER, "castle_godwin_tower_cells"),
        # The shortcut: a ladder up the shaft to the barracks' trapdoor, shut
        # until this lever is pulled.
        entity("LoadingZone", t0, 0, t1 - t0, 16, id="cells_trapdoor", name="up through the trapdoor to the barracks",
               activation="EdgeExit", target_room="castle_godwin_barracks", target_zone="castle_godwin_barracks_trapdoor",
               bidirectional=True),
        entity("LockWall", t0, TRAPDOOR_GATE_TOP, t1 - t0, TRAPDOOR_CLIMB_TOP - TRAPDOOR_GATE_TOP,
               id="cells_trapdoor_cover", name="the barracks trapdoor",
               gated_by=f"world.switch_on {TRAPDOOR_LEVER}", look="castle_cracked_floor"),
        entity("Switch", 600, LFLOOR - 32, 24, 32, id=TRAPDOOR_LEVER, name="the trapdoor lever", prompt="Pull the lever",
               action="ToggleFlag", target_encounter=""),
        start(CELLS, 300, LFLOOR),
        ledge("cells_paper_crate", 96, 512, 64),
        ledge("cells_file_walk", 224, 464, 336),
        ledge("cells_desk", 544, 528, 144),
        resident("npc_castle_quill", "castle_quill", 420, LFLOOR),
        # A prisoner the castle forgot, and raised anyway: it drags itself
        # out from under the chute.
        legless(CELLS, 1, 190, LFLOOR),
        sign("cells_sign_chute", 104, 144, "SUGGESTIONS", 132),
        sign("cells_sign_received", 104, 172, "Received", 132),
        sign("cells_sign_rules", 520, 180, "NO COMPLAINING", 220),
        sign("cells_sign_trapdoor", 573, 346, "TRAPDOOR TO THE BARRACKS", 235),
        sign("cells_sign_lever", 573, 374, "Lever by the desk", 235),
    ]
    return room(CELLS, e, at=WHERE[CELLS], size=(LW, LH), biome="castle_godwin", music="doves_of_the_commons", bg="#1A1416",
                title="THE CELLS", generator=GENERATOR)


def guild():
    """The Henchpersons' Guild's secret room, behind the kitchens' false west
    wall: chairs facing a lectern, the banner, the demands, the ballot box,
    and the strike fund (a chest). A meeting is in session: three of the
    castle's own, off the clock, so not fighting (`castle_godwin.yarn`
    `guild_*`)."""
    e = [
        piece("castle_guild_room", 16, CEILING, name="guild_room"),
        solid("floor", 0, FLOOR, GW, H - FLOOR),
        solid("ceiling", 0, 0, GW, CEILING),
        solid("west_wall", 0, CEILING, WALL, FLOOR - CEILING),
        solid("east_wall", GW - WALL, CEILING, WALL, FLOOR - 112 - CEILING),
        edge("secret_guild_east", "back through the false wall to the kitchens", GW - WALL, FLOOR, KITCHENS, "secret_kitchens_west"),
        start(GUILD, GW - 140, FLOOR),
        ledge("guild_speakers_dais", 432, 448, 176),
        ledge("guild_minutes_bench", 704, 448, 160),
        entity("ChestSpawn", 600, FLOOR - 58, 76, 58, name="the strike fund", reward="currency:66"),
        sign("guild_sign", 520, 292, "HENCHPERSONS' GUILD", 236),
        sign("guild_sign_members", 520, 318, "LOCAL 666 · members only", 236),
        sign("guild_sign_demands", 780, 248, "DEMANDS", 176),
        sign("guild_demand_dental", 780, 272, "Dental", 176),
        sign("guild_demand_shouting", 780, 296, "Less shouting", 176),
        sign("guild_demand_helmets", 780, 320, "Helmets that fit", 176),
        resident("npc_fascist_clubman", "guild_clubman", 200, FLOOR),
        resident("npc_fascist_swordsman", "guild_swordsman", 748, 448),
        resident("npc_evil_failed_prototype", "guild_prototype", 490, 448),
    ]
    return room(GUILD, e, at=WHERE[GUILD], size=(GW, H), biome="castle_godwin", music="doves_of_the_commons", bg="#1A1416",
                title="THE GUILD ROOM", generator=GENERATOR)


#: Each room's spec, the workshop first: a room may only stand where no other
#: does, and the old places overlap the new.
ROOMS = ((WORKSHOP, workshop), (COMPLAINTS, complaints), (KITCHENS, kitchens), (CELLS, cells), (GUILD, guild))


def main(argv):
    paths = []
    for rid, make in ROOMS:
        path = SPEC_OUT / f"{rid}.ron"
        path.write_text(make())
        print(path)
        paths.append(path)
    if "--apply" not in argv:
        return 0
    # The rooms name each other: only the end state is checked.
    make_rooms(WORLD, paths, keep_position="--relayout" not in argv)
    if code := paint(WORLD, KITCHENS, "Climbable", 1, STAIR[0] + 16, 0, 32, FLOOR):
        return code
    if code := paint(WORLD, WORKSHOP, "Climbable", 1, *WORKSHOP_LADDER):
        return code
    # The ladder ends at the cover. A climb permits blocks that overlap the ladder.
    if code := paint(WORLD, CELLS, "Climbable", 1, TRAPDOOR[0] + 16, TRAPDOOR_CLIMB_TOP, 32, LFLOOR - TRAPDOOR_CLIMB_TOP):
        return code
    code, _ = run("validate", str(WORLD))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
