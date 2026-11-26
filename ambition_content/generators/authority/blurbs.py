"""The development blurb of each room of the Central Hub, the Gate
Authority's capital: where the room is, when the scene is, and one fact of
the place that the room should show
(`docs/planning/game/central-hub-dimension.md`).

`make_specs.py` writes each blurb as two `DebugLabel`s of category `Room`
under the room's title. The dimension is made up; its facts are the
fiction's, and each one is something a player can see in the room.
"""

#: Room id -> (where and when, a fact).
BLURB = {
    "authority_concourse": (
        "WHERE: the Concourse, the arrival hall of the Central Hub. WHEN: a weekday, the morning rush.",
        "FACT: the Authority's own gate is LEGAL, the one address posted on every terminal; bags from every dimension come back through it, some of them changed."),
    "authority_plaza": (
        "WHERE: Authority Plaza, the seat of the Gate Authority. WHEN: blossom season, the armistice holding.",
        "FACT: every licensed gate keeps its time by the great clock."),
    "authority_manifest_office": (
        "WHERE: the Manifest Office, off Authority Plaza. WHEN: number 4,096.",
        "FACT: no record here is ever deleted, only corrected."),
}
