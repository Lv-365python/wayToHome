import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import './userSettingsForm.css';
import {Link} from 'react-router-dom'

class userSettingsForm extends React.Component {
    state = {
        value: 0,
    };

    handleChange = (event, value) => {
        this.setState({ value });
    };

    routeChange = () => {
        window.location.reload('/home')
    }

    render() {
        const { value } = this.state;

        return (
            <div className="settingsForm">
                <div className='settingsComeBack'>
                    <Link to="/home" className='settingsLink'>← ПОВЕРНУТИСЬ</Link>
                </div>
                <AppBar position="static">
                    <Tabs value={value} onChange={this.handleChange}>
                        <Tab label="Профіль" className="settingsTab" />
                        <Tab label="Шляхи" className="settingsTab" />
                    </Tabs>
                </AppBar>
                {value === 0 && <div>asdasdas</div>}
                {value === 1 && <div>vbbcbbcccv</div>}
            </div>
        );
    }
}



export default userSettingsForm;
