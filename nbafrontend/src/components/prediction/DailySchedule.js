import React, { useState, useEffect } from "react";
import DailyScheduleMatchup from "./DailyScheduleMatchup";

const DailySchedule = () => {
    const [dailyGames, setDailyGames] = useState([]);

    const currentDate = new Date();
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
        fetch(`http://127.0.0.1:5000/getDailyGames`)
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw response;
            })
            .then((data) => {
                setDailyGames(data);
            });
    }, []);

    return (
        <div className="font-sans ">
            <h1 className="text-4xl font-bold text-center">
                Daily Predictions:
                {" " +
                    monthNames[currentDate.getMonth()] +
                    " " +
                    currentDate.getDate() +
                    ", " +
                    currentDate.getFullYear()}
            </h1>
            <div>
                {dailyGames.map((game) => {
                    return (
                        <div className="p-2">
                            <DailyScheduleMatchup
                                homeTeam={game["homeTeam"]}
                                awayTeam={game["awayTeam"]}
                                score={game["score"]}
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
