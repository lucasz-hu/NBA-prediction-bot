from basketball_reference_scraper.teams import get_team_stats, get_opp_stats
from basketball_reference_scraper.seasons import get_schedule
from basketball_reference_scraper.box_scores import get_box_scores
from flask import Flask, request
from flask_cors import CORS
import json
from datetime import datetime as dt
import pandas as pd
import teamAbbreviations
import config

app = Flask(__name__)
CORS(app)

test_time = config.test_time
test_time_datetime = config.test_time_datetime

#https://docs.google.com/document/d/1mN4zhW5-i2GAzL56dSfrTR8bSRFEDIXfZZdyJpeQ0lc/edit
#https://www.nbastuffer.com/analytics101/four-factors/
#https://www.basketball-reference.com/about/glossary.html#drb_pct

#todo, implement momentum and value
#also, change homeOffenses.py get_homeOffense_stats and get_opp_stats to not have to fetch data every time. Currently, it fetches data, then filters out to approriate homeOffense.
#rather, have it fetch data and return raw data.

def calculate_efgp_helper(fieldGoal, threePoint, fieldGoalAttempts):
    return (fieldGoal + (0.5)*threePoint)/fieldGoalAttempts;

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

def calculate_score(homeInitials, awayInitials, time=dt.now() ,year=config.season):
    homeFullName = (list(teamAbbreviations.teamAbbreviations.keys())[list(teamAbbreviations.teamAbbreviations.values()).index(homeInitials)])
    awayFullName = (list(teamAbbreviations.teamAbbreviations.keys())[list(teamAbbreviations.teamAbbreviations.values()).index(awayInitials)])
    
    homeOffenseStats = get_team_stats(
        homeInitials,
        year,
        'PER_GAME'
    ) 
    homeOppStats = get_opp_stats(
        homeInitials,
        year,
        'PER_GAME'
    )

    awayOffenseStats = get_team_stats(
        awayInitials,
        year,
        'PER_GAME'
    )
    awayOppStats = get_opp_stats(
        awayInitials,
        year,
        'PER_GAME'
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
    homeDefenseFreeThrowsMade = homeOppStats["OPP_FT"]

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
    awayDefenseFreeThrowsMade = awayOppStats["OPP_FT"]

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

    homefoul = calculate_foul(homeOffenseFreeThrowsMade, homeOffenseFieldGoalAttempts, homeDefenseFreeThrowsMade, homeDefenseFieldGoalAttempts) * 100

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

    awayfoul = calculate_foul(awayOffenseFreeThrowsMade, awayOffenseFieldGoalAttempts, awayDefenseFreeThrowsMade, awayDefenseFieldGoalAttempts) * 100

    homeMomentumStats = team_momentum_stats(homeInitials, time=test_time_datetime)
    awayMomentumStats = team_momentum_stats(awayInitials, time=test_time_datetime)
    print("homeOffenseFieldGoal", homeOffenseFieldGoal)
    print("homeOffenseThreePoint", homeOffenseThreePoint)
    print("homeOffenseFieldGoalAttempts", homeOffenseFieldGoalAttempts )
    print("homeOffenseTurnOvers", homeOffenseTurnOvers )
    print("homeOffenseFreeThrowAttempts", homeOffenseFreeThrowAttempts )
    print("homeOffenseOffensiveRebounds", homeOffenseOffensiveRebounds )
    print("homeOffenseDefensiveRebounds", homeOffenseDefensiveRebounds )
    print("homeOffenseFreeThrowsMade", homeOffenseFreeThrowsMade)
    print("homeDefenseFieldGoal", homeDefenseFieldGoal)
    print("homeDefenseThreePoint", homeDefenseThreePoint)
    print("homeDefenseFieldGoalAttempts", homeDefenseFieldGoalAttempts )
    print("homeDefenseTurnOvers", homeDefenseTurnOvers )
    print("homeDefenseFreeThrowAttempts", homeDefenseFreeThrowAttempts )
    print("homeDefenseOffensiveRebounds", homeDefenseOffensiveRebounds )
    print("homeDefenseDefensiveRebounds", homeDefenseDefensiveRebounds )
    print("homeDefenseDefensiveRebounds", homeDefenseDefensiveRebounds )
    print("homeDefenseFreeThrowsMade", homeDefenseFreeThrowsMade)
    print("Homehomentumstats", homeMomentumStats)
    print("awayMomentumStats", awayMomentumStats)

    homeMomentumEfgp = calculate_efgp(
        homeMomentumStats["teamOffenseFieldGoal"], 
        homeMomentumStats["teamOffenseThreePoint"], 
        homeMomentumStats["teamOffenseFieldGoalAttempts"],
        homeMomentumStats["teamDefenseFieldGoal"],
        homeMomentumStats["teamDefenseThreePoint"],
        homeMomentumStats["teamDefenseFieldGoalAttempts"]
    ) * 100
    homeMomentumTov = calculate_turnovers(
        homeMomentumStats["teamOffenseTurnOvers"],
        homeMomentumStats["teamOffenseFieldGoalAttempts"],
        homeMomentumStats["teamOffenseFreeThrowAttempts"],
        homeMomentumStats["teamDefenseTurnOvers"],
        homeMomentumStats["teamDefenseFieldGoalAttempts"],
        homeMomentumStats["teamDefenseFreeThrowAttempts"]
    ) * 100
    homeMomentumRebound = calculate_rebound(
        homeMomentumStats["teamOffenseOffensiveRebounds"],
        homeMomentumStats["teamDefenseDefensiveRebounds"],
        homeMomentumStats["teamOffenseDefensiveRebounds"],
        homeMomentumStats["teamDefenseOffensiveRebounds"]
    ) * 100
    homeMomentumFoul = calculate_foul(
        homeMomentumStats["teamOffenseFreeThrowsMade"],
        homeMomentumStats["teamOffenseFieldGoalAttempts"],
        homeMomentumStats["teamDefenseFreeThrowsMade"],
        homeMomentumStats["teamDefenseFieldGoalAttempts"]
    ) * 100

    awayMomentumEfgp = calculate_efgp(
        awayMomentumStats["teamOffenseFieldGoal"], 
        awayMomentumStats["teamOffenseThreePoint"], 
        awayMomentumStats["teamOffenseFieldGoalAttempts"],
        awayMomentumStats["teamDefenseFieldGoal"],
        awayMomentumStats["teamDefenseThreePoint"],
        awayMomentumStats["teamDefenseFieldGoalAttempts"]
    ) * 100
    awayMomentumTov = calculate_turnovers(
        awayMomentumStats["teamOffenseTurnOvers"],
        awayMomentumStats["teamOffenseFieldGoalAttempts"],
        awayMomentumStats["teamOffenseFreeThrowAttempts"],
        awayMomentumStats["teamDefenseTurnOvers"],
        awayMomentumStats["teamDefenseFieldGoalAttempts"],
        awayMomentumStats["teamDefenseFreeThrowAttempts"]
    )* 100
    awayMomentumRebound = calculate_rebound(
        awayMomentumStats["teamOffenseOffensiveRebounds"],
        awayMomentumStats["teamDefenseDefensiveRebounds"],
        awayMomentumStats["teamOffenseDefensiveRebounds"],
        awayMomentumStats["teamDefenseOffensiveRebounds"]
    )* 100
    awayMomentumFoul = calculate_foul(
        awayMomentumStats["teamOffenseFreeThrowsMade"],
        awayMomentumStats["teamOffenseFieldGoalAttempts"],
        awayMomentumStats["teamDefenseFreeThrowsMade"],
        awayMomentumStats["teamDefenseFieldGoalAttempts"]
    ) * 100

    hometotal = (0.4 * homeefgp) + (0.25 * hometov) + (0.2 * homerebound) + (0.15 * homefoul)
    awaytotal = (0.4 * awayefgp) + (0.25 * awaytov) + (0.2 * awayrebound) + (0.15 * awayfoul)

    homeMomentumTotal = (0.4*homeMomentumEfgp) + (0.25 * homeMomentumTov) + (0.2 * homeMomentumRebound) + (0.15 * homeMomentumFoul)
    awayMomentumTotal = (0.4*awayMomentumEfgp) + (0.25 * awayMomentumTov) + (0.2 * awayMomentumRebound) + (0.15 * awayMomentumFoul)

    total = (((hometotal+homeMomentumTotal))-((awaytotal+awayMomentumTotal)))
    return total

def team_momentum_stats(team, amountOfPreviousGames=5, time=dt.now()):
    #team in full name
    stats = get_last(team, amountOfPreviousGames, time)
    newStats = {key: stats[key] // amountOfPreviousGames for key in stats.keys()}
    return newStats

def get_last(team, amountOfPreviousGames, time=dt.now()):
    data = get_last_x_games(team, amountOfPreviousGames, time)
    return get_last_x_stats(data, team)

def get_last_x_games(team, amountOfPreviousGames, time=dt.now()):
    #Gets schedule for team with amountOfGames
    teamFullName = (list(teamAbbreviations.teamAbbreviations.keys())[list(teamAbbreviations.teamAbbreviations.values()).index(team)]).title()
    if teamFullName == "Philadelphia 76Ers":
        teamFullName = "Philadelphia 76ers"
    schedule = get_schedule(config.season)
    schedule["DATE"] = pd.to_datetime(schedule["DATE"])
    today = time # dt.now()
    schedule = schedule.loc[(schedule["DATE"] < today) & ((schedule["HOME"] == teamFullName) | (schedule["VISITOR"] == teamFullName))]
    return schedule.tail(amountOfPreviousGames)

def get_last_x_stats(previousGameData, team):
    #Gets stats based on get_last_x_games schedule. Returns a dict
    teamStats = {
        "teamOffenseFieldGoal" : 0,
        "teamOffenseThreePoint" : 0,
        "teamOffenseFieldGoalAttempts" : 0,
        "teamOffenseTurnOvers" : 0,
        "teamOffenseFreeThrowAttempts" : 0,
        "teamOffenseOffensiveRebounds" : 0,
        "teamOffenseDefensiveRebounds" : 0,
        "teamOffenseFreeThrowsMade" : 0,
        "teamDefenseFieldGoal" : 0,
        "teamDefenseThreePoint" : 0,
        "teamDefenseFieldGoalAttempts" : 0,
        "teamDefenseTurnOvers" : 0,
        "teamDefenseFreeThrowAttempts" : 0,
        "teamDefenseOffensiveRebounds" : 0,
        "teamDefenseDefensiveRebounds" : 0,
        "teamDefenseFreeThrowsMade" : 0
    }
    for index, row in previousGameData.iterrows():
        homeAbbreviation = teamAbbreviations.teamAbbreviations[row["HOME"].upper()]
        awayAbbreviation = teamAbbreviations.teamAbbreviations[row["VISITOR"].upper()]
        homeFullName = (list(teamAbbreviations.teamAbbreviations.keys())[list(teamAbbreviations.teamAbbreviations.values()).index(team)]).title()
        if homeFullName == "Philadelphia 76Ers":
            homeFullName = "Philadelphia 76ers"
        game = get_box_scores(row["DATE"], homeAbbreviation, awayAbbreviation)
        if row["HOME"] == homeFullName:
            teamStats["teamOffenseFieldGoal"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FG"])
            teamStats["teamOffenseThreePoint"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["3P"])
            teamStats["teamOffenseFieldGoalAttempts"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FGA"])
            teamStats["teamOffenseTurnOvers"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["TOV"])
            teamStats["teamOffenseFreeThrowAttempts"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FTA"])
            teamStats["teamOffenseOffensiveRebounds"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["ORB"])
            teamStats["teamOffenseDefensiveRebounds"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["DRB"])
            teamStats["teamOffenseFreeThrowsMade"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FT"])

            teamStats["teamDefenseFieldGoal"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FG"])
            teamStats["teamDefenseThreePoint"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["3P"])
            teamStats["teamDefenseFieldGoalAttempts"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FGA"])
            teamStats["teamDefenseTurnOvers"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["TOV"])
            teamStats["teamDefenseFreeThrowAttempts"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FTA"])
            teamStats["teamDefenseOffensiveRebounds"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["ORB"])
            teamStats["teamDefenseDefensiveRebounds"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["DRB"])
            teamStats["teamDefenseFreeThrowsMade"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FT"])
        elif row["VISITOR"] == homeFullName:
            teamStats["teamOffenseFieldGoal"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FG"])
            teamStats["teamOffenseThreePoint"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["3P"])
            teamStats["teamOffenseFieldGoalAttempts"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FGA"])
            teamStats["teamOffenseTurnOvers"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["TOV"])
            teamStats["teamOffenseFreeThrowAttempts"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FTA"])
            teamStats["teamOffenseOffensiveRebounds"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["ORB"])
            teamStats["teamOffenseDefensiveRebounds"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["DRB"])
            teamStats["teamOffenseFreeThrowsMade"] += int(game[awayAbbreviation].loc[game[awayAbbreviation]["PLAYER"] == "Team Totals"]["FT"])

            teamStats["teamDefenseFieldGoal"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FG"])
            teamStats["teamDefenseThreePoint"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["3P"])
            teamStats["teamDefenseFieldGoalAttempts"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FGA"])
            teamStats["teamDefenseTurnOvers"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["TOV"])
            teamStats["teamDefenseFreeThrowAttempts"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FTA"])
            teamStats["teamDefenseOffensiveRebounds"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["ORB"])
            teamStats["teamDefenseDefensiveRebounds"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["DRB"])
            teamStats["teamDefenseFreeThrowsMade"] += int(game[homeAbbreviation].loc[game[homeAbbreviation]["PLAYER"] == "Team Totals"]["FT"])
    return teamStats

@app.route("/prediction/")
def prediction():
    try:
        homeTeam=request.args.get("homeTeam")
        awayTeam=request.args.get("awayTeam")
        score = calculate_score(homeTeam, awayTeam)
        score = round(score, 1)
        return {'score': score}
    except Exception as e:
        print(f"Error in prediction(): {e}")
        return {}
    
@app.route("/getDailyGames/")
def getDailyGames():
    try:
        with open("scores/cacheGames.json", "r") as scoreJson:
            scores = json.load(scoreJson)
            return scores
    except Exception as e:
        print(f"Error in getDailyGames(): {e}")
        return {}

def main():
    calculate_score("PHO", "MIL")
    #get_last("Milwaukee Bucks", 5)
    # print("Welcome to my four factors NBA prediction model")
    # homeTeam = input("To start, who is the home team? (In initials): ")
    # awayTeam = input("And who is away? (Also in initials): ")
    # year = input("And did you want this match played in a historical specific year? (Input year, if not then just leave blank and press enter): ")
    # if(year==""):
    #     score = calculate_score(homeTeam, awayTeam) 
    # else:
    #     score = calculate_score(homeTeam, awayTeam, int(year)) 
    # score = round(score, 1)


if __name__ == "__main__":
    main()