import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles((theme) => ({}));

const ModelPage = ({
  rValue,
  handleRValueChange,
  positivityRate,
  handlePositivityRateChange,
  numDays,
  handleNumDaysChange,
  population,
  handlePopulationChange,
}) => {
  const classes = useStyles();
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h6">Model Inputs:</Typography>
      </Grid>

      <Grid item xs={3}>
        <TextField
          id="r-value-input"
          label="r Value"
          value={rValue}
          onChange={handleRValueChange}
          variant="outlined"
        />
      </Grid>
      <Grid item xs={3}>
        <TextField
          id="positivity-rate-input"
          label="Positivity Rate"
          value={positivityRate}
          onChange={handlePositivityRateChange}
          variant="outlined"
        />
      </Grid>

      <Grid item xs={3}>
        <TextField
          id="length-days-input"
          label="Number of Days (in 10s of days)"
          value={numDays}
          onChange={handleNumDaysChange}
          variant="outlined"
        />
      </Grid>

      <Grid item xs={3}>
        <TextField
          id="population-input"
          label="Population"
          value={population}
          onChange={handlePopulationChange}
          variant="outlined"
        />
      </Grid>
    </Grid>
  );
};

export default ModelPage;
