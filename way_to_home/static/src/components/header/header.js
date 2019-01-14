import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';

import LoginBtn from '../loginBtn/loginBtn.js';
import './header.css'
import StartBtn from "../startBtn/startBtn.js";

const style = {
    height: '44px',
    background: '#4887c1cc',
    borderRadius: 5,
}

class Header extends Component{
    render(){
        return(
            <div>
            <AppBar style={style} position="static">
            <Toolbar>
                <StartBtn/>
                <LoginBtn/>
                <AccountCircle style={{fontSize: '40px'}}/>
            </Toolbar>
            </AppBar>
            </div>
        )
    }
}

export default Header
