import React, {Component} from 'react';

import TrendingFlat from '@material-ui/icons/TrendingFlat';
import Chip from '@material-ui/core/Chip';
import IconButton from '@material-ui/core/IconButton';
import SettingsIcon from '@material-ui/icons/Settings';
import PlaceIcon from '@material-ui/icons/Place';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import './wayItem.css';


export default class WayItem extends Component{

    state = {
        startPlace: {},
        endPlace: {},
        notificationOpen: false,
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

    render(){
        return(
            <div className="wayItem">
               <Chip
                   className="textField"
                   color="primary"
                   icon={<PlaceIcon />}
                   label={this.state.startPlace.name}
                   variant="outlined"
               />

                <TrendingFlat className="arrow" />

                <Chip
                    className="textField"
                    color="primary"
                    icon={<PlaceIcon color="secondary"/>}
                    label={this.state.endPlace.name}
                    variant="outlined"
                />


                <Tooltip title="Settings">
                    <IconButton color="primary" aria-label="Нотифікації" onClick={this.handleOpenNotification}>
                         <SettingsIcon />
                    </IconButton>
                </Tooltip>

                <Tooltip title="Delete">
                    <IconButton color="secondary" aria-label="Видалити" onClick={() => this.props.deleteButton(this.props.way.id)}>
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>

            </div>
        )
    }
}
