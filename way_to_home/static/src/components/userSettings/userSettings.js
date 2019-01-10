import React, {Component} from 'react';
import Header from "../header/header";
import SimpleTabs from "../userSettingsForm/userSettingsForm"

export default class UserSettings extends Component{
    render(){
        return(
            <div>
                <Header/>
                <SimpleTabs/>
            </div>
        )
    }
}
