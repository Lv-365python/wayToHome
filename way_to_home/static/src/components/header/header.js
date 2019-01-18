import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Cookies } from 'react-cookie';
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

    static propTypes = {
//        cookies: instanceOf(Cookies).isRequired,
    };

    state = {
        show: true,
//        image: cookies.get('picture'),
        image: 'https://lh3.googleusercontent.com/-xYbOPGo_nDM/AAAAAAAAAAI/AAAAAAAAAPY/EQgQkBZ-_D0/photo.jpg',
    };

    isLoggined = () => {
        return true;
//        return document.cookie.indexOf('sessionid') !== -1;
    };

    render(){
        return(
            <div>
            <AppBar style={style} position='static'>
            <Toolbar>

                <div className='Title'> Way to home </div>

                <ToggleDisplay show={!this.isLoggined()}>
                    <LoginBtn />
                    <AccountCircle className='AvatarDiv' style={{fontSize: '40px'}} />
                </ToggleDisplay>

                <ToggleDisplay show={this.isLoggined()}>
                    <div className='AvatarDiv'>
                        <Avatar
                            alt='user icon'
                            src={this.state.image}
                        />
                    </div>
                    <SettingsButton/>
                </ToggleDisplay>

            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default Header;
