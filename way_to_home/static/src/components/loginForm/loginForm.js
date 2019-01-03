import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios';
import './loginForm.css';


class LoginForm extends Component {

    state = {
        display: 'block',
        request_type: 'login',
        change_button: 'sign up',
        repeat_display: 'none',
        email: '',
        first_pass: '',
        second_pass: '',
        email_error: false,
        pass_error: false,
    };

    onClickSignup = () => {
        let display = this.state.repeat_display === 'inline-flex' ? 'none': 'inline-flex';
        this.setState({repeat_display: display});

        let button_text = this.state.change_button === 'sign up' ? 'login': 'sign up';
        this.setState({change_button: button_text});
        let type = this.state.request_type === 'register' ? 'login': 'register';
        this.setState({request_type: type});
    };

    onClickConfirm = () => {
        let type = this.state.request_type;

        let email = this.handleEmail(this.state.email);
        let pass = this.handlePassword(type);

        let is_error = false;
        if(!email){
            this.setState({email_error: true});
            is_error = true;
        }
        else
            this.setState({email_error: false});

        if(!pass){
            this.setState({pass_error: true});
            is_error = true;
        }
        else
            this.setState({pass_error: false});

        if(is_error)
            return;

        axios.post('http://127.0.0.1:8000/api/v1/user/' + type, {
            email: email,
            password: pass
        })
            .then(function (response) {
                console.log(response);
                this.props.action();
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    handleEmail = (email) => {
        let regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

        if(!regex.test(String(email).toLowerCase()))
            return false;

        return email;
    };

    handlePassword = (request_type) => {
        let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
        let first_pass = this.state.first_pass;
        let second_pass = this.state.second_pass;

        if(request_type === 'register'){
            if(first_pass !== second_pass)
                return false;
            if(!regex.test(first_pass))
                return false;
            return first_pass;
        }

        else if(request_type === 'login'){
            if(!regex.test(first_pass))
                return false;
            return first_pass;
        }

        return false
    };

    render() {
        return (
            <div style={{marginTop: '10rem', paddingBottom: '16px', display: this.state.display}}
                 className='LoginFormDiv'>
                <TextField
                    error={this.state.email_error}
                    id="email-input"
                    label={this.state.email_error ? 'Bad Email' : 'Email'}
                    type="email"
                    name="email"
                    autoComplete="email"
                    margin="normal"
                    variant="filled"
                    value={this.state.email}
                    onChange={(e) => this.setState({email: e.target.value})}/>
                <TextField
                    error={this.state.pass_error}
                    id="password-input"
                    label={this.state.pass_error ? 'Bad Password' : 'Password'}
                    type="password"
                    autoComplete="current-password"
                    margin="normal"
                    variant="filled"
                    value={this.state.first_pass}
                    onChange={(e) => this.setState({first_pass: e.target.value})}/>
                <TextField
                    error={this.state.pass_error}
                    style={{display: this.state.repeat_display}}
                    id="repeat-password-input"
                    label={this.state.pass_error ? 'Bad Password' : 'Repeat Password'}
                    type="password"
                    autoComplete="current-password"
                    margin="normal"
                    variant="filled"
                    value={this.state.second_pass}
                    onChange={(e) => this.setState({second_pass: e.target.value})}/>
                <div>
                    <FormControlLabel control={<Checkbox value="checkedC"/>} label="Remember me"/>
                </div>
                <div>
                    <Button color="primary" onClick={this.onClickSignup}>
                        {this.state.change_button}
                    </Button>
                </div>
                <div style={{marginTop: '16px'}}>
                    <Button style={{marginRight: '1rem'}}
                            variant='contained'
                            color='primary'
                            size='medium'
                            onClick={this.onClickConfirm}>
                        {this.state.request_type}
                    </Button>
                    <Button
                        variant='contained'
                        color='secondary'
                        size='medium'
                        className='Btn'
                        onClick={this.props.action}>
                        cancel
                    </Button>
                </div>
            </div>
        )
    };
}

export default LoginForm
