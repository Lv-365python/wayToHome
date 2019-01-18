import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import {withRouter} from 'react-router-dom';

import './settingsButton.css'


class SettingsButton extends Component{
    state = {
        anchorEl: null,
    };

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  logOut = () => {
    this.setState({ anchorEl: null });
    // TODO: loguot function
  };

  redirectToSettings = () => {
    this.setState({ anchorEl: null });
    this.props.history.push('/settings');
  }

    render(){
        const {anchorEl} = this.state;
        return(
            <div className='SettingsButtonDiv'>
                <Button
                    variant="contained"
                    color='primary'
                    size='large'
                    aria-owns={anchorEl ? 'simple-menu' : undefined}
                    aria-haspopup="true"
                    onClick={this.handleClick}
                >
                   Меню
                </Button>
                <Menu
                    id="simple-menu"
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={this.handleClose}
                >
                    <MenuItem onClick={this.redirectToSettings}>Налаштування</MenuItem>
                    <MenuItem onClick={this.logOut}>Вийти</MenuItem>
                </Menu>
            </div>
        )
    }
}

export default withRouter(SettingsButton);
