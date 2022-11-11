import React from "react";
import axios from "axios";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

export default function EconomyMetricsTable({ rows }) {
  const onMetricChange = (e, id, field) => {
    if (e.target.value > 0) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/setEconomyMetrics",
        data: {
          id: id,
          field: field,
          newVal: e.target.value,
        },
      }).then(function (response) {
        console.log(response.data);
      });
    }
  };
  const classes = useStyles();

  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow key={0}>
            <TableCell align="right">Sector</TableCell>
            <TableCell align="right">Number of Businesses</TableCell>
            <TableCell align="right">Number of Employees</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell align="right">{row.Sector}</TableCell>
              <TableCell align="right">
                <TextField
                  onChange={(e) => onMetricChange(e, row.id, "NumBusinesses")}
                  defaultValue={row.NumBusinesses}
                />
              </TableCell>

              <TableCell align="right">
                <TextField
                  onChange={(e) => onMetricChange(e, row.id, "NumEmployees")}
                  defaultValue={row.NumEmployees}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
