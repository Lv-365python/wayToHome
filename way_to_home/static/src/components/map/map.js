import React, { Component } from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';
import { GOOGLE_MAP_API } from "src/settings"
import './map.css'


export class MapContainer extends Component {
    render() {
        return (
            <div className='map'>
                <Map
                    google={this.props.google}
                    zoom={14}
                    initialCenter={{
                        lat: 49.84,
                        lng: 24.028667
                    }}
                />
            </div>
        );
    }
}

export default GoogleApiWrapper({

    apiKey: GOOGLE_MAP_API
})(MapContainer);
