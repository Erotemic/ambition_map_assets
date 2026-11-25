"""The development blurb of each room of the Neural dimension: where the
room is, when the scene is, and one fact of the place that the room should
show (`docs/planning/game/neural-dimension.md`).

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
under the room's title. The dimension is made up; its facts are the
fiction's, and each one is something a player can see in the room.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    "neural_callosum": (
        "WHERE: the Callosum, the bridge between the two halves of the Neural dimension. WHEN: always awake.",
        "FACT: the living half is west of the gate and the built half east; the signpost points to memory, attention and biases."),
    "neural_cathedral": (
        "WHERE: the Neural Cathedral, in the Cortex, the living half. WHEN: a busy thought.",
        "FACT: cells that fire together are wired together; memories hang in a gallery over the floor."),
    "neural_weights": (
        "WHERE: the Weights, the built half. WHEN: during training.",
        "FACT: the classifier is sure a rabbit is a red herring; logic gates cross the spikes."),
    "neural_echo_chamber": (
        "WHERE: the Echo Chamber, up on the deck of the Weights. WHEN: the same as always.",
        "FACT: every screen says what you said."),
}
