import "./App.css";
import DailySchedule from "./components/prediction/DailySchedule";
import NavHeader from "./components/NavHeader";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import About from "./components/About";

const App = () => {
    mixpanel.track("Mainpage viewed");
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
