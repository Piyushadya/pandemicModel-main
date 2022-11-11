import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { DataGrid } from "@material-ui/data-grid";
import Grid from "@material-ui/core/Grid";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Typography from "@material-ui/core/Typography";

import TabPanel from "../components/TabPanel";
import EconomyMetricsTable from "../components/EconomyMetricsTable";
import CasesMetricsTable from "../components/CasesMetricsTable";

const MetricsPage = ({ rows, economicMetricsRows }) => {
  const [tabValue, setTabValue] = React.useState(0);

  const handleTabValueChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h3">Metrics:</Typography>
      </Grid>

      <Grid item xs={12}>
        <Tabs
          value={tabValue}
          indicatorColor="primary"
          textColor="primary"
          onChange={handleTabValueChange}
        >
          <Tab label="Cases" />
          <Tab label="Economy" />
        </Tabs>
        <TabPanel value={tabValue} index={0}>
          <div style={{ height: 500, width: "100%" }}>
            <CasesMetricsTable rows={rows} />
          </div>
        </TabPanel>
        <TabPanel value={tabValue} index={1}>
          <div style={{ height: 500, width: "100%" }}>
            <EconomyMetricsTable rows={economicMetricsRows} />
          </div>
        </TabPanel>
      </Grid>
    </Grid>
  );
};

export default MetricsPage;
