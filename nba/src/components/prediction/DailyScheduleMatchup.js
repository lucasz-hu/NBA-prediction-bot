import React from "react";
import "../../index.js";
import DailyScheduleMatchupTeam from "./DailyScheduleMatchupTeam.js";

const DailyScheduleMatchup = ({ homeTeam, awayTeam, score }) => {
    return (
        <div className="box-border border-4 m-4 p-2 rounded-md bg-purple-100 border-gray-700 shadow-xl">
            <div className="place-items-center m-auto flex justify-center ">
                <DailyScheduleMatchupTeam teamName={homeTeam} />
                <h1 className="md:mx-48 mx-10 text-2xl">vs</h1>
                <DailyScheduleMatchupTeam teamName={awayTeam} />
            </div>
            <h2 className="flex justify-center text-4xl font-bold">{score}</h2>
        </div>
    );
};

export default DailyScheduleMatchup;
