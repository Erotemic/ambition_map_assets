"""The scenery of the Business dimension's rooms: `Prop` entities (art, no
collision) that `make_specs.py` lists before each room's other entities, so
they draw behind.

The art is the sprite tools' `targets/props/business_props.py`, drawn in
each room's own coordinates over the walk lines `make_specs.py` places (the
café's awning and balcony, the fountain's rim and pedestal, the catwalks, the
lecture hall's tiers). Each piece names the top left of its frame in its
room: the numbers are the art's (its `PIECES` frames); change them with it.
"""
from __future__ import annotations

from district_scenery import piece

#: Room -> [(kind, frame x, frame y)], furthest back first.
SCENERY = {
    "business_founders_plaza": [
        ("business_cafe_front", 600, 290),
        ("business_college_front", 2060, 140),
        ("business_founder_statue", 1260, 300),
        ("business_picket_line", 1690, 480),
    ],
    "business_records_processing": [
        ("business_records_desk", 540, 320),
        ("business_stamp_press", 580, 600),
        ("business_records_conveyor", 160, 900),
        ("business_shredder", 1250, 800),
    ],
    "business_college_lecture_hall": [("business_lecture_room", 16, 32)],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y, *rest) for kind, x, y, *rest in SCENERY.get(rid, ())]
