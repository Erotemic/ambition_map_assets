"""The development blurb of each room of the Unfinished dimension: where the
room is, when the scene is, and one fact of the place that the room should
show (`docs/planning/game/unfinished-dimension.md`).

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
under the room's title. The dimension is made up; its facts are the
fiction's, and each one is something a player can see in the room.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    "unfinished_staging": (
        "WHERE: the Staging Area, the first ground the Boss's agents laid. WHEN: the second sprint, still.",
        "FACT: what is not painted yet is only drawn: the trees stop at a line and go on as outlines."),
    "unfinished_draft": (
        "WHERE: the Draft, east of the Staging Area, over the void. WHEN: before Tuesday (which Tuesday is not specified).",
        "FACT: the slabs hang from cranes; the outlines between them are ideas, and an idea does not hold you."),
    "unfinished_site_office": (
        "WHERE: the Site Office, in the cabin on the Staging Area. WHEN: stand-up.",
        "FACT: three gauges set the dimension's gravity, weather and layers."),
}
