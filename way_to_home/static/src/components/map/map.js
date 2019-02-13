import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, Polyline, InfoWindow } from 'google-maps-react';
import { GOOGLE_MAP_API } from "src/settings"
import { CustomizedSnackbars } from '../index';
import {ResultForm, StartBtn} from '.';
import axios from "axios";
import './map.css'

export class MapContainer extends Component {

    state = {
        startPoint: undefined,
        endPoint: undefined,
        coordsWay: undefined,
        map: undefined,
        error: undefined,
        pointMarkerStart: {lat: 49.84, lng: 24.028667 },
        pointMarkerEnd: {lat: 49.84, lng: 24.028667 },
        openResultForm: false,
        routes: undefined,
        choice: undefined,
        showingInfoWindow: false,
        activeMarker: {},
        selectedPlace: undefined
    };

    setStartPoint = (start) => {
        this.setState({
            startPoint: start,
        });
    };

    setEndPoint = (end) => {
        this.setState({
            endPoint: end,
        });
    };

    setError = (error) => {
        this.setState({
            error: error,
        });
    };

    setChoice = (choice) =>{
        this.setState({
            choice: choice,
        });
    };

    setPlace = (addr) =>{
        this.setState({
            selectedPlace: addr,
        });
    };

    setCoords = (coords) => {
        this.setState({
            coordsWay: coords,
        });
    };

    setPointMarkerStart = (point) =>{
        this.setState({
            pointMarkerStart: point,
        });
    };

    setPointMarkerEnd = (point) =>{
        this.setState({
            pointMarkerEnd: point,
        });
    };

    onMarkerDrag = (coord, key) =>{
        if(this.state.coordsWay) {
            this.setCoords();
        }
        if(this.state.selectedPlace) {
            this.setPlace();
        }
        const { latLng } = coord;
        const point = {lat: latLng.lat(), lng: latLng.lng()};
        if(key === 1){
            this.setPointMarkerStart(point);
        }else{
            this.setPointMarkerEnd(point);
        }
        this.setChoice('marker');
    };

    onMarkerClick = (props, marker) => {
        const {pointMarkerStart, pointMarkerEnd} = this.state;
        if(marker.name === 1) {
            this.convertToAddress(pointMarkerStart.lat, pointMarkerStart.lng, this.setPlace);
        }else{
            this.convertToAddress(pointMarkerEnd.lat, pointMarkerEnd.lng, this.setPlace);
        }
        this.setState({
            activeMarker: marker,
            showingInfoWindow: true
        });
    };

    onMapClicked = () => {
        if (this.state.showingInfoWindow) {
            this.setState({
                showingInfoWindow: false,
                activeMarker: null,
                selectedPlace: undefined
            })
        }
    };

    convertToAddress = (latitude, longitude, callfunc) => {
        let url = 'https://nominatim.openstreetmap.org/reverse';
        axios.get(url, {
            params: {
                format: 'jsonv2',
                lat: latitude,
                lon: longitude
            }
        })
            .then(response => {
                const address = this.getAddress(response);
                callfunc(address);
            })
            .catch(error => {
                this.setError("Неможливо визначити адресу.");
            });
    };

    getAddress = response => {
        const address = response.data.address;
        let addr = `${address.town || address.city}, ${address.road || address.path || address.suburb}`;

        if (address.house_number)
            addr += `, ${address.house_number}`;

        if (addr.includes("undefined"))
            addr = "Неможливо визначити місце.";

        return addr;
    };

    getCoordsWay = () => {
        const {startPoint, endPoint, pointMarkerStart, pointMarkerEnd, choice} = this.state;
        const DirectionsService = new google.maps.DirectionsService();
        let start, end;
        if (choice === 'point'){
            start = startPoint;
            end = endPoint;
        }else{
            start = new google.maps.LatLng(pointMarkerStart.lat, pointMarkerStart.lng);
            end = new google.maps.LatLng(pointMarkerEnd.lat, pointMarkerEnd.lng);
        }

        DirectionsService.route({
            origin: start,
            destination: end,
            travelMode: google.maps.TravelMode.TRANSIT
        }, (response, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
                const coords = response.routes[0].overview_path;
                let point;
                this.setCoords(coords);
                this.setState({routes: response.routes[0]});
                point = {lat: coords[0].lat(), lng: coords[0].lng()};
                this.setPointMarkerStart(point);
                point = {lat: coords[coords.length - 1].lat(), lng: coords[coords.length - 1].lng()};
                this.setPointMarkerEnd(point);
                this.setChoice(choice);
                this.openRouteResult();
            } else {
                this.setError('Неможливо прокласти маршрут.');
            }
        });
    };

    openRouteResult = () =>{
        this.setState({
            openResultForm: true
        });
    };

    closeRouteResult = () =>{
        this.setState({
            openResultForm: false
        });
    };

    render() {
        const {pointMarkerStart, pointMarkerEnd, coordsWay, error, openResultForm, choice} = this.state;
        let isHomeOpen = window.location.href.includes('home');
        return (
            <Map
                google={this.props.google}
                zoom={14}
                className='map'
                initialCenter={{
                    lat: 49.84,
                    lng: 24.028667
                }}
                onClick={this.onMapClicked}
            >
                {isHomeOpen &&
                <StartBtn
                    getCoordsWay={this.getCoordsWay}
                    setEndPoint={this.setEndPoint}
                    setStartPoint={this.setStartPoint}
                    pointMarkerStart={pointMarkerStart}
                    pointMarkerEnd={pointMarkerEnd}
                    choice={choice}
                    convertToAddress={this.convertToAddress}
                    setChoice={this.setChoice}
                />
                }
                <Marker
                    draggable = {true}
                    onClick={this.onMarkerClick}
                    title = { 'Кінцева точка' }
                    name={2}
                    onDragend={(t, map, coord) => this.onMarkerDrag(coord, 2)}
                    position = {pointMarkerEnd}
                />
                <Marker
                    draggable = {true}
                    onClick={this.onMarkerClick}
                    title = { 'Початкова точка' }
                    name={1}
                    onDragend={(t, map, coord) => this.onMarkerDrag(coord, 1)}
                    position = {pointMarkerStart}
                />
                <InfoWindow
                    marker={this.state.activeMarker}
                    visible={this.state.showingInfoWindow}>
                    <p>{this.state.selectedPlace}</p>
                </InfoWindow>

                {coordsWay && (
                    <Polyline
                        path={coordsWay}
                        geodesic={false}
                        options={{
                            strokeColor: '#332fb4',
                            strokeOpacity: 0.8,
                            strokeWeight: 10,
                        }}
                    />
                )}
                { openResultForm && <ResultForm routes={this.state.routes} onClose={this.closeRouteResult}/>}
                { error && <CustomizedSnackbars message={error} reset={this.setError}/>}
            </Map>
        );
    }
}

export default GoogleApiWrapper({

    apiKey: GOOGLE_MAP_API
})(MapContainer);
