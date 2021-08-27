from sportsreference.nba.teams import Teams
from sportsreference.nba.schedule import Schedule

scheduledGames = ['ATL', 'BRK', 'PHI', 'CLE', 'NYK', 'IND', 'LAL', 'WAS', 'MIA', 'NOP', 'SAC', 'DAL', 'TOR', 'DEN']

#todo - import teams using hookdata.io nba API(https://www.hooksdata.io/docs/api/datasources/nbagames/)
#todo continued, use nbaminer to get team dunk stats
#todo continued in the future, getting every team's game and storing it in a db. This way is better so I can go back in x amount of games / dates. https://www.w3schools.com/python/python_mysql_getstarted.asp

def printAllTeams(): #because sportsreference is dumb and sometimes doesn't have the right abbreviations and I can't remember them
    teams = Teams()
    for team in teams:
        print(team.abbreviation + " " + team.name)


def importTeamResult(abbreviation):
    scheduled = Schedule(abbreviation)
    wins = 0
    total = 0
    for game in scheduled:
        if game.result == 'Win':
            wins = wins + 1
            total = total + 1
        elif game.result == 'Loss':
            total = total + 1
    return(wins/total)

def comparePairs(starting):
    global scheduledGames
    team1 = importTeamResult(scheduledGames[starting])
    team2 = importTeamResult(scheduledGames[starting+1])
    if team1 > team2:
        print(scheduledGames[starting] + 'vs' + scheduledGames[starting+1] + ' Place a bet on ' + scheduledGames[starting])
        betCounter += 1
    elif team2 > team1:
        print(scheduledGames[starting] + 'vs' + scheduledGames[starting+1] + ' Place a bet on ' + scheduledGames[starting+1])
        betCounter += 1

def importTeamThreePointPercentage(abbreviation):
    teams = Teams()
    for team in teams:
        if(abbreviation == team.abbreviation):
            return team.three_point_field_goal_percentage

def importTeamThreePPG(abbreviation):
    teams = Teams()
    for team in teams:
        if(abbreviation == team.abbreviation):
            return (team.three_point_field_goals*3)/team.games_played

def importTeamBlocksPG(abbreviation):
    teams = Teams()
    for team in teams:
        if(abbreviation == team.abbreviation):
            return team.blocks/team.games_played

def importOppThreePointPercentage(abbreviation):
    teams = Teams()
    for team in teams:
        if(abbreviation == team.abbreviation):
            return team.opp_three_point_field_goal_percentage/team.games_played

def importOppThreePPG(abbreviation):
    teams = Teams()
    for team in teams:
        if(abbreviation == team.abbreviation):
            return (team.opp_three_point_field_goals*3)/team.games_played

def importOppBlocksPG(abbreviation):
    teams = Teams();
    for team in teams:
        if(abbreviation == team.abbreviation):
            return team.opp_blocks/team.games_played

def startScript(starting):
    global scheduledGames, betCounter
    team1 = [] ##the array
    team2 = []
    teamScoreFinal = []
    count = 0
    team1.extend([importTeamThreePointPercentage(scheduledGames[starting]),
                 importTeamThreePPG(scheduledGames[starting]),
                 importTeamBlocksPG(scheduledGames[starting]),
                 importOppThreePointPercentage(scheduledGames[starting]),
                 importOppThreePPG(scheduledGames[starting]),
                 importOppBlocksPG(scheduledGames[starting])]
                 )
    team2.extend([importTeamThreePointPercentage(scheduledGames[starting+1]),
                 importTeamThreePPG(scheduledGames[starting+1]),
                 importTeamBlocksPG(scheduledGames[starting+1]),
                 importOppThreePointPercentage(scheduledGames[starting+1]),
                 importOppThreePPG(scheduledGames[starting+1]),
                 importOppBlocksPG(scheduledGames[starting+1])]
                 )
    teamScoreFinal.extend([team1[0]-team2[0],
                           team1[1]-team2[1],
                           team1[2]-team2[2],
                           team2[3]-team1[3],
                           team2[4]-team1[4],
                           team2[5]-team1[5]])
    for i in range(len(teamScoreFinal)):
        if(teamScoreFinal[i] > 0):
            count+=1

    if(count >= 4):
        print("Bet on " + scheduledGames[starting] + ". The game is: " + scheduledGames[starting] + " vs " + scheduledGames[starting+1])
    elif(count < 3):
        print("Bet on " + scheduledGames[starting+1] + ". The game is: " + scheduledGames[starting] + " vs " + scheduledGames[starting+1])
    elif(count ==3):
        print("Push, teams are too equal")

def main():
    for i in range(0, len(scheduledGames), 2):
        startScript(i) ##comparePairs (W/L) and threePoint(dunks and threepoints)

main()
