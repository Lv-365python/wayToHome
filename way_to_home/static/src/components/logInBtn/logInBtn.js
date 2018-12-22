import React, {Component} from 'react';
import './logInBtn.css'
import Button from '@material-ui/core/Button';
import '../logInForm.js'

class LogInBtn extends Component{

    state = {}

    onClick = () => {
    this.openLogInForm();
    this.closeStartBtn();
  }

  openLogInForm = () => {
    //alert('openLogInForm');
    document.getElementById('loginform').style.display = 'block'
  }

  closeStartBtn = () => {
//    document.getElementsByClassName('StartBtnDiv').hidden = true;
    document.getElementsByClassName('StartBtnDiv')[0].style.display = 'none'
  }


    render(){
        return(
            <div className='LogInBtnDiv'>
                <Button variant="contained" color='primary' size='large' onClick={this.onClick} className='Btn'>
                    LOG IN
                </Button>
            </div>
        )
    }
}

export default LogInBtn
