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

const EconomyPage = ({ totalEconomicImpact }) => {
  const classes = useStyles();

  const data =
  totalEconomicImpact["q"] &&
  totalEconomicImpact["q"].map((num, index) => {
      return {
        name: num,
        jobs_changed: totalEconomicImpact["jobs_changed"][index],
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
          dataKey="jobs_changed"
          stroke="#8884d8"
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </>
  );
};

export default EconomyPage;
