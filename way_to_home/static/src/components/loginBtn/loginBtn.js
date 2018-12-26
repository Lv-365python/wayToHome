import React, {Component} from 'react';
import './loginBtn.css'
import Button from '@material-ui/core/Button';
import LoginForm from '../loginForm/loginForm.js';

class LoginBtn extends Component{

    onClickLoginBtn = () => {
        this.refs.child.handleOpen();
        console.log('click on login button');
    }

    render(){
        return(
            <div className='LoginBtnDiv'>

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
