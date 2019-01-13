import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';

import LoginBtn from '../loginBtn/loginBtn.js';
import './header.css'
import StartBtn from "../startBtn/startBtn.js";


class Header extends Component{
    render(){
        return(
            <div>
            <AppBar style={{height: '44px', }} position="static">
            <Toolbar>
            WAY TO HOME
                <StartBtn/>
                <LoginBtn/>
                <AccountCircle style={{fontSize: '40px', top: '10px'}}/>
            </Toolbar>
            </AppBar>
            </div>
        )
    }
}

export default Header
