import React from "react";
import axios from "axios";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import TreeView from "@material-ui/lab/TreeView";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import TreeItem from "@material-ui/lab/TreeItem";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Drawer from "@material-ui/core/Drawer";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import SideBarRow from "./SideBarRow";

import SideBarFooter from "./SideBarFooter";

const drawerWidth = 450;

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    maxWidth: 450,
    marginLeft: theme.spacing(2),
    paddingTop: theme.spacing(2),
    marginBottom: theme.spacing(5),
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerContainer: {
    overflow: "auto",
    marginBottom: "5rem",
  },
  metrics: {
    padding: theme.spacing(2),
    paddingBottom: theme.spacing(4),
  },
  headerContainer: {
    position: "fixed",
    width: "450px",
    left: "0px",
    zIndex: 1,
  },
  metricsHeader: {
    margin: theme.spacing(2),
    paddingRight: theme.spacing(4),
  },
  sideBarDecriptionText: {
    paddingTop: theme.spacing(10),
    paddingRight: theme.spacing(1),
  },
}));

const SideBar = ({
  rValue,
  positivityRate,
  numDays,
  population,
  setCasesData,
  rows,
  setTotalEconomicImpact,
  setGdpImpact, //GDP
  setBusinessImpact //Business
}) => {
  const classes = useStyles();
  const [expanded, setExpanded] = React.useState(["1", "16", "19"]);
  const [selected, setSelected] = React.useState([]);

  const handleToggle = (event, nodeIds) => {
    setExpanded(nodeIds);
  };

  const handleSelect = (event, nodeIds) => {
    setSelected(nodeIds);
  };

  const handleCalculate = async () => {
    // make a call to the backend
    await axios({
      method: "post",
      url: "http://127.0.0.1:5000/cases",
      data: {
        rValue: parseFloat(rValue),
        positivityRate: parseFloat(positivityRate),
        numDays: parseFloat(numDays),
        population: parseFloat(population),
      },
    }).then(function (response) {
      console.log(response.data);
      setCasesData(response.data);
    });

    await axios({
      method: "post",
      url: "http://127.0.0.1:5000/economy/data",
    }).then(function (response) {
      setTotalEconomicImpact(response.data);
    });
    await axios({
      method: "post",
      url: "http://127.0.0.1:5000/economy/data/Gdp",//piyush
    }).then(function (response) {
      setGdpImpact(response.data);
    });
    await axios({
      method: "post",
      url: "http://127.0.0.1:5000/economy/data/Business",//piyush
    }).then(function (response) {
      setBusinessImpact(response.data);
    });
  };

  const renderSideBarRows = (categoryLabel, categoryNumber) => {
    return rows
      .filter((row) => row.Subsection === categoryLabel)
      .map(({ id, BusinessType, OpCapacity }) => {
        return (
          <TreeItem
            nodeId={id + categoryNumber}
            label={
              <SideBarRow
                businessType={BusinessType}
                id={id}
                ogOpCapacity={OpCapacity}
              />
            }
          />
        );
      });
  };

  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
    >
      <Toolbar />
      <div className={classes.drawerContainer}>
        <Grid item>
          <Grid
            container
            direction="column"
            spacing={5}
            className={classes.metrics}
          >
            <Card variant="outlined" className={classes.headerContainer}>
              <Grid
                container
                justify="space-between"
                direction="row"
                className={classes.metricsHeader}
              >
                <Grid item>
                  <Typography variant="h6">Metrics</Typography>
                </Grid>
                <Grid item>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={() => handleCalculate()}
                  >
                    Calculate
                  </Button>
                </Grid>
              </Grid>
            </Card>
          </Grid>

          <Grid
            container
            justify="flex-end"
            className={classes.sideBarDecriptionText}
          >
            <Typography>Occupancy (%)</Typography>
          </Grid>
          <Grid item>
            <TreeView
              className={classes.root}
              defaultCollapseIcon={<ExpandMoreIcon />}
              defaultExpandIcon={<ChevronRightIcon />}
              expanded={expanded}
              selected={selected}
              onNodeToggle={handleToggle}
              onNodeSelect={handleSelect}
            >
              <TreeItem nodeId="1" label="Sports and Rec">
                {renderSideBarRows("Sports and Rec", 1)}
              </TreeItem>

              <TreeItem nodeId="18" label="School">
                {renderSideBarRows("School", 2)}
              </TreeItem>

              <TreeItem nodeId="24" label="Social Gathering">
                {renderSideBarRows("Social Gathering", 3)}
              </TreeItem>

              <TreeItem nodeId="32" label="Religious Gathering">
                {renderSideBarRows("Religious Gathering", 4)}
              </TreeItem>

              <TreeItem nodeId="34" label="Shopping">
                {renderSideBarRows("Shopping", 5)}
              </TreeItem>

              <TreeItem nodeId="39" label="Restaurants">
                {renderSideBarRows("Restaurants", 6)}
              </TreeItem>

              <TreeItem nodeId="46" label="Entertainment">
                {renderSideBarRows("Entertainment", 7)}
              </TreeItem>

              <TreeItem nodeId="61" label="University/College">
                {renderSideBarRows("University/College", 8)}
              </TreeItem>

              <TreeItem nodeId="64" label="Health Care">
                {renderSideBarRows("Health Care", 9)}
              </TreeItem>

              <TreeItem nodeId="70" label="Self Care">
                {renderSideBarRows("Self Care", 10)}
              </TreeItem>

              <TreeItem nodeId="82" label="Economic">
                {renderSideBarRows("Economic", 11)}
              </TreeItem>

              <TreeItem nodeId="88" label="Personal Services">
                {renderSideBarRows("Personal Services", 12)}
              </TreeItem>

              <TreeItem nodeId="97" label="Nature">
                {renderSideBarRows("Nature", 13)}
              </TreeItem>

              <TreeItem nodeId="103" label="Community Services">
                {renderSideBarRows("Community Services", 14)}
              </TreeItem>

              <TreeItem nodeId="108" label="Attractions and Heritage">
                {renderSideBarRows("Attractions and Heritage", 15)}
              </TreeItem>

              <TreeItem nodeId="116" label="Animal Services">
                {renderSideBarRows("Animal Services", 16)}
              </TreeItem>
            </TreeView>
          </Grid>
          <SideBarFooter />
        </Grid>
      </div>
    </Drawer>
  );
};

export default SideBar;
