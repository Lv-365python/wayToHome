import React, {Component} from 'react';
import axios from "axios";

import TrendingFlat from '@material-ui/icons/TrendingFlat';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import DirectionsIcon from '@material-ui/icons/Directions';
import Dialog from '@material-ui/core/Dialog';
import CircularProgress from '@material-ui/core/CircularProgress';

import ModalMap from './modalMap';
import './newWayItem.css';
import { HERE_APP_CODE, HERE_APP_ID } from "src/settings";


export default class NewWayItem extends Component{

    state = {
        placeA: 'Виберіть місце A',
        placeB: 'Виберіть місце Б',
        mapOpen: false,
        loading: false,
        routes: [],
    };

    handleClickModalOpen = () => {
        this.setState({loading:true});

        let today = new Date();
        let tomorrow = new Date(today.getTime() + (24 * 60 * 60 * 1000)).toISOString();

        let placeA = this.props.places.find(place => place.id === this.state.placeA);
        let placeB = this.props.places.find(place => place.id === this.state.placeB);

        const url = `https://transit.api.here.com/v3/route.json?dep=${placeA.latitude}%2C${placeA.longitude}&arr=${placeB.latitude}%2C${placeB.longitude}&time=${tomorrow}&app_id=${HERE_APP_ID}&app_code=${HERE_APP_CODE}&routing=tt`;

        axios.get(url)
            .then(response => {
                let listRoutes = response.data.Res.Connections.Connection;
                this.setState({
                    routes: listRoutes,
                    mapOpen: true,
                    loading: false
                });
            })
             .catch(error => {
                 this.props.setError("Між між місцями неможливо прокласти маршрут. Виберіть інші місця");
                 this.setState({loading:false})
             });
    };

    handleModalClose = () => {
        this.setState({mapOpen: false});
    };

    newWayValidator(){
        if (this.state.placeA === this.state.placeB) {
            return false
        }

        if (!Number.isInteger(this.state.placeA) || !Number.isInteger(this.state.placeB)){
            return false
        }
        return true
    }

     handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
        });
     };

    saveButton = route => {
        this.setState({
            loading: true,
            mapOpen: false
        });
        this.props.saveRoute(this.state.placeA, this.state.placeB, route);
        this.setState({loading:false})
    };

    render() {
        const { places } = this.props;

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
                    {places.map(place => (
                        <MenuItem key={place.id} value={place.id}>
                            {place.name === '' ? place.address : place.name}
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
                    {places.map(place => (
                        <MenuItem key={place.id} value={place.id}>
                            {place.name === '' ? place.address : place.name}
                        </MenuItem>
                    ))}
                </TextField>

                <Tooltip title="Вибрати маршрут">
                    <div>
                        <IconButton
                            style={this.newWayValidator()?{color: "green"}:{color: "grey"}}
                            disabled={!this.newWayValidator()}
                            aria-label="Зберегти"
                            onClick={this.handleClickModalOpen}
                        >
                            <DirectionsIcon />
                        </IconButton>
                    </div>
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

                <Dialog open={this.state.mapOpen} >
                    <ModalMap
                        onClose={this.handleModalClose}
                        saveRoute={this.saveButton}
                        routes={this.state.routes}
                    />
                </Dialog>

                {this.state.loading && <CircularProgress size={64} className="buttonProgress"/>}

            </div>
        )
    }
}
