import React, {Component} from 'react';
import Header from "../header/header";
import GoogleApiWrapper from "../map/map";

export default class UserSettings extends Component{
    render(){
        return(
            <div>
                <Header/>
                <h1>USER SETTINGS</h1>
                <GoogleApiWrapper/>
            </div>
        )
    }
}
