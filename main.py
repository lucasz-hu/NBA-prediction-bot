from basketball_reference_scraper.teams import get_team_stats, get_opp_stats
from basketball_reference_scraper.seasons import get_schedule
from basketball_reference_scraper.box_scores import get_box_scores
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#https://docs.google.com/document/d/1mN4zhW5-i2GAzL56dSfrTR8bSRFEDIXfZZdyJpeQ0lc/edit
#https://www.nbastuffer.com/analytics101/four-factors/
#https://www.basketball-reference.com/about/glossary.html#drb_pct

#todo, implement momentum and value
#also, change homeOffenses.py get_homeOffense_stats and get_opp_stats to not have to fetch data every time. Currently, it fetches data, then filters out to approriate homeOffense.
#rather, have it fetch data and return raw data.

def calculate_efgp_helper(fieldGoal, threePoint, fieldGoalAverage):
    return (fieldGoal + (0.5)*threePoint)/fieldGoalAverage;

def calculate_efgp(offensiveFieldGoal, offensiveThreePoint, offensiveFieldGoalAverage, defensiveFieldGoal, defensiveThreePoint, defensiveFieldGoalAverage):
    return (calculate_efgp_helper(offensiveFieldGoal, offensiveThreePoint, offensiveFieldGoalAverage)-calculate_efgp_helper(defensiveFieldGoal, defensiveThreePoint, defensiveFieldGoalAverage))

def calculate_turnovers(offensiveTurnovers, offensiveFieldGoalAttempts, offensiveFreeThrowAttempts, defensiveTurnovers, defensiveFieldGoalAttempts, defensiveFreeThrowAttempts):
    return calculate_turnovers_helper(offensiveTurnovers, offensiveFieldGoalAttempts, offensiveFreeThrowAttempts)-calculate_turnovers_helper(defensiveTurnovers, defensiveFieldGoalAttempts, defensiveFreeThrowAttempts)

def calculate_turnovers_helper(turnovers, fieldGoalAttempts, freeThrowAttempts):
    return (turnovers)/(fieldGoalAttempts+(0.44*freeThrowAttempts)+turnovers)

def calculate_rebound(offensiveRebounds, opponentDefensiveRebounds, defensiveRebounds, opponentOffensiveRebounds):
    return calculate_rebound_helper(offensiveRebounds, opponentDefensiveRebounds)-calculate_rebound_helper(defensiveRebounds, opponentOffensiveRebounds)

def calculate_rebound_helper(rebounds, opponentDefensiveRebounds):
    return (rebounds)/(rebounds+opponentDefensiveRebounds)

def calculate_foul_helper(freeThrowsMade, fieldGoalAttempts):
    return (freeThrowsMade/fieldGoalAttempts)

def calculate_foul(homeFreeThrowsMade, homeFieldGoalAttempts, awayFreeThrowsmade, awayFieldGoalAttempts):
    return calculate_foul_helper(homeFreeThrowsMade, homeFieldGoalAttempts)-calculate_foul_helper(awayFreeThrowsmade, awayFieldGoalAttempts)

def calculate_score(homeInitials, awayInitials, year=2021):
    homeOffenseStats = get_team_stats(
        homeInitials,
        year,
        'TOTAL'
    ) 
    homeOppStats = get_opp_stats(
        homeInitials,
        year,
        'TOTAL'
    )

    awayOffenseStats = get_team_stats(
        awayInitials,
        year,
        'TOTAL'
    )
    awayOppStats = get_opp_stats(
        awayInitials,
        year,
        'TOTAL'
    )

    homeOffenseFieldGoal = homeOffenseStats["FG"]
    homeOffenseThreePoint = homeOffenseStats["3P"]
    homeOffenseFieldGoalAttempts = homeOffenseStats["FGA"]
    homeOffenseTurnOvers = homeOffenseStats["TOV"]
    homeOffenseFreeThrowAttempts = homeOffenseStats["FTA"]
    homeOffenseOffensiveRebounds = homeOffenseStats["ORB"]
    homeOffenseDefensiveRebounds = homeOffenseStats["DRB"]
    homeOffenseFreeThrowsMade = homeOffenseStats["FT"]

    homeDefenseFieldGoal=homeOppStats["OPP_FG"]
    homeDefenseThreePoint = homeOppStats["OPP_3P"]
    homeDefenseFieldGoalAttempts = homeOppStats["OPP_FGA"]
    homeDefenseTurnOvers = homeOppStats["OPP_TOV"]
    homeDefenseFreeThrowAttempts = homeOppStats["OPP_FTA"]
    homeDefenseOffensiveRebounds = homeOppStats["OPP_ORB"]
    homeDefenseDefensiveRebounds = homeOppStats["OPP_DRB"]
    homeDefenseDefensiveRebounds = homeOppStats["OPP_DRB"]
    homeDefenseFreeThrowsmade = homeOppStats["OPP_FT"]

    awayOffenseFieldGoal = awayOffenseStats["FG"]
    awayOffenseThreePoint = awayOffenseStats["3P"]
    awayOffenseFieldGoalAttempts = awayOffenseStats["FGA"]
    awayOffenseTurnOvers = awayOffenseStats["TOV"]
    awayOffenseFreeThrowAttempts = awayOffenseStats["FTA"]
    awayOffenseOffensiveRebounds = awayOffenseStats["ORB"]
    awayOffenseDefensiveRebounds = awayOffenseStats["DRB"]
    awayOffenseFreeThrowsMade = awayOffenseStats["FT"]

    awayDefenseFieldGoal= awayOppStats["OPP_FG"]
    awayDefenseThreePoint = awayOppStats["OPP_3P"]
    awayDefenseFieldGoalAttempts = awayOppStats["OPP_FGA"]
    awayDefenseTurnOvers = awayOppStats["OPP_TOV"]
    awayDefenseFreeThrowAttempts = awayOppStats["OPP_FTA"]
    awayDefenseOffensiveRebounds = awayOppStats["OPP_ORB"]
    awayDefenseDefensiveRebounds = awayOppStats["OPP_DRB"]
    awayDefenseDefensiveRebounds = awayOppStats["OPP_DRB"]
    awayDefenseFreeThrowsmade = awayOppStats["OPP_FT"]

    homeefgp = calculate_efgp(
        homeOffenseFieldGoal,
        homeOffenseThreePoint,
        homeOffenseFieldGoalAttempts,
        homeDefenseFieldGoal,
        homeDefenseThreePoint,
        homeDefenseFieldGoalAttempts
    )* 100

    hometov = calculate_turnovers(
        homeOffenseTurnOvers,
        homeOffenseFieldGoalAttempts,
        homeOffenseFreeThrowAttempts,
        homeDefenseTurnOvers,
        homeDefenseFieldGoalAttempts,
        homeDefenseFreeThrowAttempts
    ) * 100

    homerebound = calculate_rebound(
        homeOffenseOffensiveRebounds,
        homeDefenseDefensiveRebounds,
        homeOffenseDefensiveRebounds,
        homeDefenseOffensiveRebounds
    ) * 100

    homefoul = calculate_foul(homeOffenseFreeThrowsMade, homeOffenseFieldGoalAttempts, homeDefenseFreeThrowsmade, homeDefenseFieldGoalAttempts) * 100

    awayefgp = calculate_efgp(
        awayOffenseFieldGoal,
        awayOffenseThreePoint,
        awayOffenseFieldGoalAttempts,
        awayDefenseFieldGoal,
        awayDefenseThreePoint,
        awayDefenseFieldGoalAttempts
    ) * 100

    awaytov = calculate_turnovers(
        awayOffenseTurnOvers,
        awayOffenseFieldGoalAttempts,
        awayOffenseFreeThrowAttempts,
        awayDefenseTurnOvers,
        awayDefenseFieldGoalAttempts,
        awayDefenseFreeThrowAttempts
    ) * 100

    awayrebound= calculate_rebound(
        awayOffenseOffensiveRebounds,
        awayDefenseDefensiveRebounds,
        awayOffenseDefensiveRebounds,
        awayDefenseOffensiveRebounds
    ) * 100

    awayfoul = calculate_foul(awayOffenseFreeThrowsMade, awayOffenseFieldGoalAttempts, awayDefenseFreeThrowsmade, awayDefenseFieldGoalAttempts) * 100

    hometotal = (0.4 * homeefgp) + (0.25 * hometov) + (0.2 * homerebound) + (0.15 * homefoul)
    awaytotal = (0.4 * awayefgp) + (0.25 * awaytov) + (0.2 * awayrebound) + (0.15 * awayfoul)

    total = (hometotal-awaytotal)*2

    return total

@app.route("/prediction/")
def hello_world():
    try:
        homeTeam=request.args.get("homeTeam")
        awayTeam=request.args.get("awayTeam")
        score = calculate_score(homeTeam, awayTeam)
        score = round(score, 1)
        return {'score': score}
    except:
        return {}
    
    

def main():
    print("Welcome to my four factors NBA prediction model")
    homeTeam = input("To start, who is the home team? (In initials): ")
    awayTeam = input("And who is away? (Also in initials): ")
    year = input("And did you want this match played in a historical specific year? (Input year, if not then just leave blank and press enter): ")
    if(year==""):
        score = calculate_score(homeTeam, awayTeam) 
    else:
        score = calculate_score(homeTeam, awayTeam, int(year)) 
    score = round(score, 1)


if __name__ == "__main__":
    main()