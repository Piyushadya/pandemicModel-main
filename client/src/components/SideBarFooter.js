import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import ArrowForwardIcon from "@material-ui/icons/ArrowForward";
import Grid from "@material-ui/core/Grid";
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  root: {
    position: "fixed",
    left: "0px",
    bottom: "0px",
    width: "450px",
  },
  margin: {
    margin: theme.spacing(1),
  },
  textMargin: {
    margin: theme.spacing(2),
  },
}));

const SideBarFooter = () => {
  const classes = useStyles();

  return (
    <Card className={classes.root} variant="outlined">
      <Grid container alignItems="center" justify="space-between">
        <Grid item>
          <Typography className={classes.textMargin} gutterBottom>
            View and Edit Metrics
          </Typography>
        </Grid>

        <Grid item>
          <Link to="/metrics">
            <IconButton
              aria-label="edit-metrics-arrow"
              className={classes.margin}
            >
              <ArrowForwardIcon fontSize="large" />
            </IconButton>
          </Link>
        </Grid>
      </Grid>
    </Card>
  );
};

export default SideBarFooter;
