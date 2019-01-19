import React, {Component} from 'react';
import axios from "axios";

import TrendingFlat from '@material-ui/icons/TrendingFlat';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Dialog from '@material-ui/core/Dialog';
import CircularProgress from '@material-ui/core/CircularProgress';

import ModalMap from '../modalMap';
import './newWayItem.css';

const url = 'http://127.0.0.1:8000/api/v1/';


export default class NewWayItem extends Component{

    state = {
        placeA: 'Виберіть місце A',
        placeB: 'Виберіть місце Б',
        mapOpen: false,
        loading: false,
        routes: []
    };

    handleClickModalOpen = async () => {
        this.setState({loading:true});

        let today = new Date();
        let tomorrow = new Date(today.getTime() + (24 * 60 * 60 * 1000)).toISOString();
        const APP_ID = "ctrJV3imNpgpWu5urnAa";
        const APP_CODE = "4lPfKEUtIyz_PXCcimqv2w";
        const testUrl = `https://transit.api.here.com/v3/route.json?dep=49.8073074%2C23.982835&arr=49.8334453%2C23.9930059&time=${tomorrow}&app_id=${APP_ID}&app_code=${APP_CODE}&routing=tt`;

         await axios.get(testUrl)
            .then(response => {
                console.log(response);
                let listRoutes = response.data.Res.Connections.Connection;

                this.setState({
                    routes: listRoutes,
                    mapOpen: true,
                });
            })
            .catch(error => {
                console.log(error)
            });

         this.setState({loading:false})
    };

    handleModalClose = () => {
        this.setState({ mapOpen: false });
    };

    newWayValidator(){
        if (this.state.placeA === this.state.placeB) {
            return false
        }

        if (!Number.isInteger(this.state.placeA) || !Number.isInteger(this.state.placeB)){
            return false
        }
        return true
    }

     handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
         });
     };

    saveButton = route => {
        this.setState({loading:false});
        this.props.saveRoute(this.state.placeA, this.state.placeB, route);
        this.setState({loading:false})
    };

    render() {
        const { places } = this.props;

        return (
            <div className="newWayItem">
                <TextField
                  select
                  className="textField"
                  label="Місце А"
                  value={this.state.placeA}
                  onChange={this.handleChange('placeA')}
                  helperText="Виберіть одне з Ваших збережених місць"
                  margin="normal"
                >
                  {places.map(place => (
                    <MenuItem key={place.id} value={place.id}>
                      {place.name}
                    </MenuItem>
                  ))}
                </TextField>

                <TrendingFlat className="arrow" />

                <TextField
                  select
                  className="textField"
                  label="Місце Б"
                  value={this.state.placeB}
                  onChange={this.handleChange('placeB')}
                  helperText="Виберіть одне з Ваших збережених місць"
                  margin="normal"
                >
                  {places.map(place => (
                    <MenuItem key={place.id} value={place.id}>
                      {place.name}
                    </MenuItem>
                  ))}
                </TextField>

                <Tooltip title="Вибрати маршрут">
                    <IconButton
                        style={this.newWayValidator()?{color: "green"}:{color: "grey"}}
                        disabled={!this.newWayValidator()}
                        aria-label="Зберегти"
                        onClick={this.handleClickModalOpen}
                    >
                        <SaveAlt />
                    </IconButton>
                </Tooltip>

                <Tooltip title="Видалити">
                    <IconButton
                        color="secondary"
                        aria-label="Видалити"
                        onClick={this.props.deleteButton}
                    >
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>

                <Dialog open={this.state.mapOpen} >
                    <ModalMap
                        onClose={this.handleModalClose}
                        routes={this.state.routes}
                        saveRoute={this.saveButton}
                    />
                </Dialog>

                {this.state.loading && <CircularProgress size={64} className="buttonProgress"/>}

            </div>
        )
    }
}
