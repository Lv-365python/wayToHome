import React, {Component} from 'react';
import {Button} from "@material-ui/core";
import axios from "axios";

import UserSettingsForm from "../userSettingsForm/userSettingsForm";
import './userSettings.css';


export default class UserSettings extends Component{

    render(){
        return(
            <div>
                <div className='settingsComeBack'>
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={() => this.props.history.push('/home')}
                    >← ПОВЕРНУТИСЬ
                    </Button>
                </div>

                <UserSettingsForm />
            </div>
        )
    }
}
