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

export default function CasesMetricsTable({ rows }) {
  const onMetricChange = (e, id, field) => {
    if (e.target.value > 0) {
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/setCasesMetrics",
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
            <TableCell align="right">Subsection</TableCell>
            <TableCell align="right">Business Type</TableCell>
            <TableCell align="right">Quantity</TableCell>
            <TableCell align="right">Average Population</TableCell>
            <TableCell align="right">Relative Risk</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell align="right">{row.Subsection}</TableCell>
              <TableCell align="right">{row.BusinessType}</TableCell>

              <TableCell align="right">
                <TextField
                  onChange={(e) => onMetricChange(e, row.id, "Quantity")}
                  defaultValue={row.Quantity}
                />
              </TableCell>

              <TableCell align="right">
                <TextField
                  onChange={(e) => onMetricChange(e, row.id, "AvgPop")}
                  defaultValue={row.AvgPop}
                />
              </TableCell>

              <TableCell align="right">
                <TextField
                  onChange={(e) => onMetricChange(e, row.id, "RelRisk")}
                  defaultValue={row.RelRisk}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
