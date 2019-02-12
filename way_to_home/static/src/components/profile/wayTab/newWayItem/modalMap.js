/* global google */
import React from 'react';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import './newWayItem.css';
import { GOOGLE_MAP_API } from "src/settings"


export default class ModalMap extends React.Component {

    state = {
        map: undefined,
        time: undefined
    };

    componentWillMount() {
        const { routeInfo } = this.props;
        const colors = ["black", "green", "purple", "blue", "red"];
        let google_static_map = "https://maps.googleapis.com/maps/api/staticmap?size=550x400";
        let duration = 0;

        routeInfo.map((info, index) => {
            duration += info.duration;
            let rand = colors[Math.floor(Math.random() * colors.length)];
            google_static_map = google_static_map + `&path=color:${rand}|enc:${info.polyline}&markers=size:mid|color:green|label:${index}|${info.end_location.lat()},${info.end_location.lng()}`;
        });

        let date = new Date(null);
        date.setSeconds(duration);
        let timeString = date.toISOString().substr(11, 8);

        google_static_map = google_static_map + `&key=${GOOGLE_MAP_API}`;
        this.setState({
            map: google_static_map,
            time: timeString
        })
    }

    render() {
        const { route, saveRoute, routeInfo } = this.props;
        const { time, map } = this.state;

        return (
            <div>
                <DialogTitle>Маршрут</DialogTitle>
                <DialogContent>
                    <img src={map} />
                </DialogContent>

                <DialogActions>
                    <div className="routeInformation">
                    <p className="leftInfoParagraph">Маршрут: <br/>№ { routeInfo.map(route => (route.transit ? `${route.transit} `: false)) }</p>
                    <p className="rightInfoParagraph">Тривалість поїздки: <br/> {time}</p>
                    </div>

                    <Button
                        variant="outlined"
                        style={{color:"green"}}
                        onClick={() => saveRoute(route)}
                    >
                        Вибрати
                    </Button>
                    <Button
                        variant="outlined"
                        color="secondary"
                        onClick={this.props.onClose}
                    >
                        Скасувати
                    </Button>
                </DialogActions>
          </div>
        );
    }
}
