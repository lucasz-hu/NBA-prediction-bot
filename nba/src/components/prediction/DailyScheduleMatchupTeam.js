import React from "react";

const DailyScheduleMatchupTeam = ({ teamName }) => {
    const teamAbbreviations = {
        ATL: "ATLANTA HAWKS",
        BOS: "BOSTON CELTICS",
        BRK: "BROOKLYN NETS",
        CHI: "CHICAGO BULLS",
        CHO: "CHARLOTTE HORNETS",
        CLE: "CLEVELAND CAVALIERS",
        DAL: "DALLAS MAVERICKS",
        DEN: "DENVER NUGGETS",
        DET: "DETROIT PISTONS",
        GSW: "GOLDEN STATE WARRIORS",
        HOU: "HOUSTON ROCKETS",
        IND: "INDIANA PACERS",
        LAC: "LOS ANGELES CLIPPERS",
        LAL: "LOS ANGELES LAKERS",
        MEM: "MEMPHIS GRIZZLIES",
        MIA: "MIAMI HEAT",
        MIL: "MILWAUKEE BUCKS",
        MIN: "MINNESOTA TIMBERWOLVES",
        NOP: "NEW ORLEANS PELICANS",
        NYK: "NEW YORK KNICKS",
        OKC: "OKLAHOMA CITY THUNDER",
        ORL: "ORLANDO MAGIC",
        PHI: "PHILADELPHIA 76ERS",
        PHO: "PHOENIX SUNS",
        POR: "PORTLAND TRAIL BLAZERS",
        SAC: "SACRAMENTO KINGS",
        SAS: "SAN ANTONIO SPURS",
        TOR: "TORONTO RAPTORS",
        UTA: "UTAH JAZZ",
        WAS: "WASHINGTON WIZARDS",
    };
    const fullTeamName = teamAbbreviations[teamName];
    return (
        <div className="grid place-items-center">
            <img
                src={`/team_logos/${fullTeamName}.PNG`}
                alt={fullTeamName + " logo"}
                className="object-contain h-16 w-16 md:h-36 md:w-36"
            ></img>
            <p className="font-semibold">{fullTeamName}</p>
        </div>
    );
};

export default DailyScheduleMatchupTeam;
