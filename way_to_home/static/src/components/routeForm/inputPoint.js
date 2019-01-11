import {Component, Fragment} from "react";
import TextField from '@material-ui/core/TextField';
import React from "react";

export default class InputPoint extends Component {

    state = {
      name: this.props.name,
      value: this.props.value,
      multiline: 'Controlled',
    }

  handleChange = event => {
      let value = event.target.value;
      if (value.length > 3){
        this.props.onChange(value)
      }else{
        this.props.onChange(undefined);
      }
  };

    render() {

      return (
        <Fragment>
          <TextField
            label={this.props.name}
            value={this.props.value}
            InputLabelProps={{ shrink: true }}
            onChange={this.handleChange}/>
        </Fragment>
      )
    }
};
