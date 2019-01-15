import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Avatar from '@material-ui/core/Avatar';

import LoginBtn from '../loginBtn/loginBtn.js';
import './header.css'
import StartBtn from "../startBtn/startBtn.js";
import UserIcon from './usericon.js'

const style = {
    height: '44px',
    background: '#4887c1cc',
    borderRadius: 5,
    avatar: {
        margin: 10,
    },
};

class Header extends Component{
    render(){
        return(
            <div>
            <AppBar style={style} position="static">
            <Toolbar>
                <StartBtn/>
                <LoginBtn/>
                <Avatar />
                 <Avatar
                     alt="user icon"
                     src="https://lh3.googleusercontent.com/-xYbOPGo_nDM/AAAAAAAAAAI/AAAAAAAAAPY/EQgQkBZ-_D0/photo.jpg"
                     className={style.avatar}
                 />
            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default Header;
