# The Ninja Village (gate address `SILENT`)

A mountain village of the ninja dimension. The world file is
`pvn.ldtk` (the PvN dimension). The gate arrives at the gate shrine, at the zone
`ninja_village_gate_arrival`.

`make_specs.py` writes each room's `.ron` spec and, with `--apply`, makes the
rooms, the Shadow Dojo's door to the forest (`sandbox.ldtk`) and the ladder.
`props.py` gives each room its scenery. Change the scripts, not the specs.
Run them from the repository root.

## The rooms

| room | what it is | who lives there |
| --- | --- | --- |
| `ninja_village_gate_shrine` | the gate shrine; a stone stair up to the torii terrace | Sato (shrine keeper), Nagisa the Gatekeeper (keeps the gate), Kenji (gate-sick courier) |
| `ninja_village_street` | the main street, the tea house, the roofs as a road | Daichi (wants to pass the exam), Ume (tea house) |
| `ninja_village_dojo` | the village dojo and its rank exam | Sensei Hayashi (teacher), Ren (top student and rival) |
| `ninja_village_forest` | the cedar forest; the door to the Shadow Dojo | |

The village is ordinary people. The joke is the institutions (the exam's
forms, the rival form, the shouted names of moves), not the culture.

## The roads

- The low road: shrine floor, street, forest floor.
- At the shrine, the low road goes under the stone stair. The signs
  point along the lower road and up to the torii terrace.
- The high road follows the forest's branches, the roofs of the street,
  the torii terrace, and the shrine's stair. Each room joins the next at
  both heights.
- A ladder at the bakery and the dojo practice platforms connect the
  street to the roofs. Use the third practice platform to reach the tea
  house roof. Use the top platform to reach the dojo roof.
- The way on: the forest's east door goes to `ninja_dojo` (two ways), the
  hall of the Shadow Clan (the Oni leader, the Duelist, the Heavy), and from
  there to the mockingbird arena.

## The rank exam

The exam starts at the red strip. First, defeat the three training dummies.
Then defeat the examiner. The wave book gives the order. Steps at both
ends of the exam beam let a player jump onto it. Use the bell outside
the exam floor to start again. After the exam, Sensei Hayashi awards the rank
(`ninja_village_rank_awarded`). The quest is `ninja_village_rank_exam`
(`quests.ron`); the talk is `dialogue/sandbox/ninja_village.yarn`.

## Bamboo Pass

Cross at bridge level or take the ford below it. The ladder at the west
end and the high stone at the east end lead back to the trail.

## The gate

Agent GATE places the ring and its terminal on the shrine's clear floor
(x 160..512, floor y 704, clear to 224 over the floor). Put those entities in
`gate_interface.yaml` here (an `entity add` spec): `--apply` adds that file
again after it makes the rooms. Until the ring stands, the arrival zone is a
one-way door to the hub.

## Proof

`game/ambition_app/tests/the_ninja_village.rs` walks the loop by keys from
the shrine, talks to each resident, passes the exam by Attack presses, and
goes through the door to the Shadow Dojo and back.
