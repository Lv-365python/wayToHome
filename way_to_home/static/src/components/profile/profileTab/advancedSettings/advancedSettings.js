import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import axios from 'axios';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import TextField from '@material-ui/core/TextField';

import { CustomizedSnackbars } from '../../../index';
import { url } from '../profileTab.js'
import './advancedSettings.css';
import '../profileTab.css'

let savedState = {
    deleteAlertOpen: false,
    old_password: "",
    new_password: "",
    save_disabled: true,
    ajaxError: undefined,
    new_password_error: false,
};


class AdvancedSettings extends Component {

    state = {
        deleteAlertOpen: false,
        old_password: "",
        new_password: "",
        save_disabled: true,
        ajaxError: undefined,
        new_password_error: false,
    };

    setError = (error) => {
        this.setState({ajaxError: error});
    };

    deleteButtonClick = (event) => {
        let uri = '/delete_account';
        axios.delete(url + uri)
            .then((response) => {
                if(response.status === 200){
                    this.props.history.go(0)
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => {
                console.log(error);
            })
    };

    handlePassword = (pass) => {
        let regex = /^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$/;
        return regex.test(pass);
    };

    handleOpenDeleteAlert = (event) => {
        this.setState({
            deleteAlertOpen: true
        });
    };

    handleCloseDeleteAlert = (event) => {
        this.setState({
            deleteAlertOpen: false
        });
    };

    componentDidMount(){
        if(savedState.old_password!==""||savedState.new_password!==""){
            this.setState(state=>savedState);
        }
    };

    componentWillUnmount(){
        savedState = this.state;
    };

    newPasswordChange = (event) => {
        let changed = event.target.value;
        this.setState({new_password: changed});

        if(this.state.new_password === ""){
            this.setState({new_password_error: false});
        }
        if(this.handlePassword(this.state.new_password) ){
            this.setState({
                new_password_error: false,
                save_disabled: false,
            });
        } else {
            this.setState({new_password_error: true});
        }

    };

    oldPasswordChange = (event) => {
        let changed = event.target.value;
        this.setState({old_password: changed});
    };

    saveButtonClick = (event) => {
        let uri = '/change_password';
        axios.put(url + uri, {
            new_password: this.state.new_password,
            old_password: this.state.old_password,
        })
            .then(response =>{
                if(response.status === 200){
                    alert("Пароль збережено");
                } else {
                    this.setError("Не вірний старий пароль");
                }
            })
            .catch(error => {
                this.setError("Не вірний старий пароль");
            })
    };

    render() {
        return(
            <div className="advancedSettingsDiv">
                 <TextField
                    label = "Старий пароль"
                    className = "profileFields"
                    value = {this.state.old_password}
                    onChange = {this.oldPasswordChange}
                    type = "old_password"
                    />

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

                <Button
                    className="deleteButton"
                    variant="text"
                    color="primary"
                    size="small"
                    onClick={this.handleOpenDeleteAlert}>
                    Видалити аккаунт
                </Button>

                <Dialog
                  open={this.state.deleteAlertOpen}
                  aria-labelledby="alert-dialog-title"
                  aria-describedby="alert-dialog-description"
                >
                    <DialogTitle id="alert-dialog-title">{"Видалити користувача ?"}</DialogTitle>
                    <DialogContent>
                        <DialogContentText id="alert-dialog-description">
                            Ви впевнені, що хочете видалити свій аккаунт?
                            Також будуть видалені збережені сповіщення, шляхи та місця!
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>

                        <Button
                            onClick={this.handleCloseDeleteAlert}
                            variant="outlined"
                            color="primary"
                        >
                            Скасувати
                        </Button>

                        <Button
                            onClick={this.deleteButtonClick}
                            variant="outlined"
                            color="primary"
                            autoFocus
                        >
                            Видалити
                        </Button>

                    </DialogActions>
                </Dialog>
                {this.state.ajaxError &&
                <CustomizedSnackbars
                    message={this.state.ajaxError}
                    reset={this.setError}
                />
                }
            </div>
        )
    }
}

export default withRouter(AdvancedSettings);
