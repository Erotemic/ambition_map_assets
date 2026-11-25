"""The development blurb of each room of the Automaton dimension: where the
room is, when the scene is, and one fact of the place that the room should
show (`docs/planning/game/automaton-dimension.md`).

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
under the room's title. The facts are mathematics, and each one is
something a player can see in the room.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    "automaton_works": (
        "WHERE: the Works, the clockwork town by the gate CELLS. WHEN: on the tick.",
        "FACT: the busy beaver is the machine that writes the most ones before it halts; he is still building."),
    "automaton_life": (
        "WHERE: the Life field, east of the Works. WHEN: generation after generation.",
        "FACT: a glider moves one cell diagonally every four generations; ride one."),
    "automaton_tape_room": (
        "WHERE: the Tape Room, in the clock tower. WHEN: step 47,176,870, the last.",
        "FACT: five states, one tape: the champion runs 47,176,870 steps and halts with 4,098 ones (BB(5), proved 2024)."),
    "automaton_arena": (
        "WHERE: the Cell-ular Arena, east of the Life field. WHEN: the next challenger's turn.",
        "FACT: rule 150 on a ring of sixteen cells, from two eight apart, repeats every four generations; the ring's face shows all four."),
}
