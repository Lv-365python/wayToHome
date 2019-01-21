
import React, {Component} from 'react';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';
import * as L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import 'leaflet/dist/leaflet.css';
import './map.css';


let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});


export default class MapLeaflet extends Component {

    state = {
        lat: 49.84,
        lng: 24.028667,
    };

    render() {
        const position = [this.state.lat, this.state.lng];
        return (
            <div className="map">
                <Map
                    center={position}
                    zoom={13}
                    maxZoom={20}
                    attributionControl={true}
                    zoomControl={true}
                    doubleClickZoom={true}
                    scrollWheelZoom={true}
                    dragging={true}
                    animate={true}
                    easeLinearity={0.35}
                >
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    <Marker position={position} draggable={true} icon={DefaultIcon}>
                        <Popup>
                            Початкова точка
                        </Popup>
                    </Marker>
                    <Marker position={position} draggable={true} icon={DefaultIcon}>
                        <Popup>
                            Кінцева точка
                        </Popup>
                    </Marker>
                </Map>
            </div>
        )
    }
}
