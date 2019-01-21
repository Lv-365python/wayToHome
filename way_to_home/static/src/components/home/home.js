import React, {Component} from 'react';
import StartBtn from '../startBtn/startBtn';
import Header from "../header/header";
import UserSettingsForm from "../userSettingsForm/userSettingsForm"

export default class Home extends Component{
    render(){
        return(
            <div>
                <Header/>
                <UserSettingsForm/>
            </div>
        )
    }
}
