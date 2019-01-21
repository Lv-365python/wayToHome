import React, {Component} from 'react';
import withRouter from "react-router-dom/withRouter";
import Button from "@material-ui/core/Button";
import KeyboardBackspace from "@material-ui/icons/KeyboardBackspace";

import UserSettingsForm from "../userSettingsForm/userSettingsForm";
import './userSettings.css';


class UserSettings extends Component{

    render(){
        return(
            <div>
                <UserSettingsForm />
                <div className='settingsComeBack'>
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={() => this.props.history.push('/home')}
                    >
                        <KeyboardBackspace />ПОВЕРНУТИСЬ
                    </Button>
                </div>
            </div>
        )
    }
}

export default withRouter(UserSettings);
