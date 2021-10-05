import React from "react";
import "../../index.js";
import DailyScheduleMatchupTeam from "./DailyScheduleMatchupTeam.js";

const DailyScheduleMatchup = ({ homeTeam, awayTeam, score }) => {
    return (
        <div className="box-border border-4 m-4 p-2 rounded-md bg-white border-gray-700 shadow-xl">
            <div className="flex justify-center space-x-5 md:space-x-30 lg:space-x-52">
                <div className="font-semibold grid place-items-center">
                    Home: <DailyScheduleMatchupTeam teamName={homeTeam} />
                </div>
                <div className="flex flex-col justify-around text-center">
                    <h1 className="text-2xl">vs</h1>
                    <h2 className="text-4xl font-bold">{score}</h2>
                </div>
                <div className="font-semibold grid place-items-center">
                    Away: <DailyScheduleMatchupTeam teamName={awayTeam} />
                </div>
            </div>
        </div>
    );
};

export default DailyScheduleMatchup;
