import React, {Component} from 'react';
import {withRouter} from 'react-router-dom'
import axios from 'axios';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';

import { CustomizedSnackbars, iconSVG } from '../../index';
import SVGInline from "react-svg-inline";
import './loginForm.css';


class LoginForm extends Component {

    state = {
        request_type: 'login',
        confirm_button: 'увійти',
        change_button: 'зареєструватися',
        confirm_reset_button: 'скинути пароль',
        reset_password_button: 'забули пароль',
        repeat_display: 'none',
        repeat_reset_display: 'inline-flex',
        email: '',
        first_pass: '',
        second_pass: '',
        email_error: false,
        pass_error: false,
        disable_button: true,
        error: undefined,
        remember_me: false,
        showPassword: false,
    };

    onClickChangeType = () => {
        let display = this.state.repeat_display === 'inline-flex' ? 'none': 'inline-flex';
        let button_text = this.state.change_button === 'зареєструватися' ? 'увійти': 'зареєструватися';
        let confirm_text = this.state.confirm_button === 'зареєструватися' ? 'увійти': 'зареєструватися';
        let button_reset_password_text = this.state.reset_password_button === 'забули пароль';
        let type = this.state.request_type === 'register' ? 'login': 'register';

        this.setState({repeat_display: display,
            change_button: button_text,
            confirm_button: confirm_text,
            reset_password_button: button_reset_password_text,
            request_type: type
        });

        if(type === 'register' && this.state.first_pass !== this.state.second_pass)
            this.setState({disable_button: true});
    };

    onClickReset = () => {
        let display = this.state.repeat_reset_display === 'none' ? 'inline-flex': 'none';
        this.setState({
            repeat_reset_display: display,
            request_type: 'reset_password',
            confirm_button: 'відновити пароль'
        })
    };

    onClickConfirm = () => {
        let type = this.state.request_type;
        if(type === 'reset_password') {
            axios.post('/api/v1/user/' + type, {
                email: this.state.email
            })
                .then(() => {
                    setTimeout(() => {
                            this.props.history.go(0)
                        }, 3 * 1000);
                        this.setError('Підтвердіть Вашу пошту');
                })
                .catch((error) => {
                    this.setError(error.response.data);
                });
        }
        else {
            axios.post('/api/v1/user/' + type, {
                email: this.state.email,
                password: this.state.first_pass,
                remember_me: this.state.remember_me,
            })
                .then(() => {

                    if (this.state.request_type === 'register') {
                        setTimeout(() => {
                            this.props.history.go(0)
                        }, 3 * 1000);
                        this.setError('Підтвердіть Вашу пошту');
                    } else this.props.history.go(0)
                })
                .catch((error) => {
                    this.setError(error.response.data);
                });
        }
    };

    onChangeEmail = (event) => {
        let email = event.target.value;
        let email_error = this.handleEmail(email);

        this.setState({
            email: email,
            email_error: !email_error
        });

        this.handleButton(!email_error, email, this.state.pass_error, this.state.first_pass);
    };

    onChangeFirstPassword = (event) => {
        this.handleChange();

        let first_pass = event.target.value;
        let pass_error = !this.handlePassword(first_pass);

        this.setState({
            first_pass: first_pass,
            pass_error: pass_error
        });

        this.handleButton(this.state.email_error, this.state.email, pass_error, first_pass);
    };

    onChangeSecondPassword = (event) => {
        let second_pass = event.target.value;
        let pass_error = !this.handlePassword(this.state.first_pass, second_pass);

        this.setState({
            second_pass: second_pass,
            pass_error: pass_error
        });

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
    };

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
        let type = this.state.request_type;
        if (type === 'reset_password') {
            if (email_error) {
                this.setState({disable_button: true});
            }

            else if (!email) {
                this.setState({disable_button: true});
            }

            else
                this.setState({disable_button: false});

        } else {
            if (email_error || pass_error) {
                this.setState({disable_button: true});
            }

            else if (!email || !pass) {
                this.setState({disable_button: true});
            }

            else
                this.setState({disable_button: false});
        }
    };

    handleSigninGoogle = () => {
        axios.get('/api/v1/user/auth_via_google')
            .then((response ) => {
                window.location.replace(response.data.url);
            })
            .catch((error) => {
                this.setError("Не вдалося авторизуватись через Google.");
            });
    };

    changeSaveCookies = () => {
        this.setState({remember_me: !this.state.remember_me});
    };

    handleChange = prop => event => {
        this.setState({ [prop]: event.target.value });
    };

    handleClickShowPassword = () => {
        this.setState(state => ({ showPassword: !state.showPassword }));
    };

    render() {
        const {email_error, email, pass_error, first_pass, repeat_display, repeat_reset_display, second_pass,
            change_button, disable_button, confirm_button, reset_password_button, error, remember_me} = this.state;
        return (
            <div className='LoginFormDiv'>
                <TextField
                    error={email_error}
                    className="loginField"
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
                    label={pass_error ? 'Поганий пароль' : 'Пароль'}
                    type={this.state.showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    margin="normal"
                    variant="filled"
                    value={first_pass}
                    onChange={this.onChangeFirstPassword}
                    style={{paddingRight: '25px', width: '300px', display: repeat_reset_display}}

                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="Toggle password visibility"
                                    onClick={this.handleClickShowPassword}
                                >
                                    {this.state.showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                            </InputAdornment>
                        ),
                    }}
                />

                <TextField
                    error={pass_error}
                    style={{display: repeat_display}}
                    label={pass_error ? 'Поганий пароль' : 'Повторіть пароль'}
                    type={this.state.showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    margin="normal"
                    fullWidth
                    variant="filled"
                    value={second_pass}
                    onChange={this.onChangeSecondPassword}/>
                <div className="ResetPasswordButton">
                    <Button
                        style={{display: repeat_reset_display}}
                        className='reset_password_button'
                        color="primary"
                        onClick={this.onClickReset}>
                        {reset_password_button}
                    </Button>
                </div>
                <div>
                    <FormControlLabel
                        style={{display: repeat_reset_display}}
                        checked={remember_me}
                        onChange={this.changeSaveCookies}
                        control={<Checkbox value="checkedC"/>}
                        label="Запам'ятати мене"/>
                </div>
                <div className="blow">
                    <SVGInline
                        style={{display: repeat_reset_display}}
                        svg={ iconSVG }
                        onClick={this.handleSigninGoogle}
                    />
                </div>
                <div>
                    <Button
                        style={{display: repeat_reset_display}}
                        color="primary"
                        onClick={this.onClickChangeType}>
                        {change_button}
                    </Button>
                </div>
                <div className="loginButtons">
                    <Button
                        className='confirmButton'
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
