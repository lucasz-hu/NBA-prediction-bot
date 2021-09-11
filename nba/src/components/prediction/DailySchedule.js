import React, { useState, useEffect } from "react";
import DailyScheduleMatchup from "./DailyScheduleMatchup";

const DailySchedule = () => {
    const [dailyGames, setDailyGames] = useState([]);

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
        <>
            {dailyGames.map((game) => {
                return (
                    <DailyScheduleMatchup
                        homeTeam={game["homeTeam"]}
                        awayTeam={game["awayTeam"]}
                        score={game["score"]}
                        key={game["id"]}
                    />
                );
            })}
        </>
    );
};

export default DailySchedule;
