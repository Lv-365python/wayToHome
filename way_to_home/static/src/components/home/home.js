import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import StartBtn from '../startBtn/startBtn';
import Header from "../header/header";

class Home extends Component {
    render(){
        return(
            <div>
                <Header/>
                <StartBtn/>
            </div>
        )
    }
}

export default withRouter(Home);