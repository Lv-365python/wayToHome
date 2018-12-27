import React, {Component} from 'react';
import './loginBtn.css'
import Button from '@material-ui/core/Button';
import LoginForm from '../loginForm/loginForm.js';
import SignupForm from '../signupForm/signupForm.js';

class LoginBtn extends Component{

    onClickLoginBtn = () => {
        this.refs.child.loginFormOpen();
        console.log('click on login button');
    }

    render(){
        return(
            <div className='LoginBtnDiv'>

                <SignupForm ref="child"/>
                <LoginForm ref="child"/>

                <Button variant="contained" color='primary' size='large'
                    onClick={this.onClickLoginBtn} className='Btn'>
                    log in
                </Button>
            </div>
        )
    }
}

export default LoginBtn
