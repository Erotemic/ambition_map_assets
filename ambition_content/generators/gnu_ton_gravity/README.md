# The GNU-ton gravity handle

The gravity works of the Science dimension (Jon, 2026-10-24: GNU-ton lives
in the Science dimension, with its orbital station): four rooms of gravity
and portal puzzles, and GNU-ton at the end. The world file is
`science.ldtk`, which holds the station's rooms too
(`../orbital_station/`). Walk west from the orchard to the tram spoke
and the station's observation deck. The orchard has the ASCENT gate.
The station has the GALACTIC gate. The rooms use the `orbital_truss` theme: open trusses
under glass, the planet below. The central hub's door `gnu_ton_handle_hub_door`
(main floor, between the Hall of Biomes and the gate stack) leads in, both
ways. The arena's door goes home to it.

`make_specs.py` writes the room specs. Run it from the repository root.
Use `--apply` to update the generated rooms. Edit LDtk-owned rooms in
`science.ldtk`.

## How each room is made

Each puzzle room teaches ONE idea where a mistake costs nothing, tests it
where a mistake costs a short walk, and then turns it with an idea of an
earlier room. The numbers (measured in the game): a jump rises 83 px, a jump
and a double jump 139 px; a run is 270 px/s; the body is 30 x 48. A
`GravityZone` pulls at the normal gravity in its `dir`, and the smaller zone
wins where two overlap. A portal pair opens as long as its shorter end. Two
ends with the same normal turn a body round (it comes out going the other
way along the face).

## The rooms

1. **`gnu_ton_orchard` — here an apple falls up (up fields).**
   - Teach: a column of up field over plain floor. Walk in: you fall onto
     the ceiling. Walk out: you fall back to the floor. A coin is in a nook
     of the ceiling that only a body falling up reaches.
   - Test: a chasm too wide to jump (192 deep, steps out on its near side).
     A column stands over it from bank to bank: walk the ceiling across.
   - Twist: the last column swings from bank to bank (256 each way,
     0.5 rad/s). On the ceiling you stay in it only if you walk with it.
   - Walk across either pit floor to the service ladder on its east
     bank. Use the steps on the west side to go back.
   - Continue east along the floor into the Vector Well.
2. **`gnu_ton_vector_well` — every wall is a floor (side fields).**
   - The bottom passage opens west onto the orchard floor.
   - Teach: the floor of the well pulls right. Walk in, the east wall is
     the floor; walk up it. Over the field you fall back to the floor.
   - Test: a band across the well pulls left. Walk up the east wall into it,
     fall across the well, and walk up the west wall.
   - Twist: at the top of the west wall an up field (room 1) takes you to
     the vault. Walk out of the field to drop into the upper passage.
   - Climb the ladder from the passage to Conservation Hall.
3. **`gnu_ton_conservation_hall` — two places made one (portals).**
   - Climb from the shaft landing to the hall floor. To go down to the
     well, step into the shaft and drop through the landing.
   - Teach: a shelf too tall to jump. A portal in the floor before it has
     its other end on a post on top. Walk in, come out on top.
   - Test: the shelf is closed in by a wall to the vault. The only way on is
     off its edge, into a portal that is the whole floor of the basin. Its
     other end is in the next wall, over a pit with a hazard in it. What falls
     far comes out fast and flies over.
   - Twist: a portal in the hall floor has its other end in the raised
     gallery floor, under a field that pulls up. Fall into the portal and
     go up to the ceiling. Walk out of the field and fall to the floor.
     The east passage connects this floor to the Inversion Gallery.
4. **`gnu_ton_inversion_gallery` — the whole room turns over (switches).**
   - Teach: the lever by the west passage (`SetGravityUp`) turns the room's
     gravity up. The lever above it (`SetGravityDown`) turns gravity down.
   - Test: the floor stops at a chasm with a hazard. The ceiling goes on.
     Turn the room over and walk the ceiling across.
   - Twist: the ceiling has a hole with a hazard in it, too wide to jump. The
     upside-down road steps down to a portal in the ceiling (room 3). Its
     other end is on a wall that hangs from the ceiling past the hole. Past
     that, a field pulls down to the shrine floor. Walk east through the
     passage into the Approach.
5. **`gnu_ton_works_approach` — the climb to GNU-ton, and the way back.**
   From the west passage, walk into the field that lifts the robot to
   the vault. Walk out of the field to drop to the landing. The east
   passage leads from the landing to the arena. The lift near the west
   passage goes down to the end of the station's spoke, by the orchard.
   Its gate in the spoke is let go from
   the lift's side (`spoke_lift_release`): the shortcut back, once the
   gallery is behind you.
6. **`gnu_ton_shoulders` — GNU-ton.** GNU-ton and his giant are on
   the main floor. The west
   passage enters on a ledge. The pad east of the ledge breaks when the
   robot stands on it. His placement is
   `gnu_ton_handle.gnu_ton` (the hall's copy is `hall.gnu_ton`). His reward
   and music are the boss's own. The way out is a door home in an alcove past
   the east wall, behind two `LockWall`s: one stands until his defeat is
   recorded (`boss.cleared gnu_ton_handle.gnu_ton`), the other until GNU2's
   (`boss.cleared gnu_ton_handle.gnu2`).

   **GNU2's cell (2026-11-19, GNUTON-GNU2-FINALE).** The room is LDtk-owned
   (`science.generated.json`), so its cell was authored in the LDtk file and
   `shoulders()` here does not have it. The camera shows the top 1280 px
   of the room. The arena floor is solid from y 1248 to 1344. The cell is
   below it at x 96 to 960 and y 1344 to 2240. GNU2 (`gnu_ton_handle.gnu2`,
   `PhaseScript:gnu2`, `wakes_after` GNU-ton) sleeps near the west wall
   until he enrages. Then GNU2 opens
   a pair of portals, one in the cell's west wall and one in the hall's west
   wall, and walks into the hall (`ambition_content_modules::gnu2`).
   The hall's copy (`gnu_ton_arena`, `sandbox.ldtk`) has the same cell, as
   `hall.gnu2`.

A fall into a hazard starts the room again from its door. The rooms are
made for a robot that runs and jumps. The robot can also fly, blink and
climb walls, and no room can take that away, so only the conservation
hall's shelf and gallery are closed by solid wall.

## Proof

`game/ambition_app/tests/the_gnu_ton_handle.rs` drives the robot through
each room with a player's inputs: the trees of the orchard, the swinging
tree, the four falls of the well, all three portal pairs in the hall, the
gallery levers and crossing, the approach's climb, the lift and its gate in
the spoke, and the route from the hub to the arena and home.
It also checks that GNU-ton is alive, that his punch opens his portals,
and that his recorded defeat opens the way home. The orbital station
tests check the tram route from the orchard to the observation deck
and back.

## Not done

- No switch turns a `GravityZone` or a portal on or off. The levers turn the
  room's ambient gravity only.
- No enemies in the puzzle rooms.
- The hall's GNU-ton arena is not yet a practice room (`practice`), as
  `docs/planning/game/bosses.md` asks for a hall boss that has a main-game
  placement.
