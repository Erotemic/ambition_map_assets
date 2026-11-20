"""The scenery of the Frontier's rooms: `Prop` entities (art, no collision)
that `make_specs.py` lists before each room's other entities, so they draw
behind.

The art is the sprite tools' `targets/props/frontier_props.py`, drawn in each
room's own coordinates over the walk lines `make_specs.py` places (the porch
roofs, the water tower's walk, the freighter's hold, the catwalks). Each
piece names the top left of its frame in its room: the numbers are the art's
(its `PIECES` frames); change them with it.
"""
from __future__ import annotations

from district_scenery import piece

#: Room -> [(kind, frame x, frame y)], furthest back first.
SCENERY = {
    "frontier_landing_pad": [
        ("frontier_pad_freighter", 1280, 280),
        ("frontier_pad_booth", 624, 480),
        ("frontier_pad_cargo", 976, 500),
    ],
    "frontier_main_street": [
        ("frontier_saloon_front", 150, 150),
        ("frontier_store_front", 640, 210),
        ("frontier_water_tower", 1040, 200),
        ("frontier_livery_front", 1600, 160),
        ("frontier_assay_front", 2140, 200),
    ],
    "frontier_wet_whistle": [("frontier_saloon_room", 16, 32)],
    "frontier_livery": [("frontier_livery_room", 16, 32)],
    "frontier_refinery": [
        ("frontier_refinery_tanks", 780, 420),
        ("frontier_cracking_tower", 1660, 0),
    ],
    "frontier_ore_corral": [
        ("frontier_corral_fence", 280, 280),
        ("frontier_corral_west", 16, 300),
        ("frontier_corral_east", 1200, 300),
    ],
    "hall_marshal_gallus_corral": [
        ("frontier_corral_fence", 280, 280),
        ("frontier_corral_west", 16, 300),
        ("frontier_corral_east", 1200, 300),
    ],
    "frontier_saddle_lookout": [("frontier_lookout_post", 900, 180)],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y) for kind, x, y in SCENERY.get(rid, ())]
