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

#: Room -> [(kind, frame x, frame y[, the sheet's pixels to a world unit])],
#: furthest back first. The big pieces are drawn at 1 px a unit, the rest at 2.
SCENERY = {
    "frontier_landing_pad": [
        ("frontier_pad_freighter", 1280, 280),
        ("frontier_pad_booth", 624, 480),
        ("frontier_pad_cargo", 976, 500),
        ("frontier_pad_loading_walk", 530, 482),
        ("frontier_pad_service_steps", 1736, 480),
    ],
    "frontier_main_street": [
        ("frontier_saloon_front", 150, 150),
        ("frontier_store_front", 640, 210),
        ("frontier_water_tower", 1040, 200),
        ("frontier_livery_front", 1600, 160),
        ("frontier_assay_front", 2140, 200),
        ("frontier_water_tower_service_walk", 1436, 386),
    ],
    "frontier_wet_whistle": [
        ("frontier_saloon_room", 16, 32),
        ("frontier_saloon_balcony_walk", 128, 318),
    ],
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
    # The first slice (`targets/props/frontier_slice_props.py`).
    "frontier_siding_station": [("frontier_siding_station_house", 620, 370)],
    "frontier_siding_street": [
        ("frontier_siding_windmill", 1100, 200),
        ("frontier_lie_down_inn_front", 150, 160),
        ("frontier_mercantile_front", 670, 220),
        ("frontier_telegraph_front", 1430, 170),
    ],
    "frontier_lie_down_inn": [("frontier_lie_down_inn_room", 16, 32)],
    "frontier_siding_trestle": [("frontier_siding_trestle", 0, 380, 1.0)],
    "frontier_sprocket_row": [
        ("frontier_sprocket_arch", 40, 360),
        ("frontier_hettie_garage", 470, 200),
        ("frontier_parts_yard", 1150, 470),
        ("frontier_rolling_gate", 1630, 300),
    ],
    "frontier_freight_tail": [
        ("frontier_freight_track_tail", 0, 700, 1.0),
        ("frontier_caboose", 10, 400),
        ("frontier_box_car_1", 530, 470),
        ("frontier_box_car_2", 1074, 470),
        ("frontier_flat_car_1", 1636, 470),
    ],
    "frontier_freight_cars": [
        ("frontier_freight_track_cars", 0, 700, 1.0),
        ("frontier_flat_car_1_end", 0, 590),
        ("frontier_tank_car", 410, 500),
        ("frontier_ore_car", 954, 540),
        ("frontier_box_car_3", 1498, 486),
        ("frontier_flat_car_2", 2076, 530),
    ],
    "frontier_rustler_head": [
        ("frontier_freight_track_head", 0, 700, 1.0),
        ("frontier_flat_car_2_end", 0, 530),
        ("frontier_box_car_4", 350, 470),
        ("frontier_rustler", 720, 300, 1.0),
    ],
    "frontier_clinker_yard": [
        ("frontier_yard_tracks", 0, 1240, 1.0),
        ("frontier_tipple_road", 480, 330, 1.0),
    ],
    "frontier_clinker_works": [
        ("frontier_furnace_house", 90, 60),
        ("frontier_works_crane", 800, 280),
        ("frontier_slag_pots", 690, 560),
    ],
    "frontier_clinker_row": [
        ("frontier_row_shacks_west", 220, 470),
        ("frontier_row_pump", 880, 430),
        ("frontier_row_shacks_east", 1580, 470),
    ],
    "frontier_clinker_railhead": [("frontier_railhead_grade", 0, 600, 1.0)],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y, *rest) for kind, x, y, *rest in SCENERY.get(rid, ())]
