import React from "react";
import axios from "axios";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles((theme) => ({
  labelRoot: {
    display: "flex",
    padding: theme.spacing(1, 1),
  },
  input: {
    width: 60,
    height: 20,
    marginRight: theme.spacing(2),
  },
}));

const SideBarRow = ({ businessType, id, ogOpCapacity }) => {
  const classes = useStyles();
  const [opCapacity, setOpCapacity] = React.useState(ogOpCapacity);

  const handleOpCapacityChange = (event) => {
    setOpCapacity(event.target.value);

    axios({
      method: "post",
      url: "http://127.0.0.1:5000/opCapacity",
      data: {
        id: id,
        OpCapacity: event.target.value,
      },
    }).then(function (response) {
      console.log(response.data);
    });
  };

  const handleOpCapacityBlur = () => {
    if (opCapacity < 0) {
      setOpCapacity(0.0);
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/opCapacity",
        data: {
          id: id,
          OpCapacity: 0.0,
        },
      }).then(function (response) {
        console.log(response.data);
      });
    } else if (opCapacity > 1.0) {
      setOpCapacity(1.0);
      axios({
        method: "post",
        url: "http://127.0.0.1:5000/opCapacity",
        data: {
          id: id,
          OpCapacity: 1.0,
        },
      }).then(function (response) {
        console.log(response.data);
      });
    }
  };

  return (
    <div className={classes.labelRoot}>
      <Grid container spacing={3} alignItems="center" justify="space-between">
        <Grid item>
          <Typography variant="body1" color="inherit">
            {businessType}
          </Typography>
        </Grid>
        <Grid item>
          <TextField
            className={classes.input}
            value={opCapacity}
            onChange={handleOpCapacityChange}
            onBlur={handleOpCapacityBlur}
            size="small"
            inputProps={{
              step: 0.01,
              min: 0,
              max: 1.0,
              type: "number",
              size: "small",
              "aria-labelledby": `${id}-op-capacity-slider`,
            }}
          />
        </Grid>
      </Grid>
    </div>
  );
};

export default SideBarRow;
