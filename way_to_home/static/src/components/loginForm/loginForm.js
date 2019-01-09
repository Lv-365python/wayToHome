
import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios';
import './loginForm.css';


class LoginForm extends Component {

    state = {
        request_type: 'login',
        change_button: 'sign up',
        repeat_display: 'none',
        email: '',
        first_pass: '',
        second_pass: '',
        email_error: false,
        pass_error: false,
        disable_button: true,
    };

    onClickChangeType = () => {
        let display = this.state.repeat_display === 'inline-flex' ? 'none': 'inline-flex';
        this.setState({repeat_display: display});

        let button_text = this.state.change_button === 'sign up' ? 'login': 'sign up';
        this.setState({change_button: button_text});

        let type = this.state.request_type === 'register' ? 'login': 'register';
        this.setState({request_type: type});

        if(type === 'register' && this.state.first_pass !== this.state.second_pass)
            this.setState({disable_button: true});
    };

    onClickConfirm = () => {
        let type = this.state.request_type;

        axios.post('http://127.0.0.1:8000/api/v1/user/' + type, {
            email: this.state.email,
            password: this.state.first_pass,
            //save_cookie: this.state.save_cookie,
        })
            .then(function (response) {
                console.log(response);
                this.props.close();
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    onChangeEmail = (event) => {
        let email = event.target.value;
        this.setState({email: email});
        let email_error = this.handleEmail(email);
        this.setState({email_error: !email_error});
        this.handleButton(!email_error, email, this.state.pass_error, this.state.first_pass);
    };

    onChangeFirstPassword = (event) => {
        let first_pass = event.target.value;
        this.setState({first_pass: first_pass});
        let pass_error = !this.handlePassword(first_pass);
        this.setState({pass_error: pass_error});
        this.handleButton(this.state.email_error, this.state.email, pass_error, first_pass);
    };

    onChangeSecondPassword = (event) => {
        let second_pass = event.target.value;
        this.setState({second_pass: second_pass});
        let pass_error = !this.handlePassword(this.state.first_pass, second_pass);
        this.setState({pass_error: pass_error});
        this.handleButton(this.state.email_error, this.state.email, pass_error, this.state.first_pass);
    };

    handleEmail = (email) => {
        let regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regex.test(String(email).toLowerCase());
    };

    handlePassword = (first_pass, second_pass) => {
        let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
        let type = this.state.request_type;

        if(type === 'register'){
            if(first_pass !== second_pass)
                return false;
            return regex.test(first_pass);
        }
        else if(type === 'login')
            return regex.test(first_pass);

        return false
    };

    handleButton = (email_error, email, pass_error, pass) => {
        if(email_error || pass_error)
            this.setState({disable_button: true});
        else if(!email || !pass)
            this.setState({disable_button: true});
        else
            this.setState({disable_button: false})
    };

    render() {
        return (
            <div className='LoginFormDiv'>
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
                    onChange={this.onChangeEmail}/>
                <TextField
                    error={this.state.pass_error}
                    id="password-input"
                    label={this.state.pass_error ? 'Bad Password' : 'Password'}
                    type="password"
                    autoComplete="current-password"
                    margin="normal"
                    variant="filled"
                    value={this.state.first_pass}
                    onChange={this.onChangeFirstPassword}/>
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
                    onChange={this.onChangeSecondPassword}/>
                <div>
                    <FormControlLabel control={<Checkbox value="checkedC"/>} label="Remember me"/>
                </div>
                <div>
                    <Button color="primary" onClick={this.onClickChangeType}>
                        {this.state.change_button}
                    </Button>
                </div>
                <div className="loginButtons">
                    <Button className='confirmButton'
                            variant='contained'
                            color='primary'
                            size='medium'
                            disabled={this.state.disable_button}
                            onClick={this.onClickConfirm}>
                        {this.state.request_type}
                    </Button>
                    <Button
                        variant='contained'
                        color='secondary'
                        size='medium'
                        className='Btn'
                        onClick={this.props.close}>
                        cancel
                    </Button>
                </div>
            </div>
        )
    };
}

export default LoginForm
