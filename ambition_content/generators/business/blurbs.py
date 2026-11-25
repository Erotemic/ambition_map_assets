"""The development blurb of each room of the Business dimension: where the
room is, when the scene is, and one fact of the place that the room should
show (`docs/planning/game/business-dimension.md`).

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
under the room's title. Capital is made up; its facts are the fiction's,
and each one is something a player can see in the room.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    "business_founders_plaza": (
        "WHERE: Founders' Plaza, Capital, the Business dimension. WHEN: the golden hour of a long working day.",
        "FACT: the gate stands by the Founder's fountain; the records clerks picket under his statue."),
    "business_records_processing": (
        "WHERE: Records & Processing, east of the plaza. WHEN: the same afternoon, the floor half-staffed.",
        "FACT: every form in Capital comes through here, is stamped, and goes back out to be filled in again."),
    "business_college_lecture_hall": (
        "WHERE: Lecture Hall 101, Capital Business College. WHEN: the afternoon lecture.",
        "FACT: the college teaches Synergy; the best attendance in the class is Zorlack 65536's."),
}
