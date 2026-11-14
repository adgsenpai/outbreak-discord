"""Conservative mapping from tracker room names to scenario art. Add verified room names as needed."""
STAGES = {
    'file1': {
        'outbreak': 'Outbreak', 'below_freezing_point': 'Below Freezing Point',
        'the_hive': 'The Hive', 'hellfire': 'Hellfire',
        'decisions_decisions': 'Decisions, Decisions',
    },
    'file2': {
        'wild_things': 'Wild Things', 'underbelly': 'Underbelly',
        'flashback': 'Flashback', 'desperate_times': 'Desperate Times',
        'end_of_the_road': 'End of the Road',
    },
}
# Patterns are intentionally limited to distinctive locations, not generic words.
HINTS = {
 'file1': {
  'outbreak': ('jacks bar', "jack's bar", 'apple inn street'),
  'below_freezing_point': ('freezing room', 'low temperature laboratory', 'b7f laboratory'),
  'the_hive': ('leech man', 'hospital basement'),
  'hellfire': ('apple inn', 'boiler room hotel'),
  'decisions_decisions': ('university hall', 'university entrance'),
 },
 'file2': {
  'wild_things': ('elephant restaurant', 'raccoon zoo', 'elephant stage', 'zoo entrance'),
  'underbelly': ('subway platform', 'subway tunnel', 'south concourse'),
  'flashback': ('abandoned hospital', 'forest path', 'mountain cabin'),
  'desperate_times': ('r.p.d.', 'police station lobby', 'rpd main hall'),
  'end_of_the_road': ('umbrella research facility', 'chemical plant'),
 }
}
# The site's tracker exposes the game's internal scenario number (window.trkLastState.scen).
# This is the most reliable signal; add each id once it has been confirmed in the companion log
# ("scen=N") while playing a known stage.
#
# The value is the scenario's data-archive number (rNNN.afs on the disc). Source: the Resident Evil
# Wiki's "Network Biohazard" scenario table (https://residentevil.fandom.com/wiki/Network_Biohazard),
# which matches both IDs confirmed in-game (28 = The Hive, 41 = Decisions, Decisions).
SCENARIO_IDS = {
    'file1': {
        1: 'outbreak',               # r001
        2: 'hellfire',               # r002 — confirmed in-game 2026-11-15
        28: 'the_hive',              # r028 — confirmed in-game 2026-11-15
        35: 'below_freezing_point',  # r035
        41: 'decisions_decisions',   # r041 — confirmed in-game 2026-11-15
    },
    'file2': {
        10: 'underbelly',            # r010
        15: 'desperate_times',       # r015
        26: 'flashback',             # r026
        40: 'wild_things',           # r040
    },
}
# File #2 has exactly five scenarios. The wiki doesn't list End of the Road's ID, so any other
# in-game scenario number on File #2 is treated as End of the Road (the companion log shows the
# number; pin it in SCENARIO_IDS once seen).
FILE2_REMAINDER = 'end_of_the_road'

def identify(game, location, override=None, scen=None):
    if override and override in STAGES.get(game, {}):
        return override
    if scen is not None:
        if scen in SCENARIO_IDS.get(game, {}):
            return SCENARIO_IDS[game][scen]
        if game == 'file2' and scen > 0:
            return FILE2_REMAINDER
    loc = (location or '').casefold()
    matches = [key for key, hints in HINTS.get(game, {}).items() if any(h in loc for h in hints)]
    return matches[0] if len(matches) == 1 else None
