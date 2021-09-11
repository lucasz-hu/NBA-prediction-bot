import React, { useEffect } from "react";
import PredictionSelect from "./PredictionSelect";

const Prediction = () => {
    const [homeTeam, setHomeTeam] = React.useState("");
    const [awayTeam, setAwayTeam] = React.useState("");
    const [result, setResult] = React.useState(0);

    useEffect(() => {
        fetch(
            `http://127.0.0.1:5000/prediction/?homeTeam=${homeTeam}&awayTeam=${awayTeam}`
        )
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
                throw response;
            })
            .then((data) => {
                setResult(data["score"]);
            });
    }, [JSON.stringify(homeTeam), JSON.stringify(awayTeam)]);

    const handleHomeTeamChange = (event) => {
        event.preventDefault();
        setHomeTeam(event.target.value);
    };

    const handleAwayTeamChange = (event) => {
        event.preventDefault();
        setAwayTeam(event.target.value);
    };
    return (
        <>
            <PredictionSelect
                handleHomeTeamChange={handleHomeTeamChange}
                handleAwayTeamChange={handleAwayTeamChange}
            />
            <h1>Result: {result}</h1>
        </>
    );
};

export default Prediction;
