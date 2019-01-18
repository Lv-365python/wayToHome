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
import SettingsButton from './settingsButton/settingsButton.js';
import './header.css'

const style = {
    height: '44px',
    background: '#4887c1cc',
    borderRadius: 5,
    display: 'flex',
};

class Header extends Component {

    state = {
        show: true,
    };

    isLoggined = () => {
        return false;
//        return document.cookie.indexOf('sessionid') !== -1;
    };

    render(){
        return(
            <div>
            <AppBar style={style} position='static'>
            <Toolbar>

                <div className='Title' onClick={() => this.props.history.push('/home')}>
                    Way to home
                </div>

                <ToggleDisplay show={!this.isLoggined()}>
                    <LoginBtn />
                </ToggleDisplay>

                <ToggleDisplay show={this.isLoggined()}>
                    <AccountCircle className='AvatarDiv' style={{fontSize: '40px'}} />
                    <SettingsButton/>
                </ToggleDisplay>

            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default withRouter(Header);