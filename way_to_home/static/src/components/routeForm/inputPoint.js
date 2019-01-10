import {Component} from "react";
import TextField from '@material-ui/core/TextField';
import React from "react";

export default class InputPoint extends Component {

    state = {
      name: this.props.name,
      value: undefined,
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
        <div>
          <TextField
            label={this.state.name}
            value={this.state.value}
            onChange={this.handleChange}/>
        </div>
      )
    }
};
