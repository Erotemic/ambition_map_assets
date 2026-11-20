"""The development blurb of each room of the Frontier dimension: where the
room is, when the scene is, and one fact of the place that the room should
show (`docs/planning/game/leadensaddle.md`).

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
under the room's title, so that the author and the playtester can see at a
glance what a room is for. The Frontier is made up; its facts are the
fiction's, and each one is something a player can see in the room.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    "frontier_landing_pad": (
        "WHERE: Pad Three, Dry Dock, in the Leaden Saddle. WHEN: the morning a freighter is in.",
        "FACT: the gate stands on the landing apron; the Marshal charges a toll to use it."),
    "frontier_main_street": (
        "WHERE: Main Street, Dry Dock. WHEN: the same morning, before the whistle.",
        "FACT: the town is one street of false fronts between the pads and the refinery."),
    "frontier_wet_whistle": (
        "WHERE: The Wet Whistle, the saloon on Main Street. WHEN: morning; the night shift drinks coffee.",
        "FACT: the saloon sells water by the glass; the coolant on the shelf is not for drinking."),
    "frontier_livery": (
        "WHERE: Bell's Livery, Main Street. WHEN: morning feed.",
        "FACT: the Bells hire mules by the day for the pass; nothing with an engine climbs it."),
    "frontier_refinery": (
        "WHERE: the refinery on the flank of the east mesa. WHEN: shift change.",
        "FACT: the road climbs in terraces from the town to the corral, past the tanks and the cracking tower."),
    "frontier_ore_corral": (
        "WHERE: the Ore Corral, where the ore carts are loaded. WHEN: noon.",
        "FACT: the Marshal holds court here; the gate to the mesa top opens when he is beaten."),
    "frontier_saddle_lookout": (
        "WHERE: the top of the east mesa, over the Leaden Saddle. WHEN: the afternoon after.",
        "FACT: from here the pass, the town and all three pads are in sight."),
}
