import React, {Component} from 'react';
import './logInBtn.css'
import Button from '@material-ui/core/Button';

class LogInBtn extends Component{

    constructor(props){
        super(props)

        this.state = {
        }
    }

    render(){
        return(
            <div className='LogInBtnDiv'>
                <Button variant="contained" color='primary' size='large' onClick={this.logIn}>
                    LOG IN
                </Button>
            </div>
        )
    }

    logIn = () => {
        alert('log in')
    }
}

export default LogInBtn;