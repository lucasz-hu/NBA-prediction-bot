from basketball_reference_scraper.teams import get_team_stats, get_roster_stats, get_opp_stats

#https://docs.google.com/document/d/1mN4zhW5-i2GAzL56dSfrTR8bSRFEDIXfZZdyJpeQ0lc/edit
#https://www.nbastuffer.com/analytics101/four-factors/
#https://www.basketball-reference.com/about/glossary.html#drb_pct

# schedule = get_schedule(2022)
# filtered = schedule[schedule["VISITOR"]=="Indiana Pacers"]
# stats1 = get_team_stats(
#     'GSW',
#     2011,
#     'PER_GAME'
# )
# print(stats1)

def calculate_efgp(fieldGoal, threePoint, fieldGoalAverage):
    return (fieldGoal + (0.5)*threePoint)/fieldGoalAverage;

def calculate_efgp(offensiveFieldGoal, offensiveThreePoint, offensiveFieldGoalAverage, defensiveFieldGoal, defensiveThreePoint, defensiveFieldGoalAverage):
    return (calculate_efgp_helper(offensiveFieldGoal, offensiveThreePoint, offensiveFieldGoalAverage)-calculate_efgp_helper(defensiveFieldGoal, defensiveThreePoint, defensiveFieldGoalAverage)*100)

def calculate_turnovers():
    return None

def calculate_rebound_helper(rebounds, opponentDefensiveRebounds):
    return (rebounds)/(rebounds+opponentDefensiveRebounds)

def calculate_foul(freeThrowsMade, fieldGoalAttempts):
    return (freeThrowsMade/fieldGoalAttempts)*100

print(calculate_efgp(
    39.6,
    8.4,
    85.9
))
