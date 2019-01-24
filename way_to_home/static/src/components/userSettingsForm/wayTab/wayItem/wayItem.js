import React, {Component} from 'react';

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
import './wayItem.css';


export default class WayItem extends Component{

    state = {
        startPlace: {},
        endPlace: {},
        startPlaceName: 'PlaceA',
        endPlaceName: 'PlaceB',
        notificationOpen: false,
        deleteAlertOpen: false,
    };

    getData = () => {
        let routes = this.props.way.routes;
        let startRoute = routes.find(x => x.position === 0);
        let endRoute = routes.find(x => x.position === routes.length-1);

        let startPlace = this.props.places.find(x => x.id === startRoute.start_place);
        let endPlace = this.props.places.find(x => x.id === endRoute.end_place);

        this.setState({
            startPlace: startPlace,
            endPlace: endPlace
        });
    };

    componentWillMount() {
        this.getData();
    };

    handleOpenNotification = () => {
        this.setState({
            notificationOpen: true
        })
    };

    handleCloseNotification = () => {
        this.setState({
            notificationOpen: false
        })
    };

    handleOpenDeleteAlert = () => {
        this.setState({
            deleteAlertOpen: true
        })
    };

    handleCloseDeleteAlert = () => {
        this.setState({
            deleteAlertOpen: false
        })
    };

    render(){
        return(
            <div className="wayItem">
               <Chip
                   className="textField"
                   color="primary"
                   onMouseEnter={() => this.setState({startPlaceName: this.state.startPlace.address})}
                   onMouseLeave={() => this.setState({startPlaceName: this.state.startPlace.name})}
                   icon={<PlaceIcon />}
                   label={this.state.startPlaceName}
                   variant="outlined"
               />

               <TrendingFlat className="arrow" />
               <Chip
                   className="textField"
                   color="primary"
                   onMouseEnter={() => this.setState({endPlaceName: this.state.endPlace.address})}
                   onMouseLeave={() => this.setState({endPlaceName: this.state.endPlace.name})}
                   icon={<PlaceIcon color="secondary"/>}
                   label={this.state.endPlaceName}
                   variant="outlined"
               />


               <Tooltip title="Нотифікації">
                   <IconButton color="primary" aria-label="Нотифікації" onClick={this.handleOpenNotification}>
                       <NotificationIcon />
                   </IconButton>
               </Tooltip>
                <Tooltip title="Видалити">
                    <IconButton color="secondary" aria-label="Видалити" onClick={this.handleOpenDeleteAlert}>
                        <DeleteIcon />
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
                            Ви впевнені, що хочете видалити шлях? Також будуть видалені збережені нотифікації для вибраного шляху.
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button
                            onClick={this.handleCloseDeleteAlert}
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
        )
    }
}
