import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import ArrowUpwardIcon from "@material-ui/icons/ArrowUpward";
import ArrowDownwardIcon from "@material-ui/icons/ArrowDownward";

const useStyles = makeStyles({});

export default function EconomyTotalCard({ title, direction, data }) {
  const classes = useStyles();

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>

        <Grid container alignItems="center">
          <Grid item xs={3}>
            {direction === 1 ? (
              <ArrowUpwardIcon style={{ fontSize: 70, color: "green" }} />
            ) : (
              <ArrowDownwardIcon style={{ fontSize: 70, color: "red" }} />
            )}
          </Grid>

          <Grid item xs={9}>
            <Typography
              variant="h4"
              style={{
                color: direction === 1 ? "green" : "red",
                marginLeft: "1rem",
              }}
            >
              {Number.parseFloat((Math.abs(data))).toFixed(3)}
            </Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
