import React, {Component} from 'react';
import './loginBtn.css'
import Button from '@material-ui/core/Button';
import Modal from '@material-ui/core/Modal';
import LoginForm from '../loginForm/loginForm.js';

class LoginBtn extends Component{

  state = {
    open: false,
  };

  handleOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  onClick = () => {
    this.setState({open: !this.state.open});
    console.log(this.state.openLogin);
  }

    render(){
        return(
            <div className='LoginBtnDiv'>
                <Modal open={this.state.open} onClose={this.handleClose}>
                        <LoginForm />
                </Modal>
                <Button variant="contained" color='primary' size='large' onClick={this.onClick} className='Btn'>
                    log in
                </Button>
            </div>

        )
    }
}

export default LoginBtn
