import React, {Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';

import LoginBtn from '../loginBtn/loginBtn.js';
import StartBtn from "../startBtn/startBtn.js";
import './header.css'

const style = {
    height: '44px',
    background: '#4887c1cc',
    borderRadius: 5,
    display: 'flex',
};

class Header extends Component{

    state = {
        display: 'none',
    };

    toggle = () => {
        this.setState({display: (this.state.display == 'flex' ? 'none' : 'flex')});
    };

    render(){
        return(
            <div>
            <AppBar style={style} position="static">
            <Toolbar>
                <StartBtn/>
                <LoginBtn/>
                    <AccountCircle
                        className='AvatarDiv'
                        style={{
                            fontSize: '40px',
                            display: (this.state.display == 'flex' ? 'none' : 'flex'),
                        }}
                    />
                    <div className='AvatarDiv'>
                        <Avatar
                            alt="user icon"
                            src="https://lh3.googleusercontent.com/-xYbOPGo_nDM/AAAAAAAAAAI/AAAAAAAAAPY/EQgQkBZ-_D0/photo.jpg"
                            style={{display: this.state.display}}
                        />
                    </div>
                <Button color="secondary"
                    variant='contained'
                    size='small'
                    onClick={this.toggle}
                 >
                        toggle avatar
                </Button>
            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default Header;
