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
    # The first slice west of Dry Dock (`docs/planning/game/techno-western-frontier-first-slice.md`).
    "frontier_siding_station": (
        "WHERE: Halfway Siding, the auxiliary gate terminal on the gulch rim. WHEN: a gate arrives mid-morning.",
        "FACT: the gate shares a platform with the rail halt; the agent sells tickets for both."),
    "frontier_siding_street": (
        "WHERE: the one street of Halfway Siding. WHEN: mid-morning, the freight not yet due.",
        "FACT: the town lives off the travellers who arrive sick and must rest before going on."),
    "frontier_lie_down_inn": (
        "WHERE: The Lie-Down Inn, Halfway Siding. WHEN: mid-morning; the cots are full of the gate-sick.",
        "FACT: rooms are let by the hour, and every cot has a bucket beside it."),
    "frontier_siding_trestle": (
        "WHERE: the Halfway Trestle over the gulch. WHEN: 9:40, as the ore freight passes under.",
        "FACT: the rail line runs on the gulch floor; the trestle carries the road to the mechanics."),
    "frontier_sprocket_row": (
        "WHERE: Sprocket Row, the mechanics' street across the trestle. WHEN: late morning.",
        "FACT: the fitters and smiths of the siding keep shop here; their yards run on past the gate."),
    "frontier_freight_tail": (
        "WHERE: the tail of the Number 9 ore freight, down the gulch. WHEN: 9:40, at speed.",
        "FACT: an outlaw engine has coupled on at the head; the crew at the tail cannot stop it."),
    "frontier_freight_cars": (
        "WHERE: the middle of the Number 9 freight. WHEN: the same run, the gulch narrowing.",
        "FACT: ore cars, a tank car and loose crates; the shaking moves the cargo."),
    "frontier_rustler_head": (
        "WHERE: the head of the Number 9, behind the outlaw engine. WHEN: the run, nearing the flats.",
        "FACT: the Rustler steals freight by the car load and hauls it past Clinker Flats."),
    "frontier_clinker_yard": (
        "WHERE: the rail yard of Clinker Flats, down the line from the siding. WHEN: noon.",
        "FACT: the freight passes slowly through the yard; the tipple road climbs to the works."),
    "frontier_clinker_works": (
        "WHERE: the smelter works over Clinker Flats. WHEN: noon, the furnaces lit.",
        "FACT: the works smelt the ore that the freights bring down; the slag goes on the heaps."),
    "frontier_clinker_row": (
        "WHERE: the Row, the shacks under the works. WHEN: noon, the shift at lunch.",
        "FACT: the smelter hands live under the works, out of the wind and in the soot."),
    "frontier_clinker_railhead": (
        "WHERE: the railhead east of Clinker Flats. WHEN: the afternoon.",
        "FACT: the line runs on east to Dry Dock and its pads; the old tramway grade comes down from the works."),
}
