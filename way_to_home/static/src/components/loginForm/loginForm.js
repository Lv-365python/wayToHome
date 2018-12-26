import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import LockIcon from '@material-ui/icons/LockOutlined';
import Avatar from '@material-ui/core/Avatar';
import Modal from '@material-ui/core/Modal';
import './loginForm.css'


class LoginForm extends Component{

    state = {
        open: false
    }

    onClickSignup = () => {
        console.log('click on sign up button');
    }

    onClickConfirm = () => {
        console.log('click on confirm button');
    }

    handleClose = () => {
        this.setState({ open: false });
        console.log('login form was closed');
    };

    handleOpen = () => {
        this.setState({ open: true });
        console.log('open handle');
    };

    render(){
        console.log('rendering login form')
        return(
        <Modal open={this.state.open} onClose={this.handleClose}>
          <div style={{marginTop: '80px'}} className='LoginFormDiv'>
              <Avatar>
                <LockIcon />
              </Avatar>
              <TextField
                  id="filled-email-input"
                  label="Email"
                  type="email"
                  name="email"
                  autoComplete="email"
                  margin="normal"
                  variant="filled"/>

              <TextField
                  id="filled-password-input"
                  label="Password"
                  type="password"
                  autoComplete="current-password"
                  margin="normal"
                  variant="filled"/>
              <div><FormControlLabel control={<Checkbox value="checkedC" />} label="Remember me" /></div>

              <div><Button color="primary" onClick={this.onClickSignup}> sign up </Button></div>

              <Button variant='contained' color='primary' size='medium' onClick={this.onClickConfirm}> confirm </Button>

              <Button
                  variant='contained'
                  color='secondary'
                  size='medium'
                  className='Btn'
                  onClick={this.handleClose}>
                cancel
              </Button>
          </div>
        </Modal>
        )
    }
};

export default LoginForm