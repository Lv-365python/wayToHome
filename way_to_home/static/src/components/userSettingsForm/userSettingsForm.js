import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PropTypes from 'prop-types';
import ClickAwayListener from '@material-ui/core/ClickAwayListener';
import {withRouter} from 'react-router-dom';

import ProfileTab from './profileTab/profileTab'
import WayTab from './wayTab/wayTab';
import PlaceTab from './placeTab/placeTab';
import './userSettingsForm.css';


class UserSettingsForm extends React.Component {
    state = {
        value: 0,
    };

    handleChange = (event, value) => {
        this.setState({ value });
    };

    handleClickAway = () => {
        this.props.history.push('/home');
    };

    render() {
        const { value } = this.state;

        return (
            <div className="settingsForm">
            <ClickAwayListener onClickAway={this.handleClickAway}>
            <div>
                <AppBar position="static">
                    <Tabs value={value} onChange={this.handleChange} centered >
                        <Tab label="Профіль" className="settingsTab" />
                        <Tab label="Місця" className="settingsTab" />
                        <Tab label="Шляхи" className="settingsTab" />
                    </Tabs>
                </AppBar>
                {value === 0 && <ProfileTab/>}
                {value === 1 && <PlaceTab/>}
                {value === 2 && <WayTab/>}
            </div>
            </ClickAwayListener>
            </div>
        );
    }
}

export default withRouter(UserSettingsForm);
