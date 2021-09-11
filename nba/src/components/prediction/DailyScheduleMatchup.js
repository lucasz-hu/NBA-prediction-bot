import React from "react";

const DailyScheduleMatchup = ({ homeTeam, awayTeam, score }) => {
    return (
        <div>
            <h1>
                {homeTeam} vs {awayTeam}
            </h1>
            <h2>{score}</h2>
        </div>
    );
};

export default DailyScheduleMatchup;
