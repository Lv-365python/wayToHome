
import React, {Component} from 'react';
import {withRouter} from 'react-router-dom'
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import SVGInline from "react-svg-inline";
import iconSVG from "./../../../public/images/google.svg";
import CustomizedSnackbars from '../message/message';
import axios from 'axios';
import './loginForm.css';


class LoginForm extends Component {

    state = {
        request_type: 'login',
        confirm_button: 'увійти',
        change_button: 'зареєструватися',
        repeat_display: 'none',
        email: '',
        first_pass: '',
        second_pass: '',
        email_error: false,
        pass_error: false,
        disable_button: true,
        error: undefined,
        remember_me: false,
    };

    onClickChangeType = () => {
        let display = this.state.repeat_display === 'inline-flex' ? 'none': 'inline-flex';
        this.setState({repeat_display: display});

        let button_text = this.state.change_button === 'зареєструватися' ? 'увійти': 'зареєструватися';
        this.setState({change_button: button_text});

        let confirm_text = this.state.confirm_button === 'зареєструватися' ? 'увійти': 'зареєструватися';
        this.setState({confirm_button: confirm_text});

        let type = this.state.request_type === 'register' ? 'login': 'register';
        this.setState({request_type: type});

        if(type === 'register' && this.state.first_pass !== this.state.second_pass)
            this.setState({disable_button: true});
    };

    onClickConfirm = () => {
        let type = this.state.request_type;
        axios.post('/api/v1/user/' + type, {
            email: this.state.email,
            password: this.state.first_pass,
            remember_me: this.state.remember_me,
        })
            .then(() => {

                if(this.state.request_type === 'register') {
                    setTimeout(() => {
                        this.props.history.go(0)
                    }, 5 * 1000);
                    this.setError('Підтвердіть Вашу пошту');
                }else this.props.history.go(0)
            })
            .catch((error) => {
                this.setError(error.response.data);
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

    setError = (value) => {
        this.setState({
            error: value
        });
    }

    handlePassword = (first_pass, second_pass) => {
        let regex = /^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$/;
        let type = this.state.request_type;

        if(type === 'register'){
            if(first_pass !== second_pass)
                return false;
            return regex.test(first_pass);
        }
        else if(type === 'login')
            return regex.test(first_pass);

        return false;
    };

    handleButton = (email_error, email, pass_error, pass) => {
        if(email_error || pass_error)
            this.setState({disable_button: true});
        else if(!email || !pass)
            this.setState({disable_button: true});
        else
            this.setState({disable_button: false});
    };

    handleSigninGoogle = () => {
        axios.get('/api/v1/user/auth_via_google')
            .then((response ) => {
                window.location.replace(response.data.url);
            })
            .catch((error) => {
                this.setError(error.response.data);
            });
    };

    changeSaveCookies = () => {
        this.setState({remember_me: !this.state.remember_me});

    };

    render() {
        const {email_error, email, pass_error, first_pass, repeat_display,second_pass,
            change_button, disable_button, confirm_button, error, remember_me} = this.state;
        return (
            <div className='LoginFormDiv'>
                <TextField
                    error={email_error}
                    className="loginField"
                    id="email-input"
                    label={email_error ? 'Поганий Email' : 'Email'}
                    type="email"
                    name="email"
                    autoComplete="email"
                    margin="normal"
                    fullWidth
                    variant="filled"
                    value={email}
                    onChange={this.onChangeEmail}/>
                <TextField
                    error={pass_error}
                    id="password-input"
                    label={pass_error ? 'Поганий пароль' : 'Пароль'}
                    type="password"
                    autoComplete="current-password"
                    margin="normal"
                    fullWidth
                    variant="filled"
                    value={first_pass}
                    onChange={this.onChangeFirstPassword}/>
                <TextField
                    error={pass_error}
                    style={{display: repeat_display}}
                    id="repeat-password-input"
                    label={pass_error ? 'Поганий пароль' : 'Повторіть пароль'}
                    type="password"
                    autoComplete="current-password"
                    margin="normal"
                    fullWidth
                    variant="filled"
                    value={second_pass}
                    onChange={this.onChangeSecondPassword}/>
                <div>
                    <FormControlLabel checked={remember_me}
                                      onChange={this.changeSaveCookies}
                                      control={<Checkbox value="checkedC"/>}
                                      label="Запам'ятати мене"/>
                </div>
                <div>
                    <SVGInline svg={ iconSVG }
                               onClick={this.handleSigninGoogle}
                    />
                </div>
                <div>
                    <Button color="primary" onClick={this.onClickChangeType}>
                        {change_button}
                    </Button>
                </div>
                <div className="loginButtons">
                    <Button className='confirmButton'
                            variant='contained'
                            color='primary'
                            size='medium'
                            disabled={disable_button}
                            onClick={this.onClickConfirm}>
                        {confirm_button}
                    </Button>
                    <Button
                        variant='contained'
                        color='secondary'
                        size='medium'
                        className='Btn'
                        onClick={this.props.close}>
                        відмінити
                    </Button>
                </div>
                { error && <CustomizedSnackbars message={error} reset={this.setError}/>}
            </div>
        )
    };
}

export default withRouter(LoginForm);
