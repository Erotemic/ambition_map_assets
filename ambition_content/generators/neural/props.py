"""The scenery of the Neural dimension's rooms: `Prop` entities (art, no
collision) that `make_specs.py` lists before each room's other entities, so
they draw behind.

The art is the sprite tools' `targets/props/neural_props.py`, drawn in each
room's own coordinates over the walk lines `make_specs.py` places (the
synapse caps and the arch, the gallery, the dendrite tree's branches, the
logic gates, the racks). Each piece names the top left of its frame in its
room: the numbers are the art's (its `PIECES` frames); change them with it.
"""
from __future__ import annotations

from district_scenery import piece

#: Room -> [(kind, frame x, frame y)], furthest back first.
SCENERY = {
    "neural_callosum": [
        ("neural_callosum_caps", 1076, 312),
        ("neural_signpost", 640, 440),
    ],
    "neural_cathedral": [
        ("neural_cathedral_lift_fibres", 460, 510),
        ("neural_memory_gallery", 580, 32),
        ("neural_dendrite_tree", 1260, 590),
    ],
    "neural_weights": [
        ("neural_training_bypass", 866, 934),
        ("neural_red_herring_board", 1540, 580),
        ("neural_weights_racks", 1950, 600),
        ("neural_logic_gates", 1040, 830),
        ("neural_weights_circuit_walk", 1392, 675),
    ],
    "neural_echo_chamber": [
        ("neural_echo_screens", 16, 32),
        ("neural_echo_viewing_balcony", 240, 268),
    ],
}


def scenery(rid: str) -> list[str]:
    """The `Prop` entities of room `rid`'s scenery, furthest back first."""
    return [piece(kind, x, y, *rest) for kind, x, y, *rest in SCENERY.get(rid, ())]
