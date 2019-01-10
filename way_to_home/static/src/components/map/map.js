import React, { Component } from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';
import './map.css'

export class MapContainer extends Component {
    render() {
        return (
            <Map
                google={this.props.google}
                zoom={14}
                className='map'
                initialCenter={{
                    lat: 49.8330602,
                    lng: 23.9969029
                }}
            />
        );
    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyAQ8U2CGzOX4p9G_0Qn7fASEbbnW8XeIyA'
})(MapContainer);
