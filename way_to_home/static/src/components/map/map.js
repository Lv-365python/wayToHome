import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, Polyline } from 'google-maps-react';
import { GOOGLE_MAP_API } from "src/settings"
import { CustomizedSnackbars } from '../index';
import {ResultForm, StartBtn} from '.';
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
        choice: undefined
    };

    setStartPoint = (start) => {
        this.setState({
            startPoint: start,
        });
        this.setChoice('point');
    };

    setEndPoint = (end) => {
        this.setState({
            endPoint: end,
        });
        this.setChoice('point');
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

    setCoords = (coords) => {
        this.setState({
            coordsWay: coords,
            openResultForm: true
        });
    };

    onMarkerDragStart = (coord) => {
        const { latLng } = coord;
        let pointA = {lat: latLng.lat(), lng: latLng.lng()};
        this.setState({
            pointMarkerStart: pointA,
        });
        this.setChoice('marker');
    };

    onMarkerDragEnd = (coord) => {
        const { latLng } = coord;
        let pointA = {lat: latLng.lat(), lng: latLng.lng()};
        this.setState({
            pointMarkerEnd: pointA,
        });
        this.setChoice('marker');
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
                this.setState({routes: response.routes[0]});
                this.setCoords(coords);
            } else {
                this.setError('Неможливо прокласти маршрут.');
            }
        });
    };

    closeRouteResult = () =>{
        this.setState({
            openResultForm: false
        });
    };

    render() {
        const {pointMarkerStart, pointMarkerEnd, coordsWay, error, openResultForm, choice} = this.state;
        let startPointCoords = undefined;
        let endPointCoords = undefined;
        let isHomeOpen = window.location.href.includes('home');
        if (coordsWay !== undefined){
            startPointCoords = coordsWay[0];
            endPointCoords = coordsWay[coordsWay.length - 1];
        }
        return (
            <Map
                google={this.props.google}
                zoom={14}
                className='map'
                initialCenter={{
                    lat: 49.84,
                    lng: 24.028667
                }}
            >
                {isHomeOpen &&
                    <StartBtn
                          getCoordsWay={this.getCoordsWay}
                          setEndPoint={this.setEndPoint}
                          setStartPoint={this.setStartPoint}
                          pointMarkerStart={pointMarkerStart}
                          pointMarkerEnd={pointMarkerEnd}
                          choice={choice}
                    />
                }

                <Marker
                    draggable = {true}
                    title = { 'Початкова точка' }
                    onDragend={(t, map, coord) => this.onMarkerDragStart(coord)}
                    position = {startPointCoords || pointMarkerStart}
                    name = { 'Точка А' }
                />
                <Marker
                    draggable = {true}
                    title = { 'Кінцева точка' }
                    onDragend={(t, map, coord) => this.onMarkerDragEnd(coord)}
                    position = {endPointCoords || pointMarkerEnd}
                    name = { 'Точка Б' }
                />
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
