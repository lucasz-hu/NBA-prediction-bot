import React, { useState, useEffect } from "react";
import DailyScheduleMatchup from "./DailyScheduleMatchup";
import data from "../../scores/cacheGames.json";

const DailySchedule = () => {
    const [dailyGames, setDailyGames] = useState([]);
    const [dailyTime, setDailyTime] = useState([]);

    const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

    useEffect(() => {
        try {
            setDailyGames(data["games"]);
            setDailyTime(new Date(data["meta"].time * 1000));
        } catch {
            console.log("Error with importing json");
        }
    }, []);

    return (
        <div className="font-sans ">
            <h1 className="text-4xl font-bold text-center">
                Daily Predictions:
                {dailyTime.length !== 0
                    ? " " +
                      monthNames[dailyTime.getMonth()] +
                      " " +
                      dailyTime.getDate() +
                      ", " +
                      dailyTime.getFullYear()
                    : void 0}
            </h1>
            <div>
                {dailyGames.map((game) => {
                    return (
                        <div className="p-2">
                            <DailyScheduleMatchup
                                homeTeam={game["homeTeam"]}
                                awayTeam={game["awayTeam"]}
                                score={Math.round(game["score"] * 10) / 10}
                                key={game["id"]}
                            />
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default DailySchedule;
