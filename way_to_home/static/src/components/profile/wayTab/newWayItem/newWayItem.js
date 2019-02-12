/* global google */
import React, {Component} from 'react';

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


export default class NewWayItem extends Component{

    state = {
        placeA: 'Виберіть місце A',
        placeB: 'Виберіть місце Б',
        mapOpen: false,
        loading: false,
        route: undefined,
        routeInfo: undefined
    };

    handleClickModalOpen = () => {
        this.setState({loading: true});

        let placeA = this.props.places.find(place => place.id === this.state.placeA);
        let placeB = this.props.places.find(place => place.id === this.state.placeB);

        let from = {
            lat: placeA.latitude,
            lng: placeA.longitude
        };
        let to = {
            lat: placeB.latitude,
            lng: placeB.longitude
        };
        this.getDirections(from, to);

    };

    getDirections = (from, to) => {
        const DirectionsService = new google.maps.DirectionsService();

        DirectionsService.route({
            origin: new google.maps.LatLng(from.lat, from.lng),
            destination: new google.maps.LatLng(to.lat, to.lng),
            travelMode: google.maps.TravelMode.TRANSIT,

        }, (result, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
                let routeInfo = [];
                let route = result.routes[0].legs[0].steps;
                route.map(step => {
                    routeInfo.push({
                        polyline: step.polyline.points,
                        start_location: {
                            lat: step.start_location.lat,
                            lng: step.start_location.lng
                        },
                        end_location: {
                            lat: step.end_location.lat,
                            lng: step.end_location.lng
                        },
                        duration: step.duration.value,
                        transit: step.transit ? step.transit.line.short_name : undefined
                    })
                });
                this.setState({
                    route: route,
                    routeInfo: routeInfo,
                    mapOpen: true,
                    loading: false
                })

            } else {
                this.props.setMessage("Не вдалось прокласти маршрут", 'error')
            }
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

        this.setState({loading:false});
        this.props.setMessage("Маршрут успішно збережено", 'success')

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
                        route={this.state.route}
                        routeInfo={this.state.routeInfo}
                    />
                </Dialog>

                {this.state.loading && <CircularProgress size={64} className="buttonProgress"/>}

            </div>
        )
    }
}
