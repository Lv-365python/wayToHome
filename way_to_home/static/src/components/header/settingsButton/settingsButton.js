import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';

import './settingsButton.css'


class SettingsButton extends Component{
    state = {
        anchorEl: null,
    };

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
  };

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
                    <MenuItem onClick={this.handleClose}>Мої маршрути</MenuItem>
                    <MenuItem onClick={this.handleClose}>Мої місця</MenuItem>
                    <MenuItem onClick={this.handleClose}>Сповіщення</MenuItem>
                    <MenuItem onClick={this.handleClose}>Вийти</MenuItem>
                </Menu>
            </div>
        )
    }
}

export default SettingsButton;
