import React, {Component} from 'react';

import {TrendingFlat} from "@material-ui/icons";
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import SaveAlt from '@material-ui/icons/SaveAlt';

import './newWayItem.css';
import axios from "axios";

const url = 'http://127.0.0.1:8000/api/v1/';


export default class NewWayItem extends Component{

    state = {
        places: [],
        placeA: 'Виберіть місце A',
        placeB: 'Виберіть місце Б',
    };

    getData = () => {
        let requestPlaces = 'place/';

        axios.get(url + requestPlaces)
            .then(response => {
                this.setState({ places: response.data });
            });
    };

    handleSaveButton = () =>{

        // let postWay = 'way/';
        //
        // axios.post(url + postWay)
        //     .then(response => {
        //         this.setState({ places: response.data });
        //     });

        console.log("save")
    };

    componentWillMount() {
        this.getData();
    };

    newWayValidator(){
        if (this.state.placeA === this.state.placeB) {
            console.log("placeA and placeB should be different")
            return false
        }

        if (!Number.isInteger(this.state.placeA) || !Number.isInteger(this.state.placeB)){
            console.log("select place")
            return false
        }

        return true
    }

     handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
         });
     };

    render() {
        return (
            <div className="newWayItem">
                <TextField
                  select
                  className="textField"
                  label="Місце А"
                  value={this.state.placeA}
                  onChange={this.handleChange('placeA')}
                  helperText="Виберіть одне з Ваших збережених місць"
                  margin="normal"
                >
                  {this.state.places.map(place => (
                    <MenuItem key={place.id} value={place.id}>
                      {place.name}
                    </MenuItem>
                  ))}
                </TextField>

                <TrendingFlat className="arrow" />

                <TextField
                  select
                  className="textField"
                  label="Місце Б"
                  value={this.state.placeB}
                  onChange={this.handleChange('placeB')}
                  helperText="Виберіть одне з Ваших збережених місць"
                  margin="normal"
                >
                  {this.state.places.map(place => (
                    <MenuItem key={place.id} value={place.id}>
                      {place.name}
                    </MenuItem>
                  ))}
                </TextField>

                <Tooltip title="Зберегти">
                    <IconButton
                        style={this.newWayValidator()?{color: "green"}:{color: "grey"}}
                        disabled={!this.newWayValidator()}
                        aria-label="Зберегти"
                        onClick={this.handleSaveButton}
                    >
                        <SaveAlt />
                    </IconButton>
                </Tooltip>

                <Tooltip title="Видалити">
                    <IconButton
                        color="secondary"
                        aria-label="Видалити"
                        onClick={this.props.deleteButton}
                    >
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>

            </div>
        )
    }
}
