import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Avatar from '@material-ui/core/Avatar';
import ToggleDisplay from 'react-toggle-display';

import LoginBtn from '../loginBtn/loginBtn.js';
import StartBtn from '../startBtn/startBtn.js';
import MenuButton from './menuButton/menuButton.js';
import './header.css'

const style = {
    top: '0.5%',
    height: '7%',
    background: '#4887c1cc',
    borderRadius: 5,
};

class Header extends Component {

    state = {
        show: true,
    };

    isLoggined = () => {
//        return document.cookie.indexOf('sessionid') !== -1;
        return true;
    };

    render(){
        return(
            <div>
            <AppBar style={style}>
            <Toolbar>

                <div className='Title' onClick={() => this.props.history.push('/home')}>
                    <p>WayToHome</p>
                </div>

                <ToggleDisplay show={!this.isLoggined()}>
                    <LoginBtn />
                </ToggleDisplay>

                <ToggleDisplay show={this.isLoggined()}>
                    <AccountCircle className='AvatarDiv' style={{fontSize: '40px'}} />
                    <MenuButton />
                </ToggleDisplay>

            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default withRouter(Header);
