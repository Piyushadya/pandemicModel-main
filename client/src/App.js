import React from "react";
import {
  makeStyles,
  createMuiTheme,
  ThemeProvider,
} from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import axios from "axios";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import SideBar from "./components/SideBar";
import TabPanel from "./components/TabPanel";
import ModelPage from "./pages/ModelPage";
import CasesPage from "./pages/CasesPage";
import EconomyPage from "./pages/EconomyPage";
import GdpPage from "./pages/GdpPage";
import BusinessPage from "./pages/BusinessPage";
import MetricsPage from "./pages/MetricsPage";

const theme = createMuiTheme({
  typography: {
    fontFamily: "Maven Pro, sans-serif",
  },
  palette: {
    primary: {
      main: "#106f91",
    },
  },
});

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  metrics: {
    padding: "4%",
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  nonLink: {
    color: "white",
    textDecoration: "none",
  },
}));

function App() {
  const classes = useStyles();

  const [tabValue, setTabValue] = React.useState();
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  const [subtabValue, setSubTabValue] = React.useState(); //piyush
  const handleSubTabChange = (event, subValue) => {
    setSubTabValue(subValue);
  };

  const [rValue, setRValue] = React.useState(1.2);
  const handleRValueChange = (event) => {
    setRValue(event.target.value);
  };

  const [positivityRate, setPositivityRate] = React.useState(0.07);
  const handlePositivityRateChange = (event) => {
    setPositivityRate(event.target.value);
  };

  const [numDays, setNumDays] = React.useState(10);
  const handleNumDaysChange = (event) => {
    setNumDays(event.target.value);
  };

  const [population, setPopulation] = React.useState(3000000);
  const handlePopulationChange = (event) => {
    setPopulation(event.target.value);
  };

  const [casesData, setCasesData] = React.useState({});
  const [rows, setRows] = React.useState([]);
  const [economicMetricsRows, setEconomicMetricsRows] = React.useState([]);
  const [totalEconomicImpact, setTotalEconomicImpact] = React.useState({});
  const [gdpImpact, setGdpImpact] = React.useState({}); //piyush
  const [businessImpact, setBusinessImpact] = React.useState({}); //piyush

  React.useEffect(async () => {
    await axios({
      method: "get",
      url: "http://127.0.0.1:5000/metrics",
    }).then(function (response) {
      console.log(response.data);
      setRows(response.data);
    });

    await axios({
      method: "get",
      url: "http://127.0.0.1:5000/economy/metrics",
    }).then(function (response) {
      console.log(response.data);
      setEconomicMetricsRows(response.data);
    });
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <div className={classes.root}>
        <Router>
          <AppBar position="fixed" className={classes.appBar}>
            <Toolbar>
              <Link to="/" className={classes.nonLink}>
                <Typography variant="h6" noWrap>
                  Pandemic Model
                </Typography>
              </Link>
            </Toolbar>
          </AppBar>
          <SideBar 
            rValue={rValue}
            positivityRate={positivityRate}
            numDays={numDays}
            population={population}
            setCasesData={setCasesData}
            rows={rows}
            setTotalEconomicImpact={setTotalEconomicImpact}
            setGdpImpact={setGdpImpact} // piyush
            setBusinessImpact={setBusinessImpact} // piyush
          />
          <main className={classes.content}>
            <Toolbar />

            <Switch>
              <Route path="/metrics">
                <MetricsPage
                  rows={rows}
                  economicMetricsRows={economicMetricsRows}
                />
              </Route>
              <Route path="/">
                <ModelPage
                  rValue={rValue}
                  positivityRate={positivityRate}
                  numDays={numDays}
                  population={population}
                  handleRValueChange={handleRValueChange}
                  handlePositivityRateChange={handlePositivityRateChange}
                  handleNumDaysChange={handleNumDaysChange}
                  handlePopulationChange={handlePopulationChange}
                />
                <Toolbar />
                <Tabs
                  value={tabValue}
                  onChange={handleTabChange}
                  indicatorColor="primary"
                  textColor="primary"
                >
                  <Tab label="Cases" />
                  <Tab label="Economy" />
                </Tabs>
                <TabPanel value={tabValue} index={0}>
                  <CasesPage casesData={casesData} />
                </TabPanel>
                <TabPanel value={tabValue} index={1}>
                  <Tabs
                    value={subtabValue}
                    onChange={handleSubTabChange}
                    indicatorColor="primary"
                    textColor="primary"
                  >
                    <Tab label="Jobs Changed" />
                    <Tab label="GDP changed" />
                    <Tab label="Business closed" />
                  </Tabs>
                  <TabPanel value={subtabValue} index={0}>
                    <EconomyPage
                      totalEconomicImpact={totalEconomicImpact}
                    />
                  </TabPanel>
                  <TabPanel value={subtabValue} index={1}>
                    <GdpPage 
                      gdpImpact={gdpImpact}/>
                  </TabPanel>
                  <TabPanel value={subtabValue} index={2}> 
                    <BusinessPage 
                      businessImpact={businessImpact}/> 
                  </TabPanel>
                </TabPanel>
              </Route>
            </Switch>
          </main>
        </Router>
      </div>
    </ThemeProvider>
  );
}

export default App;
