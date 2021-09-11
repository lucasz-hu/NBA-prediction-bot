import "./App.css";
import React, { useEffect, useState } from "react";
import Prediction from "./components/prediction/Prediction";
import DailySchedule from "./components/prediction/DailySchedule";

const App = () => {
    return (
        <>
            <Prediction />
            <DailySchedule />
        </>
    );
};

export default App;
