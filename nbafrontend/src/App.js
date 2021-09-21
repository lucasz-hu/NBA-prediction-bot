import "./App.css";
import react from "react";
import Prediction from "./components/prediction/Prediction";
import DailySchedule from "./components/prediction/DailySchedule";
import NavHeader from "./components/NavHeader";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import About from "./components/About";

const App = () => {
    return (
        <>
            <BrowserRouter>
                {/* <Prediction /> */}
                <NavHeader />
                <Switch>
                    <Route path="/about" component={About} />
                    <Route path="/" component={DailySchedule} />
                </Switch>
            </BrowserRouter>
        </>
    );
};

export default App;
