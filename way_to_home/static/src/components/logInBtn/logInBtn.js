import React, {Component} from 'react';
import './logInBtn.css'
import Button from '@material-ui/core/Button';
import '../loginForm/loginForm.js'

class LogInBtn extends Component{

    state = {}

    onClick = () => {
    this.openLoginForm();
    this.closeStartBtn();
    this.closeLogInBtn();
  }

  openLoginForm = () => {
    document.getElementsByClassName('LoginFormDiv')[0].style.display = 'block'
  }
  closeStartBtn = () => {
    document.getElementsByClassName('StartBtnDiv')[0].style.display = 'none'
  }
  closeLogInBtn = () => {
    document.getElementsByClassName('LogInBtnDiv')[0].style.display = 'none'
  }

    render(){
        return(
            <div className='LogInBtnDiv'>
                <Button variant="contained" color='primary' size='large' onClick={this.onClick} className='Btn'>
                    log in
                </Button>
            </div>
        )
    }
}

export default LogInBtn
