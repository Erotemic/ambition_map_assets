#!/usr/bin/env python3
"""Write the rooms of the Neural dimension: the Cortex, the living half, and
the Weights, the built half (`docs/planning/game/neural-dimension.md`).

    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/neural/make_specs.py          # writes the specs
    uv run --project tools/ambition_ldtk_tools python game/ambition_map_assets/ambition_content/generators/neural/make_specs.py --apply  # and makes the rooms

Run it from the repository root. Change the script, not the rooms.

The world file is `neural.ldtk`. The gate (address LATENT) stands on the
Callosum, the bridge between the two halves. The three outdoor rooms join
by edges; the Echo Chamber is a room you go into, so its way in is a door:

                                                  door
                                          [the Echo Chamber]
                                                  |
 [ the Neural Cathedral ] ==== [ the Callosum ] ==== [ the Weights ]

- `neural_callosum`: the gate, terminal, signpost, and Grandmother Cell.
  Synapse caps and an upright fibre bundle lead to the arch and its chest.
- `neural_cathedral`: the living half. A pool of fluid in the floor; the
  dendrite tree, whose branches climb to the gallery of memories; Donna
  Hebb; Intrusive Thoughts in the air.
- `neural_weights`: the built half. Percy the Perceptron on the floor; a
  bed of spikes crossed by two logic gates; the classifier's board; racks
  up to the deck and the Echo Chamber's door; Attention Heads in the air.
- `neural_echo_chamber`: a round room of screens, and Echo.

The robot's numbers (`district_kit`): a jump rises 83, a jump and a double
jump 139; a step of 64 is one jump, 128 a double jump.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
#: The shared generator code and the authoring tool stay in the main repo.
TOOL_ROOT = HERE.parents[4] / "tools" / "ambition_ldtk_tools"
TOOL_SPECS = TOOL_ROOT / "specs"
#: The area specs are made again on each run and not kept: the rooms are the truth.
SPEC_OUT = Path(tempfile.gettempdir()) / "ambition_neural_specs"
SPEC_OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(TOOL_SPECS))
sys.path.insert(0, str(TOOL_SPECS / "gate_network"))
sys.path.insert(0, str(HERE))

from district_kit import WALL, WORLDS, door, edge, ensure_world, entity, ledge, make_rooms, resident, room, run, sign, solid, start, water  # noqa: E402

import gates  # noqa: E402
from blurbs import BLURB  # noqa: E402
from props import scenery  # noqa: E402

WORLD = WORLDS / "neural.ldtk"
GENERATOR = "game/ambition_map_assets/ambition_content/generators/neural/make_specs.py"
UID_OFFSET = 1700000

CALLOSUM = "neural_callosum"
CATHEDRAL = "neural_cathedral"
WEIGHTS = "neural_weights"
ECHO = "neural_echo_chamber"

BG = "#1A1030"
MUSIC = "the_algorithm_knows_youre_lonely"

#: Each room: where it is on the flat map, and its size. The three outdoor
#: rooms are side by side, their floors at one height where they join; the
#: Echo Chamber is above the Weights.
ROOMS_AT = {
    CALLOSUM: ((0, 0), (2400, 768)),
    CATHEDRAL: ((-2400, -384), (2400, 1152)),
    WEIGHTS: ((2400, -384), (2400, 1152)),
    ECHO: ((3200, -1104), (1280, 576)),
}

#: The Callosum (`targets/props/neural_props.py` draws to these).
CALLOSUM_FLOOR = 640
CAPS = ((1104, 576, 112), (1280, 512, 144), (1488, 448, 96))
ARCH = (1600, 2000, 368)
FIBRE_CLIMB = (2032, 320, 32, 320)
#: The Neural Cathedral.
CATHEDRAL_FLOOR = 1024
POOL = (800, 1120, 64)
GALLERY = (600, 1240, 544)
GALLERY_LIFT = (480, 592, 992)
BRANCHES = ((1300, 1500, 896), (1560, 1760, 768), (1300, 1500, 640))
#: The Weights.
WEIGHTS_FLOOR = 1024
SPIKES = (1100, 1340)
GATES = ((1080, 1200, 928), (1240, 1360, 848))
WEIGHTS_SHAFTS = ((960, 1024), (1408, 1472))
WEIGHTS_TUNNEL_FLOOR = 1120
RACKS = ((1960, 2140, 896), (2180, 2360, 768))
DECK = (1960, 2384, 640)
#: The Echo Chamber.
ECHO_FLOOR = 512
ECHO_SEATS = (
    ("west_lower_seats", 256, 384, 448),
    ("west_upper_seats", 400, 512, 384),
    ("viewing_balcony", 528, 848, 320),
    ("east_upper_seats", 864, 976, 384),
    ("east_lower_seats", 992, 1120, 448),
)


def side_walls(w, h, west, east):
    """The side walls of a room, over the floor where each side's edge
    stands (`None`: a whole wall, no edge on that side)."""
    out = []
    for side, x, floor in (("west", 0, west), ("east", w - WALL, east)):
        out.append(solid(f"{side}_wall", x, 0, WALL, (floor - 96) if floor is not None else h))
    return out


def blurb(rid, x):
    """The room's blurb (`blurbs.py`): two lines under its title."""
    out = []
    for n, text in enumerate(BLURB[rid]):
        w = len(text) * 9 + 24
        out.append(entity("DebugLabel", x - w // 2, 64 + n * 24, w, 24, name=f"{rid}_blurb_{n}", text=text, category="Room"))
    return out


def chest(name, reward, x, floor):
    return entity("ChestSpawn", x, floor - 58, 76, 58, name=name, reward=reward)


def flier(rid, character, n, x, y, w=40, h=40):
    """A thing that flies, where it waits in the air when the room opens."""
    return entity("EnemySpawn", x - w // 2, y - h // 2, w, h, name=f"{rid}_{character}_{n}", brain="combatant",
                  character_id=character, respawn="OnRoomReenter")


def ground_enemy(rid, character, x, floor, w, h):
    return entity("EnemySpawn", x - w // 2, floor - h, w, h, name=f"{rid}_{character}_0", brain="combatant",
                  character_id=character, respawn="OnRoomReenter")


def build(rid, e, title, biome, dangerous=False, extra=""):
    at, size = ROOMS_AT[rid]
    text = room(rid, scenery(rid) + e + blurb(rid, size[0] // 2), at=at, size=size, biome=biome, music=MUSIC, bg=BG, title=title,
                generator=GENERATOR, dangerous=dangerous, extra=extra)
    return rid, text


def callosum():
    rid = CALLOSUM
    w, h = ROOMS_AT[rid][1]
    floor = CALLOSUM_FLOOR
    a0, a1, arch = ARCH
    e = [
        solid("bridge", 0, floor, w, h - floor),
        *side_walls(w, h, floor, floor),
        edge("callosum_to_cathedral", "west, to the living half", 0, floor, CATHEDRAL, "cathedral_to_callosum"),
        # The gate (LATENT) and its terminal: the way in and the way home.
        *gates.as_ron(gates.ring("Callosum Gate", "neural_callosum_gate", 96, floor, "the gate")),
        *gates.as_ron(gates.terminal("Callosum Gate", "neural_gate_terminal", 400, floor)),
        start(rid, 540, floor),
        sign("callosum_sign_gate", 300, floor - 360, "LATENT: THE CALLOSUM", 300),
        # The signpost's three boards.
        sign("callosum_sign_memory", 690, 501, "< MEMORY", 120),
        sign("callosum_sign_attention", 740, 547, "ATTENTION ^", 140),
        sign("callosum_sign_biases", 790, 581, "BIASES >", 120),
        resident("npc_neural_grandmother_cell", "neural_grandmother", 1000, floor),
        # The caps lead up to the arch from the west.
        *[ledge(f"synapse_cap_{n}", x, top, cap_w) for n, (x, top, cap_w) in enumerate(CAPS)],
        ledge("fibre_arch", a0, arch, a1 - a0),
        chest("a misplaced memory", "currency:30", 1760, arch),
        edge("callosum_to_weights", "east, to the built half", w - WALL, floor, WEIGHTS, "weights_to_callosum"),
    ]
    x, top, width, height = FIBRE_CLIMB
    climb = f'( kind: "Ladder", px: [{x}, {top}], size: [{width}, {height}] )'
    return build(rid, e, "THE CALLOSUM", "neural", extra=f"\n    intgrid: (climbable: [{climb}]),")


def cathedral():
    rid = CATHEDRAL
    w, h = ROOMS_AT[rid][1]
    floor = CATHEDRAL_FLOOR
    p0, p1, depth = POOL
    g0, g1, gallery = GALLERY
    lift_left, lift_right, lift_bottom = GALLERY_LIFT
    e = [
        solid("floor_west", 0, floor, p0, h - floor),
        solid("pool_bed", p0, floor + depth, p1 - p0, h - floor - depth),
        solid("floor_east", p1, floor, w - p1, h - floor),
        water("neural_cathedral_pool", p0, floor, p1 - p0, depth),
        solid("vault", 0, 0, w, 32),
        *side_walls(w, h, None, floor),
        edge("cathedral_to_callosum", "east, to the Callosum", w - WALL, floor, CALLOSUM, "callosum_to_cathedral"),
        start(rid, w - 120, floor),
        resident("npc_neural_hebb", "neural_hebb", 320, floor),
        # The dendrite tree's branches, a double jump each, and the gallery
        # of memories west of the top one.
        *[ledge(f"branch_{n}", x0, top, x1 - x0) for n, (x0, x1, top) in enumerate(BRANCHES)],
        ledge("memory_gallery", g0, gallery, g1 - g0),
        entity("MovingPlatform", lift_left, lift_bottom, lift_right - lift_left, 16,
               id="neural_cathedral_gallery_lift", name="Memory lift", speed=168.0,
               lift_dy=float(gallery - lift_bottom), one_way=True, visual="neural_cathedral_memory_lift"),
        chest("a memory of a good day", "currency:35", 880, gallery),
        sign("cathedral_sign_gallery", (g0 + g1) // 2, 250, "THE GALLERY OF MEMORIES (SOME OF THEM YOURS)", 520),
        # The diver has dragged his chest out of the pool; leave room for its swing.
        entity("EnemySpawn", 1252, floor - 72, 36, 72,
               name="neural_cathedral_sunk_cost_fallacy_0", brain="combatant",
               character_id="sunk_cost_fallacy", respawn="OnRoomReenter"),
        ground_enemy(rid, "anchoring_bias", 730, gallery, 44, 84),
        ground_enemy(rid, "motor_neuron", 1670, floor, 44, 75),
        flier(rid, "brainstorm", 0, 1620, 432, 72, 50),
        # Intrusive Thoughts drift in the nave.
        flier(rid, "intrusive_thought", 0, 1050, 760),
        flier(rid, "intrusive_thought", 1, 1900, 620),
        flier(rid, "intrusive_thought", 2, 500, 420),
        # First impressions: the halo that becomes horns in the eastern nave.
        flier(rid, "halo_horns_effect", 0, 1870, 940, 56, 56),
    ]
    return build(rid, e, "THE NEURAL CATHEDRAL", "neural", dangerous=True)


def weights():
    rid = WEIGHTS
    w, h = ROOMS_AT[rid][1]
    floor = WEIGHTS_FLOOR
    s0, s1 = SPIKES
    d0, d1, deck = DECK
    (west, roof_start), (roof_end, east) = WEIGHTS_SHAFTS
    tunnel_floor = WEIGHTS_TUNNEL_FLOOR
    e = [
        solid("floor_west", 0, floor, west, h - floor),
        solid("training_deck", roof_start, floor, roof_end - roof_start, 16),
        solid("floor_east", east, floor, w - east, h - floor),
        solid("maintenance_floor", west, tunnel_floor, east - west, h - tunnel_floor),
        solid("ceiling", 0, 0, w, 32),
        *side_walls(w, h, floor, None),
        edge("weights_to_callosum", "west, to the Callosum", 0, floor, CALLOSUM, "callosum_to_weights"),
        start(rid, 120, floor),
        resident("npc_neural_perceptron", "neural_perceptron", 420, floor, w=56, h=96),
        sign("weights_sign_percy", 420, floor - 140, "PERCEPTRON, MARK I. ASK IT A YES OR NO.", 420),
        # A bed of spikes, and the two logic gates over it.
        entity("HazardBlock", s0, floor - 16, s1 - s0, 16, name="the training spikes"),
        *[ledge(f"logic_gate_{n}", x0, top, x1 - x0) for n, (x0, x1, top) in enumerate(GATES)],
        sign("weights_sign_and", 1140, 980, "AND", 60),
        sign("weights_sign_or", 1300, 900, "OR", 60),
        # The classifier's board.
        sign("weights_sign_herring", 1730, 556, "RED HERRING (PROBABLE) 99.7%", 360),
        sign("weights_sign_cats", 1730, 846, "PATTERN RECOGNITION: CAT, CAT, CAT, CAT?", 420),
        ground_enemy(rid, "stereotyping", 1730, floor, 86, 74),
        # The racks up to the deck, and the Echo Chamber's door on it.
        *[solid(f"rack_{n}", x0, top, x1 - x0, floor - top) for n, (x0, x1, top) in enumerate(RACKS)],
        ledge("deck", d0, deck, d1 - d0),
        chest("a cached result", "currency:35", 2020, deck),
        door("weights_echo_door", "into the Echo Chamber", 2300, deck, ECHO, "echo_door"),
        sign("weights_sign_echo", 2270, deck - 132, "ECHO CHAMBER", 200),
        # Attention Heads watch from the air.
        flier(rid, "attention_head", 0, 1112, 832, 36, 36),
        flier(rid, "attention_head", 1, 1500, 520, 36, 36),
        flier(rid, "attention_head", 2, 2050, 440, 36, 36),
    ]
    ladders = "\n".join(
        f'        (kind: "Ladder", px: [{x + 16}, {floor - 16}], size: [32, {tunnel_floor - floor + 16}]),'
        for x, _ in WEIGHTS_SHAFTS
    )
    extra = f"\n    intgrid: (climbable: [\n{ladders}\n    ]),"
    return build(rid, e, "THE WEIGHTS", "neural_circuit", dangerous=True, extra=extra)


def echo_chamber():
    rid = ECHO
    w, h = ROOMS_AT[rid][1]
    floor = ECHO_FLOOR
    e = [
        solid("floor", 0, floor, w, h - floor),
        solid("ceiling", 0, 0, w, 32),
        solid("west_wall", 0, 32, WALL, floor - 32),
        solid("east_wall", w - WALL, 32, WALL, floor - 32),
        door("echo_door", "out to the Weights", 64, floor, WEIGHTS, "weights_echo_door"),
        start(rid, 150, floor),
        resident("npc_neural_echo", "neural_echo", 640, floor),
        *[ledge(name, left, top, right - left) for name, left, right, top in ECHO_SEATS],
    ]
    return build(rid, e, "THE ECHO CHAMBER", "neural_circuit")


ROOMS = (callosum, cathedral, weights, echo_chamber)


def main(argv):
    paths = []
    for make in ROOMS:
        rid, text = make()
        path = SPEC_OUT / f"{rid}.ron"
        path.write_text(text)
        print(path)
        paths.append(path)
    if "--apply" not in argv:
        return 0
    if code := ensure_world(WORLD, UID_OFFSET):
        return code
    # A world made from the sandbox's defs has no `dangerous` level field.
    code, out = run("level", "add-field-def", "dangerous", "--type", "Bool", "--default", "false", "--doc",
                    "Out of town: an NPC on the player's side joins the player's fights here (RoomMetadata::dangerous).",
                    str(WORLD), "--in-place")
    if code and "already" not in out:
        return code
    if code := make_rooms(WORLD, paths, keep_position="--relayout" not in argv):
        return code
    code, _ = run("validate", str(WORLD))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
