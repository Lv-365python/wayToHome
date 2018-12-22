import React, {Component} from 'react';
import './logInBtn.css'
import Button from '@material-ui/core/Button';
import '../logInForm.js'

class LogInBtn extends Component{

    constructor(props){
        super(props)

        this.state = {
        }
    }

    onClick = () => {
    this.openLogInForm();
  }

  openLogInForm = () => {
    //alert('openLogInForm');
    document.getElementById('loginform').style.display = 'block'
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
