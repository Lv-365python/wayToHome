import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import {Settings, TrendingFlat} from '@material-ui/icons';
import {Button} from "@material-ui/core";
import MenuItem from "@material-ui/core/MenuItem";
import './wayItem.css';


const currencies = [
  {
    value: 'USD',
    label: '$',
  },
  {
    value: 'EUR',
    label: '€',
  },
  {
    value: 'BTC',
    label: '฿',
  },
  {
    value: 'JPY',
    label: '¥',
  },
];

export default class WayItem extends Component{
    render(){
        return(
            <div className="wayItem">
               <TextField
                  select
                  className="textField"
                  label="Місце А"
                  value="xzxz"
                  // onChange={}

                  // helperText="Please select your currency"
                  margin="normal"
                >
                  {currencies.map(option => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>


                <TrendingFlat className="arrow" />


                <TextField
                  select
                  className="textField"
                  label="Місце Б"
                  value="xzxz"
                  // onChange={}

                  // helperText="Please select your currency"
                  margin="normal"
                >
                  {currencies.map(option => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>

                <Button><Settings/></Button>
            </div>
        )
    }
}
