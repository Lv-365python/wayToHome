import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import Modal from '@material-ui/core/Modal';
import SignupForm from '../signupForm/signupForm.js';
import LoginForm from '../loginForm/loginForm.js';
import './loginBtn.css'


class LoginBtn extends Component{

    constructor(props) {
        super(props)

        // Bind the this context to the handler function
        this.modalClose = this.modalClose.bind(this);

        // Set some state
        this.state = {
            open: false
        };
    }

    onClickLoginBtn = () => {
        this.setState({open: true});
        console.log('click on login button');
    }

    modalClose = () => {
        this.setState({open: false});
        console.log('modal window is close');
    }

    toggle() {
		this.setState({
			open: !this.state.open
		});
	}

    render(){
        var shown = {
			display: this.state.shown ? "block" : "none"
		};

		var hidden = {
			display: this.state.shown ? "none" : "block"
		}
        return(

            <div className='LoginBtnDiv'>
                <Modal open={this.state.open} onClose={this.modalClose}>

                <LoginForm action={this.modalClose} />

                </Modal>
                <Button variant="contained"
                    color='primary'
                    size='large'
                    onClick={this.onClickLoginBtn}
                    className='Btn'>
                        log in
                </Button>

            </div>
        )
    }
}

export default LoginBtn
