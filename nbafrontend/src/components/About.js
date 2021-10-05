import React from "react";

const About = () => {
    return (
        <div className="text-center">
            <h1 className="text-4xl">NBA Four Factors Betting Model</h1>
            <p>
                This NBA betting model uses the{" "}
                <a
                    href="https://www.basketball-reference.com/about/factors.html"
                    className="underline text-blue-600 hover:text-blue-800 visited:text-purple-600"
                >
                    four factors of basketball
                </a>{" "}
                developed by{" "}
                <a
                    href="http://www.basketballonpaper.com/"
                    className="underline text-blue-600 hover:text-blue-800 visited:text-purple-600"
                >
                    Dean Oliver
                </a>
            </p>
            <p>
                Shooting is measured with Effective Field Goal Percentage{" "}
                <p className="font-serif">((FG + 0.5 * 3P) / FGA)</p>
            </p>
            <p>
                Turnovers are measured with Turn Over Percentage{" "}
                <p className="font-serif">(TOV / (FGA + 0.44 * FTA + TOV))</p>
            </p>
            <p>
                Rebounds are measured with Offensive/Defensive Rebound
                Percentage{" "}
                <p className="font-serif">(ORB / (ORB + Opponent DRB))</p> For
                defense it's{" "}
                <p className="font-serif">(DRB / (Opp ORB + DRB))</p>
            </p>
            <p>
                Fouls are the only stat I've messed with. It's originally{" "}
                <p className="font-serif">
                    (Free Throws / Field Goals Attempt)
                </p>
                , but I've changed it to{" "}
                <p className="font-serif">(Free Throws / Field Goals Made)</p>{" "}
                to account for a team's ability to make free throws
            </p>
        </div>
    );
};

export default About;
