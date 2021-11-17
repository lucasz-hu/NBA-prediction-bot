import json
from datetime import datetime
from basketball_reference_scraper.seasons import get_schedule, get_standings
import config
import teamAbbreviations
from main import calculate_score
import logging

now = datetime.now()

timestamp = datetime.timestamp(now)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename=f'logs/{timestamp}.log')
logging.info("Testing")
logger = logging.getLogger("nba")

test_time = config.test_time
test_time_datetime = config.test_time_datetime


def getDailyGameSchedule(time):
    #print(get_schedule(2021))
    schedule = get_schedule(config.season)
    dailyGames = schedule.loc[schedule['DATE'] == test_time_datetime.strftime("%Y-%m-%d")]
    gamesToReturn = [] 
    for index,row in dailyGames.iterrows():
        game = {}
        game["homeTeam"] = teamAbbreviations.teamAbbreviations.get(row["HOME"].upper())
        game["awayTeam"] = teamAbbreviations.teamAbbreviations.get(row["VISITOR"].upper())
        gamesToReturn.append(game)
    return gamesToReturn

def writeToCache():
    print("Starting writeToCache() at ", datetime.now().strftime('%H:%M:%S %Y-%m-%d'))
    logger.info("Starting writeToCache() at ", datetime.now().strftime('%H:%M:%S %Y-%m-%d'))
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
        result = calculate_score(game["homeTeam"], game["awayTeam"], test_time_datetime, 2021)
        tempJsonObj["score"] = result
        tempJsonObj["id"] = jsonDataId
        scoredSchedule["games"].append(tempJsonObj)
        logger.info(f'tempJsonObj - {tempJsonObj}')
        print(tempJsonObj)
    logger.info(f'scoredSchedule - {scoredSchedule}')
    print(scoredSchedule)

        
    scoredSchedule["meta"]["time"] = str(test_time)

    with open("nbafrontend/src/scores/cacheGames.json", "w") as outfile:
        json.dump(scoredSchedule, outfile)
    finished = "Finished at ", datetime.now().strftime('%H:%M:%S %Y-%m-%d')
    logger.info(f'finished - {finished}')
    print(finished)


def main():
    # schedule.every().day.at("01:26").do(writeToCache)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    print(test_time_datetime)
    writeToCache()


if __name__ == "__main__":
    main()