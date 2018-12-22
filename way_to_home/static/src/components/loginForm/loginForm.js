import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import './loginForm.css'

class TextFields extends Component {

  constructor(props){
    super(props);

    this.state = {
      name: this.props.name,
      value: undefined,
      multiline: 'Controlled',
    }
  }



    render() {
      return (
        <div>
          <TextField
            label={this.state.name}
            value={this.state.value}
            onChange={this.handleChange}/>
        </div>
      )
    }
};

class LoginForm extends Component{

    state = {}

    render(){
        return(
          <div className='loginForm'>

              <TextField
                  id="filled-email-input"
                  label="Email"
                  type="email"
                  name="email"
                  autoComplete="email"
                  margin="normal"
                  variant="filled"
              />

              <TextField
                  id="filled-password-input"
                  label="Password"
                  type="password"
                  autoComplete="current-password"
                  margin="normal"
                  variant="filled"
              />

              <Button variant='contained' color='primary' size='medium' className='Btn'>
                confirm
              </Button>

              <Button variant='contained' color='primary' size='medium' className='Btn'>
                cancel
              </Button>
              <button className="hideBtn"> X </button>
          </div>

        )
    }
};

export default LoginForm