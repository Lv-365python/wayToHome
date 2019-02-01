import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, Polyline } from 'google-maps-react';
import { GOOGLE_MAP_API } from "src/settings"
import { CustomizedSnackbars } from '../index';
import './map.css'
import { StartBtn } from '.';

export class MapContainer extends Component {

    state = {
        startPoint: undefined,
        endPoint: undefined,
        coordsWay: undefined,
        map: undefined,
        error: undefined,
        pointMarkerStart: {lat: 49.84, lng: 24.028667 },
        pointMarkerEnd: {lat: 49.84, lng: 24.028667 }
    };

    onMarkerClick = () => {
        console.log()
    };

    setStartPoint = (start) => {
        this.setState({
            startPoint: start,
        });
    };

    setEndPoint = (end) => {
        this.setState({ endPoint: end,
        });
    };

    setError = (error) => {
        this.setState({
            error: error,
        });
    };

    setCoords = (coords) => {
        this.setState({
            coordsWay: coords,
        });
    };

    getCoordsWay = () => {
        const {startPoint, endPoint} = this.state;
        const DirectionsService = new google.maps.DirectionsService();
        DirectionsService.route({
            origin: startPoint,
            destination: endPoint,
            travelMode: google.maps.TravelMode.TRANSIT
        }, (response, status) => {
            if (status === google.maps.DirectionsStatus.OK) {
                const coords = response.routes[0].overview_path;
                this.setCoords(coords);
            } else {
                this.setError('Неможливо прокласти маршрут.');
            }
        });
    };

    render() {
        const {pointMarkerStart, pointMarkerEnd, coordsWay, error} = this.state;
        let startPointCoords = undefined;
        let endPointCoords = undefined;
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
                <StartBtn getCoordsWay={this.getCoordsWay} setEndPoint={this.setEndPoint} setStartPoint={this.setStartPoint}/>
                <Marker
                    onClick = { this.onMarkerClick }
                    draggable = {true}
                    title = { 'Початкова точка' }
                    position = {startPointCoords || pointMarkerStart}
                    name = { 'Точка А' }
                />
                <Marker
                    onClick = { this.onMarkerClick }
                    draggable = {true}
                    title = { 'Кінцева точка' }
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
                { error && <CustomizedSnackbars message={error} reset={this.setError}/>}
            </Map>
        );
    }
}

export default GoogleApiWrapper({

    apiKey: GOOGLE_MAP_API
})(MapContainer);
