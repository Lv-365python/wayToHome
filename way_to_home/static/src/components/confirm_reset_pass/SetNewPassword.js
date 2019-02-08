import React, {Component} from 'react';
import axios from 'axios';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';

import { CustomizedSnackbars } from '../index';


export default class confirm_reset_pass extends Component{
    state = {
        new_password: "",
        save_disabled: true,
        ajaxError: undefined,
        new_password_error: false,
    };

    setMessage = (message, type) => {
        this.setState({
            ajaxMessage: message,
            messageType: type,
        })
    };

    handlePassword = (pass) => {
        let regex = /^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$/;
        return regex.test(pass);
    };

    newPasswordChange = (event) => {
        let changed = event.target.value;
        this.setState({new_password: changed});

        if(this.state.new_password === ""){
            this.setState({new_password_error: false})
        }

        if(this.handlePassword(this.state.new_password)){
            this.setState({
                new_password_error: false,
                save_disabled: false,
            })

        } else this.setState({new_password_error: true})
    };

    oldPasswordChange = (event) => {
        let changed = event.target.value;
        this.setState({old_password: changed});
    };

    saveButtonClick = (event) => {
        let token = this.props.match.params.token;
        axios.put('/api/v1/user/reset_password/' + token, {
            new_password: this.state.new_password,
        })
            .then(response =>{
                if(response.status === 200){
                    setTimeout(() => {
                        this.props.history.push("/home");
                    }, 3 * 1000);
                    this.setMessage('Пароль збережено', 'success');
                }

            })
            .catch(error => {
                this.setMessage("Введіть пароль, який не використовувався", 'error');
            })
    };

    render(){
        return(
            <div className="advancedSettingsDiv">
                <TextField
                    label = {this.state.new_password_error? "Непідходящий пароль" : "Новий пароль"}
                    className = "profileFields"
                    value = {this.state.new_password}
                    onChange = {this.newPasswordChange}
                    type = "new_password"
                    error = {this.state.new_password_error}
                />
                <div className="buttonsDiv">
                    <Button
                        className="saveButton"
                        variant="contained"
                        color="primary"
                        size="medium"
                        disabled={this.state.save_disabled}
                        onClick={this.saveButtonClick}>
                        Зберегти
                    </Button>
                    <Button
                        className="closeButton"
                        variant="contained"
                        color="secondary"
                        size="medium"
                        onClick={this.props.close}>
                        Скасувати
                    </Button>
                </div>

                {this.state.ajaxMessage &&
                <CustomizedSnackbars
                    message={this.state.ajaxMessage}
                    reset={this.setMessage}
                    variant={this.state.messageType}
                />
                }
            </div>
        )
    }
}
