import schedule
import time
import json
from datetime import datetime
from basketball_reference_scraper.seasons import get_schedule, get_standings
import config
import teamAbbreviations
from main import calculate_score

test_time = config.test_time


def getDailyGameSchedule(time):
    #print(get_schedule(2021))
    schedule = get_schedule(2021)
    dailyGames = schedule.loc[schedule['DATE'] == test_time.strftime("%Y-%m-%d")]
    gamesToReturn = [] 
    for index,row in dailyGames.iterrows():
        game = {}
        game["homeTeam"] = teamAbbreviations.teamAbbreviations.get(row["HOME"].upper())
        game["awayTeam"] = teamAbbreviations.teamAbbreviations.get(row["VISITOR"].upper())
        gamesToReturn.append(game)
    return gamesToReturn

def writeToCache():
    print("Starting writeToCache() at ", datetime.now().strftime('%H:%M:%S %Y-%m-%d'))
    scoredSchedule = {}
    scoredSchedule["games"] = []
    scoredSchedule["meta"] = {}
    jsonDataId = 0

    dailyGameSchedule = getDailyGameSchedule("now")
    for game in dailyGameSchedule:
        tempJsonObj = {}
        jsonDataId = jsonDataId + 1
        tempJsonObj["homeTeam"] = game["homeTeam"]
        tempJsonObj["awayTeam"] = game["awayTeam"]
        result = calculate_score(game["homeTeam"], game["awayTeam"], test_time, 2021)
        tempJsonObj["score"] = result
        tempJsonObj["id"] = jsonDataId
        scoredSchedule["games"].append(tempJsonObj)
        print(tempJsonObj)
    print("2", scoredSchedule)

        
    scoredSchedule["meta"]["time"] = time.time()

    with open("scores/cacheGames.json", "w") as outfile:
        json.dump(scoredSchedule, outfile)
    print("Finished at ", datetime.now().strftime('%H:%M:%S %Y-%m-%d'))


def main():
    # schedule.every().day.at("01:26").do(writeToCache)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    print(test_time)
    writeToCache()


if __name__ == "__main__":
    main()