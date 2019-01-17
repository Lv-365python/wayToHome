import React from 'react';
import {withRouter} from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

import WayTab from './wayTab/wayTab';
import './userSettingsForm.css';


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
                    <Tabs value={value} onChange={this.handleChange} centered >
                        <Tab label="Профіль" className="settingsTab" />
                        <Tab label="Шляхи" className="settingsTab" />
                    </Tabs>
                </AppBar>

                {value === 0 && <div>TODO: user profile tab</div>}
                {value === 1 && <WayTab/>}
            </div>
        );
    }
}

export default withRouter(UserSettingsForm);
