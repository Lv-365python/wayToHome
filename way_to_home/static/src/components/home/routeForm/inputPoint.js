import React, {Component, Fragment} from "react";
import TextField from '@material-ui/core/TextField';


export default class InputPoint extends Component {

    handleChange = event => {
        let value = event.target.value;
        if (value.length > 3) {
            this.props.onChange(value)
        } else {
            this.props.onChange()
        }
    };

    render(){
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
