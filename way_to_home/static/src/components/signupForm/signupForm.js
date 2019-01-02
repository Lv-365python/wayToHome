import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import './signupForm.css';


class SignupForm extends Component{

    state = {
        display: 'block'
    }

    signupFormOpen = () => {
        console.log('signup form is open');
    };

    signupFormClose = () => {
        console.log('signup form is close');
        this.setState({display: 'none'});
    };

    onClickConfirm = () => {
        console.log('click on confirm');
    };

    onClickGoogle = () => {
        console.log('click on signup with google');
    };

    render(){
        return(
          <div style={{marginTop: '80px', display: this.state.display}} className='SignupFormDiv'>
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
                  variant="filled"/>
              <TextField
                  id="filled-password-input"
                  label="*Password"
                  type="password"
                  autoComplete="current-password"
                  margin="normal"
                  variant="filled"/>
              <div style={{color:'grey'}}>
                * Required fields
              </div>
              <div>
                <Button color="primary" style={{ marginTop:'20px'}} onClick={this.onClickGoogle}>
                    sign up with google
                </Button>
              </div>
              <Button variant='contained' color='primary' size='medium' onClick = {this.onClickConfirm}>
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

export default SignupForm
