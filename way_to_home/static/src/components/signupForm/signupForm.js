import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Modal from '@material-ui/core/Modal';
import './signupForm.css';


class SignupForm extends Component{

    state = {
        open: false
    };

    signupFormOpen = () => {
        this.setState({ open: true });
        console.log('signup form is open');
    };

    signupFormClose = () => {
        this.setState({ open: false });
        console.log('signup form is close');
    };

    onClickConfirm = () => {
        console.log('click on confirm');
    };

    onClickGoogle = () => {
        console.log('click on signup with google')
    };

    render(){
        return(
        <Modal open={this.state.open} onClose={this.signupFormClose}>
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
                  onClick={this.signupFormClose}>
                cancel
              </Button>
          </div>
        </Modal>
        )
    };
};

export default SignupForm
