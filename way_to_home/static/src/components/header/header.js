import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Avatar from '@material-ui/core/Avatar';
import ToggleDisplay from 'react-toggle-display';
import Cookies from 'js-cookie';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import axios from 'axios';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import IconButton from '@material-ui/core/IconButton';

import LoginBtn from '../loginBtn/loginBtn.js';
import {isAuthenticated} from '../../main_router';
import './header.css';


const style = {
    height: '40px',
    background: '#5c85d6',
};

class Header extends Component {

    state = {
        show: true,
        anchorEl: null,
    };

    isLoggined = () => {
        return isAuthenticated();
    };

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
  };

  logOut = () => {
    this.setState({ anchorEl: null });
    Cookies.remove('picture');

    axios.get('/api/v1/user/logout')
        .then(() => {
            this.props.history.go(0)
        })
  };

  toSettings = () => {
    this.setState({ anchorEl: null });
    this.props.history.push('/profile');
  }

  toHome = () => {
    this.setState({ anchorEl: null });
    this.props.history.push('/home');
  }

    render(){
        const {anchorEl} = this.state;
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
                    <div onClick={this.handleClick} className='Menu'>
                        <div>
                        {
                            Cookies.get('picture')
                            ?
                            <Avatar alt="avatar" src={Cookies.get('picture')} style={{position: 'fixed'}} className='Avatar' />
                            :
                            <AccountCircle style={{fontSize: '40px'}} className='Avatar' />
                        }
                        </div>

                        <div className='moreVertIcon'>
                          <MoreVertIcon />
                        </div>

                    </div>


                    <Menu
                        anchorEl={anchorEl}
                        open={Boolean(anchorEl)}
                        onClose={this.handleClose}
                    >
                        <MenuItem onClick={this.toHome}>На головну</MenuItem>
                        <MenuItem onClick={this.toSettings}>Налаштування</MenuItem>
                        <MenuItem onClick={this.logOut}>Вийти</MenuItem>
                    </Menu>
                </ToggleDisplay>

            </Toolbar>
            </AppBar>
            </div>
        )
    }
};

export default withRouter(Header);
