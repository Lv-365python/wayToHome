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
    open: true,
  };

    onClickCancel = () => {
        this.closeLoginForm();
        this.openStartBtn();
        this.openLogInBtn();
        this.setState({ open: false });
    }
    onClickSignUp = () => {
        this.closeLoginForm();
        this.openSignupForm();
    }

//    closeLoginForm = () => {
//        document.getElementsByClassName('LoginFormDiv')[0].style.display = 'none'
//    }
//    openStartBtn = () => {
//        document.getElementsByClassName('StartBtnDiv')[0].style.display = 'block'
//    }
//    openSignupForm = () => {
//        document.getElementsByClassName('SignupFormDiv')[0].style.display = 'block'
//    }
//    closeLoginBtn = () => {
//        document.getElementsByClassName('LoginBtnDiv')[0].style.display = 'none'
//    }
//    openLogInBtn = () => {
//        document.getElementsByClassName('LogInBtnDiv')[0].style.display = 'block'
//    }

    render(){
        return(
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

              <div><Button color="primary" onClick={this.onClickSignUp}> sign up </Button></div>

              <Button variant='contained' color='primary' size='medium'> confirm </Button>

              <Button
                  variant='contained'
                  color='secondary'
                  size='medium'
                  className='Btn'
                  onClick={this.onClickCancel}>
                cancel
              </Button>

          </div>

        )
    }
};

export default LoginForm