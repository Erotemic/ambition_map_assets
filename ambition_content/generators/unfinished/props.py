"""The scenery of the Unfinished dimension's rooms: `Prop` entities (art, no
collision) that `make_specs.py` lists before each room's other entities, so
they draw behind.

The art is the sprite tools' `targets/props/unfinished_props.py`, drawn in
each room's own coordinates over the walk lines `make_specs.py` places (the
scaffold's decks; the slabs and the painter's platform under the cranes'
cables). Each piece names the top left of its frame in its room: the
numbers are the art's (its `PIECES` frames); change them with it.
"""
from __future__ import annotations

from district_scenery import piece

#: Room -> [(kind, frame x, frame y)], furthest back first.
SCENERY = {
    "unfinished_staging": [
        ("unfinished_half_trees", 1170, 330),
        ("unfinished_site_cabin", 580, 440),
        ("unfinished_survey_post", 920, 520),
        ("unfinished_scaffold", 1632, 330),
    ],
    "unfinished_draft": [
        ("unfinished_cranes", 680, 24),
        ("unfinished_spill", 540, 590),
        ("unfinished_inspection_scaffold", 588, 488),
    ],
    "unfinished_site_office": [
        ("unfinished_office_wall", 0, 0),
        ("unfinished_gauges", 180, 32),
        ("unfinished_backlog", 920, 160),
    ],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y, *rest) for kind, x, y, *rest in SCENERY.get(rid, ())]
