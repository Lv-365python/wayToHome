import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Modal from '@material-ui/core/Modal';
import LoginForm from '../loginForm/loginForm.js';
import './loginBtn.css'


class LoginBtn extends Component{

    state = {
        open: false
    };

    onClickLoginBtn = () => {
        this.setState({open: true});
    };

    modalClose = () => {
        this.setState({open: false});
    };

    render(){
        return(
            <div className='LoginBtnDiv'>
                <Modal open={this.state.open}
                       onClose={this.modalClose}
                       disableAutoFocus={true}>

                <LoginForm close={this.modalClose} />

                </Modal>
                <Button variant="contained"
                    color='primary'
                    size='large'
                    onClick={this.onClickLoginBtn}
                    className='Btn'
                    style={{borderRadius: 0}}
                >
                        Увійти
                </Button>
            </div>
        )
    }
}

export default LoginBtn
