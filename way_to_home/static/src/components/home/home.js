import React, {Component} from 'react';
import Header from "../header/header";
import GoogleApiWrapper from "../map/map";

export default class Home extends Component{
    render(){
        return(
            <div>
                <Header/>
                <GoogleApiWrapper/>
            </div>
        )
    }
}
