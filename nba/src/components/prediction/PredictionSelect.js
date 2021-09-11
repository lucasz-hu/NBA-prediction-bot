import React from "react";

const PredictionSelect = ({ handleHomeTeamChange, handleAwayTeamChange }) => {
    return (
        <form>
            <label htmlFor="homeTeamSelect">Choose a home team: </label>
            <select
                name="homeTeam"
                id="homeTeamSelect"
                onChange={handleHomeTeamChange}
            >
                <option value="">--Home Team--</option>
                <option value="ATL">Atlanta Hawks</option>
                <option value="BOS">Boston Celtics</option>
                <option value="BRK">Brooklyn Nets</option>
                <option value="CHI">Chicago Bulls</option>
                <option value="CHO">Charlotte Hornets</option>
                <option value="CLE">Cleveland Cavaliers</option>
                <option value="DAL">Dallas Mavericks</option>
                <option value="DEN">Denver Nuggets</option>
                <option value="DET">Detroit Pistons</option>
                <option value="GSW">Golden State Warriors</option>
                <option value="HOU">Houston Rockets</option>
                <option value="IND">Indiana Pacers</option>
                <option value="LAC">Los Angeles Clippers</option>
                <option value="LAL">Los Angeles Lakers</option>
                <option value="MEM">Memphis Grizzlies</option>
                <option value="MIA">Miami Heat</option>
                <option value="MIL">Milwaukee Bucks</option>
                <option value="MIN">Minnesota Timberwolves</option>
                <option value="NOP">New Orleans Pelicans</option>
                <option value="NYK">New York Knicks</option>
                <option value="OKC">Oklahoma City Thunder</option>
                <option value="ORL">Orlando Magic</option>
                <option value="PHI">Philadelphia 76ers</option>
                <option value="PHO">Phoenix Suns</option>
                <option value="POR">Portland Trailblazers</option>
                <option value="SAC">Sacramento Kings</option>
                <option value="SAS">San Antonio Spurs</option>
                <option value="TOR">Toronto Raptors</option>
                <option value="UTA">Utah Jazz</option>
                <option value="WAS">Washington Wizards</option>
            </select>

            <label htmlFor="awayTeamSelect">Choose an away team: </label>
            <select
                name="awayTeam"
                id="awayTeamSelect"
                onChange={handleAwayTeamChange}
            >
                <option value="">--Away Team--</option>
                <option value="ATL">Atlanta Hawks</option>
                <option value="BOS">Boston Celtics</option>
                <option value="BRK">Brooklyn Nets</option>
                <option value="CHI">Chicago Bulls</option>
                <option value="CHO">Charlotte Hornets</option>
                <option value="CLE">Cleveland Cavaliers</option>
                <option value="DAL">Dallas Mavericks</option>
                <option value="DEN">Denver Nuggets</option>
                <option value="DET">Detroit Pistons</option>
                <option value="GSW">Golden State Warriors</option>
                <option value="HOU">Houston Rockets</option>
                <option value="IND">Indiana Pacers</option>
                <option value="LAC">Los Angeles Clippers</option>
                <option value="LAL">Los Angeles Lakers</option>
                <option value="MEM">Memphis Grizzlies</option>
                <option value="MIA">Miami Heat</option>
                <option value="MIL">Milwaukee Bucks</option>
                <option value="MIN">Minnesota Timberwolves</option>
                <option value="NOP">New Orleans Pelicans</option>
                <option value="NYK">New York Knicks</option>
                <option value="OKC">Oklahoma City Thunder</option>
                <option value="ORL">Orlando Magic</option>
                <option value="PHI">Philadelphia 76ers</option>
                <option value="PHO">Phoenix Suns</option>
                <option value="POR">Portland Trailblazers</option>
                <option value="SAC">Sacramento Kings</option>
                <option value="SAS">San Antonio Spurs</option>
                <option value="TOR">Toronto Raptors</option>
                <option value="UTA">Utah Jazz</option>
                <option value="WAS">Washington Wizards</option>
            </select>
        </form>
    );
};

export default PredictionSelect;
