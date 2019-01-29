import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';
import { GOOGLE_MAP_API } from "src/settings"
import './map.css'


export class MapContainer extends Component {

    onMarkerClick = () => {

    };

    render() {
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
                <Marker
                    onClick = { this.onMarkerClick }
                    draggable = {true}
                    title = { 'Changing Colors Garage' }
                    position = {{ lat: 49.84, lng: 24.028667 }}
                    name = { 'Changing Colors Garage' }
                />
                <Marker
                    onClick = { this.onMarkerClick }
                    draggable = {true}
                    title = { 'Changing Colors Garage' }
                    position = {{ lat: 49.84, lng: 24.028667 }}
                    name = { 'Changing Colors Garage' }
                />
            </Map>
        );
    }
}

export default GoogleApiWrapper({

    apiKey: GOOGLE_MAP_API
})(MapContainer);
