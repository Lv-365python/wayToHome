import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import {withRouter} from 'react-router-dom';

import './menuButton.css'


class MenuButton extends Component{
    state = {
        anchorEl: null,
    };

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
  };

  logOut = () => {
    this.setState({ anchorEl: null });
    // TODO: loguot function
  };

  toSettings = () => {
    this.setState({ anchorEl: null });
    this.props.history.push('/settings');
  }

  toHome = () => {
    this.setState({ anchorEl: null });
    this.props.history.push('/home');
  }

    render(){
        const {anchorEl} = this.state;
        return(
            <div className='MenuButtonDiv'>
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
                    <MenuItem onClick={this.toHome}>На головну</MenuItem>
                    <MenuItem onClick={this.toSettings}>Налаштування</MenuItem>
                    <MenuItem onClick={this.logOut}>Вийти</MenuItem>
                </Menu>
            </div>
        )
    }
}

export default withRouter(MenuButton);
