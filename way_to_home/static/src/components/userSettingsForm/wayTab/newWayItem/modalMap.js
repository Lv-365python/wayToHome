/* global google */
import React from 'react';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { GOOGLE_MAP_API } from "src/settings"


class ModalMap extends React.Component {

    state = {
        map: undefined
    };

    componentWillMount() {
        const { routeInfo } = this.props;
        const colors = ["black", "brown", "green", "purple", "yellow", "blue", "gray", "orange", "red", "white"];
        let google_static_map = "https://maps.googleapis.com/maps/api/staticmap?size=550x400";

        routeInfo.map((info, index) => {
            let rand = colors[Math.floor(Math.random() * colors.length)];
            google_static_map = google_static_map + `&path=color:${rand}|enc:${info.polyline}&markers=size:mid|color:green|label:${index}|${info.end_location.lat()},${info.end_location.lng()}`;
        });

        google_static_map = google_static_map + `&key=${GOOGLE_MAP_API}`;
        this.setState({map: google_static_map})
    }

    render() {
        const { route, saveRoute } = this.props;

        return (
          <div>
              <DialogTitle>Маршрут</DialogTitle>
              <DialogContent>
                  <img src={this.state.map} />
              </DialogContent>
              <DialogActions>

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

export default ModalMap;
