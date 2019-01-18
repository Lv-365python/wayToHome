import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import {Button} from "@material-ui/core";
import KeyboardBackspace from "@material-ui/icons/KeyboardBackspace";

import UserSettingsForm from "../userSettingsForm/userSettingsForm";
import './userSettings.css';


class UserSettings extends Component{

    render(){
        return(
            <div>
                <div className='settingsComeBack'>
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={() => this.props.history.push('/home')}
                    >
                        <KeyboardBackspace></KeyboardBackspace>ПОВЕРНУТИСЬ
                    </Button>
                </div>

                <UserSettingsForm />
            </div>
        )
    }
}

export default withRouter(UserSettings);
