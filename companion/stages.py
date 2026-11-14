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
SCENARIO_IDS = {
    'file1': {
        28: 'the_hive',  # confirmed 2026-11-15 in-game
    },
    'file2': {},
}

def identify(game, location, override=None, scen=None):
    if override and override in STAGES.get(game, {}):
        return override
    if scen is not None and scen in SCENARIO_IDS.get(game, {}):
        return SCENARIO_IDS[game][scen]
    loc = (location or '').casefold()
    matches = [key for key, hints in HINTS.get(game, {}).items() if any(h in loc for h in hints)]
    return matches[0] if len(matches) == 1 else None
