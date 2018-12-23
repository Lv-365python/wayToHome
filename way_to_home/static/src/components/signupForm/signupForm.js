import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import './signupForm.css'


class SignupForm extends Component{

    state = {}

    onClick = () => {
        this.closeSignupForm();
        this.openStartBtn();
        this.openLogInBtn();
    }
    closeSignupForm = () => {
        document.getElementsByClassName('SignupFormDiv')[0].style.display = 'none'
    }
    openStartBtn = () => {
        document.getElementsByClassName('StartBtnDiv')[0].style.display = 'block'
    }
    openLogInBtn = () => {
        document.getElementsByClassName('LogInBtnDiv')[0].style.display = 'block'
    }

    render(){
        return(
          <div style={{marginTop: '80px'}} className='SignupFormDiv'>

              <TextField id="standard-dense" label="Firstname" margin="dense"/>
              <TextField id="standard-dense" label="Lastname" margin="dense"/>
              <TextField id="standard-dense" label="Mobile" margin="dense"/>

              <TextField
                  id="filled-email-input"
                  label="*Email"
                  type="email"
                  name="email"
                  autoComplete="email"
                  margin="normal"
                  variant="filled"
              />

              <TextField
                  id="filled-password-input"
                  label="*Password"
                  type="password"
                  autoComplete="current-password"
                  margin="normal"
                  variant="filled"
              />
              <div style={{color:'grey'}}> * Required fields </div>
              <div><Button color="primary" style={{ marginTop:'20px'}}> sign up with google </Button></div>

              <Button variant='contained' color='primary' size='medium'> confirm </Button>

              <Button
                  variant='contained'
                  color='secondary'
                  size='medium'
                  className='Btn'
                  onClick={this.onClick}
              >
                cancel
              </Button>

          </div>

        )
    }
};

export default SignupForm