"""The scenery of the Central Hub's rooms: `Prop` entities (art, no
collision) that `make_specs.py` lists before each room's other entities, so
they draw behind.

The art is the sprite tools' `targets/props/authority_props.py`, drawn in
each room's own coordinates over the walk lines `make_specs.py` places (the
catwalk, the stairwell's steps, the conveyor, the balcony and its steps, the
planter, the benches and the bough, the chairs, the cabinets). Each piece
names the top left of its frame in its room: the numbers are the art's (its
`PIECES` frames); change them with it.
"""
from __future__ import annotations

from district_scenery import piece

#: Room -> [(kind, frame x, frame y)], furthest back first.
SCENERY = {
    "authority_concourse": [
        ("authority_baggage_wall_west", 8, 696),
        ("authority_baggage_wall_east", 1176, 696),
        ("authority_baggage_hall", 16, 704),
        ("authority_stairwell", 1720, 620),
        ("authority_catwalk", 940, 470),
        ("authority_info_booth", 620, 400),
    ],
    "authority_plaza": [
        ("authority_clock_arcade", 0, 140),
        ("authority_blossom_tree", 780, 160),
        ("authority_notice_board", 1610, 420),
        ("authority_manifest_portico", 2100, 350),
    ],
    "authority_manifest_office": [
        ("authority_filing_cabinets", 1210, 32),
        ("authority_office_counter", 200, 150),
    ],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y, *rest) for kind, x, y, *rest in SCENERY.get(rid, ())]
