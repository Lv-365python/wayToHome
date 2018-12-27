import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import LockIcon from '@material-ui/icons/LockOutlined';
import Avatar from '@material-ui/core/Avatar';
import Modal from '@material-ui/core/Modal';
import './loginForm.css';
import SignupForm from '../signupForm/signupForm';


class LoginForm extends Component{

    state = {
        open: false
    };

    onClickSignup = () => {
        this.setState({ open: false });
        this.refs.child.signupFormOpen();  // ????????
        console.log('click on sign up button');
    };

    onClickConfirm = () => {
        console.log('click on confirm button');
    };

    loginFormOpen = () => {
        this.setState({ open: true });
        console.log('login form is open');
    };

    loginFormClose = () => {
        this.setState({ open: false });
        console.log('login form is close');
    };

    render(){
        return(
        <Modal open={this.state.open} onClose={this.loginFormClose}>
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
              <div>
                <FormControlLabel control={<Checkbox value="checkedC" />} label="Remember me" />
              </div>
              <div>
                  <Button color="primary" onClick={this.onClickSignup}>
                    sign up
                  </Button>
              </div>
              <Button variant='contained' color='primary' size='medium' onClick={this.onClickConfirm}>
                confirm
              </Button>
              <Button
                  variant='contained'
                  color='secondary'
                  size='medium'
                  className='Btn'
                  onClick={this.loginFormClose}>
                cancel
              </Button>
          </div>
        </Modal>
        )
    };
};

export default LoginForm
