import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
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

class Header extends Component{

    state = {
        show: true,
    };

    toggle = () => {
        this.setState({show: !this.state.show});
    };

    render(){
        return(
            <div>
            <AppBar style={style} position='static'>
            <Toolbar>
                <div className='Title'>
                    <font size='6'
                        color='#2a218c'
                    >
                       WAY TO HOME
                    </font>
                </div>
                <StartBtn />

                <ToggleDisplay show={this.state.show}>
                    <LoginBtn />
                    <AccountCircle className='AvatarDiv' style={{fontSize: '40px'}} />
                </ToggleDisplay>

                <ToggleDisplay show={!this.state.show}>
                    <div className='AvatarDiv'>
                        <Avatar
                            alt='user icon'
                            src='https://lh3.googleusercontent.com/-xYbOPGo_nDM/AAAAAAAAAAI/AAAAAAAAAPY/EQgQkBZ-_D0/photo.jpg'
                        />
                    </div>
                    <SettingsButton/>
                </ToggleDisplay>

                <Button
                    style={{top: '25%'}}
                    color='secondary'
                    variant='contained'
                    size='small'
                    onClick={this.toggle}
                >
                   toggle
                </Button>

            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default Header;
