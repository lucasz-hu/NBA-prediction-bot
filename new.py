from basketball_reference_scraper.teams import get_team_stats, get_roster_stats, get_opp_stats

#https://docs.google.com/document/d/1mN4zhW5-i2GAzL56dSfrTR8bSRFEDIXfZZdyJpeQ0lc/edit
#https://www.nbastuffer.com/analytics101/four-factors/
#https://www.basketball-reference.com/about/glossary.html#drb_pct

#todo, implement momentum and value
#also, change teams.py get_team_stats and get_opp_stats to not have to fetch data every time. Currently, it fetches data, then filters out to approriate team.
#rather, have it fetch data and return raw data.

# schedule = get_schedule(2022)
# filtered = schedule[schedule["VISITOR"]=="Indiana Pacers"]
team = get_team_stats(
    'PHO',
    2005,
    'TOTAL'
)
opp = get_opp_stats(
    'PHO',
    2005,
    'TOTAL'
)
print(team)
print(opp)

teamFieldGoal = team["FG"]
teamThreePoint = team["3P"]
teamFieldGoalAttempts = team["FGA"]
teamTurnOvers = team["TOV"]
teamFreeThrowAttempts = team["FTA"]
teamRebounds = team["ORB"]
teamFreeThrowsMade = team["FT"]

oppFieldGoal=opp["OPP_FG"]
oppThreePoint = opp["OPP_3P"]
oppFieldGoalAttempts = opp["OPP_FGA"]
oppTurnOvers = opp["OPP_TOV"]
oppFreeThrowAttempts = opp["OPP_FTA"]
oppDefensiveRebounds = opp["OPP_DRB"]

def calculate_efgp_helper(fieldGoal, threePoint, fieldGoalAverage):
    return (fieldGoal + (0.5)*threePoint)/fieldGoalAverage;

def calculate_efgp(offensiveFieldGoal, offensiveThreePoint, offensiveFieldGoalAverage, defensiveFieldGoal, defensiveThreePoint, defensiveFieldGoalAverage):
    return (calculate_efgp_helper(offensiveFieldGoal, offensiveThreePoint, offensiveFieldGoalAverage)-calculate_efgp_helper(defensiveFieldGoal, defensiveThreePoint, defensiveFieldGoalAverage))

def calculate_turnovers(offensiveTurnovers, offensiveFieldGoalAttempts, offensiveFreeThrowAttempts, defensiveTurnovers, defensiveFieldGoalAttempts, defensiveFreeThrowAttempts):
    return calculate_turnovers_helper(defensiveTurnovers, defensiveFieldGoalAttempts, defensiveFreeThrowAttempts)-calculate_turnovers_helper(offensiveTurnovers, offensiveFieldGoalAttempts, offensiveFreeThrowAttempts)

def calculate_turnovers_helper(turnovers, fieldGoalAttempts, freeThrowAttempts):
    return (100*turnovers)/(fieldGoalAttempts+(0.44*freeThrowAttempts)+turnovers)

def calculate_rebound(rebounds, opponentDefensiveRebounds):
    return (rebounds)/(rebounds+opponentDefensiveRebounds)

def calculate_foul(freeThrowsMade, fieldGoalAttempts):
    return (freeThrowsMade/fieldGoalAttempts)

print("efgp: " + str(calculate_efgp(
    teamFieldGoal,
    teamThreePoint,
    teamFieldGoalAttempts,
    oppFieldGoal,
    oppThreePoint,
    oppFieldGoalAttempts
)))

print("TOV: " + str(calculate_turnovers(
    teamTurnOvers,
    teamFieldGoalAttempts,
    teamFreeThrowAttempts,
    oppTurnOvers,
    oppFieldGoalAttempts,
    oppFreeThrowAttempts
)))

print("rebound: " + str(calculate_rebound(
    teamRebounds,
    oppDefensiveRebounds
)))

print("Foul: " + str(calculate_foul(teamFreeThrowsMade, teamFieldGoalAttempts)))