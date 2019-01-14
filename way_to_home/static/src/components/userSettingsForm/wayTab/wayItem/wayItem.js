import React, {Component} from 'react';

import {TrendingFlat} from '@material-ui/icons';
import Chip from '@material-ui/core/Chip';
import IconButton from '@material-ui/core/IconButton';
import SettingsIcon from '@material-ui/icons/Settings';
import PlaceIcon from '@material-ui/icons/Place';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import './wayItem.css';
import axios from "axios";


export default class WayItem extends Component{

    state = {
        startPlace: {},
        endPlace: {},
    };

    getData = () => {
        let url = 'http://127.0.0.1:8000/api/v1/';

        let startPlace = this.props.way.routes.reduce(function(prev, curr) {
            return prev.position < curr.position ? prev : curr;
        });

        let endPlace = this.props.way.routes.reduce(function(prev, curr) {
            return prev.position > curr.position ? prev : curr;
        });

        let requestStartPlace = `place/${startPlace.start_place}`;
        let requestEndPlace = `place/${endPlace.end_place}`;

        axios.get(url + requestStartPlace)
            .then(response => {
                this.setState({ startPlace: response.data });
            });

        axios.get(url + requestEndPlace)
            .then(response => {
                this.setState({ endPlace: response.data });
            });
    };

    componentWillMount() {
        this.getData();
    };

    handleDeleteButton = () => {
        console.log('delete')
    };

    render(){
        return(
            <div className="wayItem">
               <Chip
                   className="textField"
                   color="primary"
                   icon={<PlaceIcon />}
                   label={this.state.startPlace.name}
                   variant="outlined"
               />


                <TrendingFlat className="arrow" />

                <Chip
                    className="textField"
                    color="primary"
                    icon={<PlaceIcon color="secondary"/>}
                    label={this.state.endPlace.name}
                    variant="outlined"
                />


                <Tooltip title="Settings">
                    <IconButton color="primary" aria-label="Нотифікації">
                         <SettingsIcon />
                    </IconButton>
                </Tooltip>

                <Tooltip title="Delete">
                    <IconButton color="secondary" aria-label="Видалити" onClick={this.handleDeleteButton}>
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>

            </div>

        )
    }
}
