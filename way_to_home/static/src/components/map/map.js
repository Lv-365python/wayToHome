import React, { Component } from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';
import GOOGLE_MAP_API from "src/settings"
import './map.css'

export class MapContainer extends Component {
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
            />
        );
    }
}

export default GoogleApiWrapper({

    apiKey: GOOGLE_MAP_API
})(MapContainer);
