import React, {Component} from 'react';
import axios from "axios";

import TrendingFlat from '@material-ui/icons/TrendingFlat';
import Chip from '@material-ui/core/Chip';
import IconButton from '@material-ui/core/IconButton';
import NotificationIcon from '@material-ui/icons/NotificationsActive';
import PlaceIcon from '@material-ui/icons/Place';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import NotificationForm from "src/components/userSettingsForm/notifications/notificationForm";
import './wayItem.css';


const url = "/api/v1/place/";

export default class WayItem extends Component{

    state = {
        startPlace: {},
        endPlace: {},
        startPlaceName: 'PlaceA',
        endPlaceName: 'PlaceB',
        deleteAlertOpen: false,
        isWayFormOpen: true,
        isNotificationFormOpen: false,
        phone_number: undefined,
    };

    getData = () => {
        let routes = this.props.way.routes;
        let startRoute = routes.find(x => x.position === 0);
        let endRoute = routes.find(x => x.position === routes.length-1);

        let startPlace = undefined;
        let endPlace = undefined;

        axios.get(url + startRoute.start_place)
            .then(response => {
                startPlace = response.data;
                this.setState({
                    startPlace: startPlace,
                    startPlaceName: startPlace.name,
                });
            })
            .catch(error => this.props.setError("Не вдалося завантажити місце"));

        axios.get(url + endRoute.end_place)
            .then(response => {
                endPlace = response.data;
                this.setState({
                    endPlace: endPlace,
                    endPlaceName: endPlace.name,
                });
            })
            .catch(error => this.props.setError("Не вдалося завантажити місце"));

        axios.get('/api/v1/user/')
            .then(response => {
                this.setState({
                    phone_number: response.data.phone_number,
                });
            })
            .catch(error => this.props.setError("Не вдалося завантажити номер телефону"));
    };

    componentWillMount() {
        this.getData();
    };

    toggleNotificationForm = () => {
        if (this.state.phone_number === ""){
            this.props.setError("Спочатку введіть номер телефону")
        } else {
            this.setState(state => ({
                isNotificationFormOpen: !state.isNotificationFormOpen,
                isWayFormOpen: !state.isWayFormOpen
            }));
        }
    };

    toggleDeleteAlert = () => {
        this.setState(state => ({
            deleteAlertOpen: !state.deleteAlertOpen
        }));
    };

    render(){

        let { startPlaceName, endPlaceName, startPlace, endPlace } = this.state;
        return(
            <div>
                {
                    this.state.isWayFormOpen &&
                    <div className="wayItem">
                        <Chip
                            className="textField"
                            color="primary"
                            onMouseEnter={() => this.setState({startPlaceName: startPlace.address})}
                            onMouseLeave={() => this.setState({startPlaceName: startPlace.name})}
                            icon={<PlaceIcon/>}
                            label={startPlaceName === '' ? startPlace.address : startPlaceName}
                            variant="outlined"
                        />

                        <TrendingFlat className="arrow"/>
                        <Chip
                            className="textField"
                            color="primary"
                            onMouseEnter={() => this.setState({endPlaceName: endPlace.address})}
                            onMouseLeave={() => this.setState({endPlaceName: endPlace.name})}
                            icon={<PlaceIcon color="secondary"/>}
                            label={this.state.endPlaceName === '' ? endPlace.address : endPlaceName}
                            variant="outlined"
                        />


                        <Tooltip title="Нотифікації">
                            <IconButton color="primary"
                                        aria-label="Нотифікації"
                                        onClick={this.toggleNotificationForm}>
                                <NotificationIcon/>
                            </IconButton>
                        </Tooltip>
                        <Tooltip title="Видалити">
                            <IconButton color="secondary" aria-label="Видалити" onClick={this.toggleDeleteAlert}>
                                <DeleteIcon/>
                            </IconButton>
                        </Tooltip>


                        <Dialog
                            open={this.state.deleteAlertOpen}
                            aria-labelledby="alert-dialog-title"
                            aria-describedby="alert-dialog-description"
                        >
                            <DialogTitle id="alert-dialog-title">{"Видалити шлях ?"}</DialogTitle>
                            <DialogContent>
                                <DialogContentText id="alert-dialog-description">
                                    Ви впевнені що хочете видалити шлях? Також будуть видалені збережені нотифікації для
                                    вибраного шляху.
                                </DialogContentText>
                            </DialogContent>
                            <DialogActions>
                                <Button
                                    onClick={this.toggleDeleteAlert}
                                    variant="outlined"
                                    color="primary"
                                >
                                    Скасувати
                                </Button>
                                <Button
                                    onClick={() => this.props.deleteButton(this.props.way.id)}
                                    variant="outlined"
                                    color="primary"
                                    autoFocus
                                >
                                    Видалити
                                </Button>
                            </DialogActions>
                        </Dialog>
                    </div>
                }
                {
                    this.state.isNotificationFormOpen &&
                    <div>
                        <NotificationForm way={this.props.way} toggleNotificationForm={this.toggleNotificationForm}/>
                    </div>
                }
            </div>
        )
    }
}
