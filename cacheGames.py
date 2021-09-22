import schedule
import time
import json
from datetime import datetime
from basketball_reference_scraper.seasons import get_schedule, get_standings
import config
import teamAbbreviations
from main import calculate_score

def getDailyGameSchedule(time):
    #print(get_schedule(2021))
    schedule = get_schedule(2021)
    dailyGames = schedule.loc[schedule['DATE'] == datetime.fromtimestamp(1620454400).strftime("%Y-%m-%d")]
    gamesToReturn = [] 
    for index,row in dailyGames.iterrows():
        game = {}
        game["homeTeam"] = teamAbbreviations.teamAbbreviations.get(row["HOME"].upper())
        game["awayTeam"] = teamAbbreviations.teamAbbreviations.get(row["VISITOR"].upper())
        gamesToReturn.append(game)
    return gamesToReturn

def writeToCache():
    jsonData = {}
    jsonData["games"] = {}
    jsonData["meta"] = {}
    jsonDataId = 0

    dailyGameSchedule = getDailyGameSchedule("now")
    scoredSchedule = []
    for game in dailyGameSchedule:
        jsonDataId = jsonDataId + 1
        jsonData["games"][jsonDataId] = game
        result = calculate_score(game["homeTeam"], game["awayTeam"], datetime.fromtimestamp(1620454400))
        jsonData["games"][jsonDataId]["score"] = result
        print(result)

        
    jsonData["meta"]["time"] = time.time()

    with open("cacheGames.json", "w") as outfile:
        json.dump(jsonData, outfile)


def main():
    writeToCache()
    #print(get_schedule(2021).to_string())
    # schedule.every().day.at("20:54").do(printHere)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()