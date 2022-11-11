import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const useStyles = makeStyles((theme) => ({}));

const CasesPage = ({ casesData }) => {
  const classes = useStyles();

  const data =
    casesData["x"] &&
    casesData["x"].map((num, index) => {
      return {
        name: num,
        y_total: casesData["y_total"][index],
        y_new: casesData["y_new"][index],
        y_active: casesData["y_active"][index],
      };
    });

  return (
    <>
      <LineChart
        width={800}
        height={400}
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="y_total"
          stroke="#8884d8"
          activeDot={{ r: 8 }}
        />
        <Line type="monotone" dataKey="y_new" stroke="#82ca9d" />
        <Line type="monotone" dataKey="y_active" stroke="#873a9d" />
      </LineChart>
      x:
      <ul>{casesData["x"] && casesData["x"].map((num) => <li>{num}</li>)}</ul>
      y_total:
      <ul>
        {casesData["y_total"] &&
          casesData["y_total"].map((num) => <li>{num}</li>)}
      </ul>
      y_new:
      <ul>
        {casesData["y_new"] && casesData["y_new"].map((num) => <li>{num}</li>)}
      </ul>
      y_active:
      <ul>
        {casesData["y_active"] &&
          casesData["y_active"].map((num) => <li>{num}</li>)}
      </ul>
    </>
  );
};

export default CasesPage;
