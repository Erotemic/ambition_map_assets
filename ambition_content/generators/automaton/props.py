"""The scenery of the Automaton dimension's rooms: `Prop` entities (art, no
collision) that `make_specs.py` lists before each room's other entities, so
they draw behind.

The art is the sprite tools' `targets/props/automaton_props.py`, drawn in
each room's own coordinates over the walk lines `make_specs.py` places (the
steps of Busy Beaver's stair of blocks; the Life field's terrace). Each
piece names the top left of its frame in its room: the numbers are the
art's (its `PIECES` frames); change them with it.
"""
from __future__ import annotations

from district_scenery import piece

#: Room -> [(kind, frame x, frame y)], furthest back first.
SCENERY = {
    "automaton_works": [
        ("automaton_cafe", 560, 200),
        ("automaton_waterwheel", 1040, 250),
        ("automaton_clock_tower", 1940, 30),
        ("automaton_block_stairs", 1396, 376),
    ],
    "automaton_life": [
        ("automaton_sierpinski_panel", 2060, 120),
        ("automaton_still_life", 1170, 760),
    ],
    "automaton_tape_room": [
        ("automaton_state_table", 1050, 100),
        ("automaton_tape", 60, 250),
    ],
    "automaton_arena": [
        ("automaton_failure_log", 150, 220),
        ("automaton_arena_ring", 816, 560),
    ],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y, *rest) for kind, x, y, *rest in SCENERY.get(rid, ())]
