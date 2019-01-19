import React, {Component} from 'react';
import UserSettingsForm from "../userSettingsForm/userSettingsForm";
import './userSettings.css';


class UserSettings extends Component{

    render(){
        return(
            <div>
                <UserSettingsForm />
            </div>
        )
    }
}

export default UserSettings;
