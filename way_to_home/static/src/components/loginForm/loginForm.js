import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import LockIcon from '@material-ui/icons/LockOutlined';
import Avatar from '@material-ui/core/Avatar';
import './loginForm.css';
import LoginBtn from '../loginBtn/loginBtn';
import SignupForm from '../signupForm/signupForm.js';


class LoginForm extends Component{

    state = {
        display: 'block',
    }

    onClickSignup = () => {
        console.log('click on sign up button');
        this.setState({display: 'none'});
        this.setState({open: 'false'});

    };

    onClickConfirm = () => {
        console.log('click on confirm button');
    };

    loginFormOpen = () => {
        console.log('login form is open');
    };

    loginFormClose = () => {
        console.log('login form is close');
        this.setState({display: 'none'});
    };

    render(){
        return(
          <div style={{marginTop: '80px', display: this.state.display}} className='LoginFormDiv'>
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
              <div>
                <FormControlLabel control={<Checkbox value="checkedC" />} label="Remember me" />
              </div>
              <div>
                  <Button color="primary" onClick={this.onClickSignup}>
                    sign up
                  </Button>
              </div>
              <Button variant='contained'
                color='primary'
                size='medium'
                onClick={this.onClickConfirm}>
                    confirm
              </Button>
              <Button
                  variant='contained'
                  color='secondary'
                  size='medium'
                  className='Btn'
                  onClick={this.props.action}>
                    cancel
              </Button>
          </div>
        )
    };
};

export default LoginForm
