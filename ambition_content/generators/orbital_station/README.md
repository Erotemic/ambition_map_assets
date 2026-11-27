# Orbital station

Edit the station in `ambition_content/worlds/science.ldtk`. The tether
terminus also connects to the Eureka elevator.

```text
Damaged spur ─ Service ─ Habitation ─ Observation ─ Tram spoke ─ Orchard
                             │             │
                          Gate dock ─ Docking bay ─ Tether terminus
```

Walk through side loading zones between adjacent rooms. The ladder
shafts join the gate dock to habitation and the docking bay to the
observation deck. The orchard walk crosses above the express lift at
the east end of the tram spoke.

The gate dock holds the GALACTIC ring and the customs desk. The docking
bay holds the hauler and shuttle. The observation deck has a window
and a raised walk. The habitation ring has the galley, bunks, and grow
deck. The service deck has a plant and two maintenance walks. The
damaged spur has three cable pits, a breaker, and a cache.

## Consignment 0447

Officer Okafor holds the consignment until Georg Canter signs the
manifest. When Okafor clears it, `orbital_consignment_cleared` opens the
freight lane and `orbital_spur_pass` opens the west hatch in the service
deck. The errand ends at the hub. The spur's breaker sets
`switch_orbital_spur_breaker_used`.

## Checks

In the main repository, run the `the_orbital_station`,
`the_consignment_errand`, and `the_gnu_ton_handle` filters in the
`ambition_app` integration test target. Run
`tools/ambition_ldtk_tools/specs/check_flat_map.py science.ldtk` to check
the positions of the loading zones.
