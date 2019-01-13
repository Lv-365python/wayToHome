import React from 'react';
import {withRouter} from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

import PlaceTab from '../placeTab/placeTab';
import './userSettingsForm.css';
import axios from "axios";



class UserSettingsForm extends React.Component {
    state = {
        value: 0,
    };

    handleChange = (event, value) => {
        this.setState({ value });
    };

    render() {
        const { value } = this.state;

        return (
            <div className="settingsForm">

                <AppBar position="static">
                    <Tabs value={value} onChange={this.handleChange}>
                        <Tab label="Профіль" className="settingsTab" />
                        <Tab label="Шляхи" className="settingsTab" />
                    </Tabs>
                </AppBar>

                {value === 0 && <div>vbbcbbcccv</div>}
                {value === 1 && <PlaceTab/>}
            </div>
        );
    }
}

export default withRouter(UserSettingsForm);
