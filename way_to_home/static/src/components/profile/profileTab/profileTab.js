import React from 'react';
import axios from 'axios';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Modal from '@material-ui/core/Modal';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import SettingsIcon from '@material-ui/icons/Settings';
import Chip from '@material-ui/core/Chip';
import Avatar from '@material-ui/core/Avatar';

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faTelegram} from '@fortawesome/free-brands-svg-icons'

import AdvancedSettings from './advancedSettings/advancedSettings.js';
import './profileTab.css';
import {CustomizedSnackbars} from '../';

let savedState = {
    first_name: '',
    last_name: '',
    phone_number: '',
    save_disabled: true,
    initial_first_name: '',
    initial_last_name: '',
    initial_phone_number: '',
    phone_error: false,
    email: '',
    openAdvancedModal: false,
    ajaxMessage: '',
    messageType: '',
    user_id: '',
    telegram_id: undefined,
};

export const url = '/api/v1/user';
const telegram_bot_name = 'WayToHomeBot';
const telegram_bot_url = 'https://telegram.me/' + telegram_bot_name;


export default class ProfileTab extends React.Component {
    state = {
        first_name: '',
        last_name: '',
        phone_number: '',
        save_disabled: true,
        initial_first_name: '',
        initial_last_name: '',
        initial_phone_number: '',
        phone_error: false,
        email: '',
        openAdvancedModal: false,
        ajaxMessage: '',
        messageType: '',
        user_id: '',
        telegram_id: undefined,
    };

    setMessage = (message, type) => {
        this.setState({
            ajaxMessage: message,
            messageType: type,
        });
    };

    getProfile = () => {
        let uri = '/profile';
        axios.get(url + uri)
            .then(response => {
                this.setState({
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                    initial_first_name: response.data.first_name,
                    initial_last_name: response.data.last_name,
                    telegram_id: response.data.telegram_id,
                });
            })
            .catch(error => {
                this.setMessage('Не вдалося завантажити дані.', 'error')
            })
    };

    getUserData = () => {
        axios.get(url + '/')
            .then(response => {
                this.setState({
                    user_id: response.data.id,
                    phone_number: response.data.phone_number,
                    initial_phone_number: response.data.phone_number,
                    email: response.data.email,
                });
            })
            .catch(error => {
                this.setMessage('Не вдалося завантажити данні.', 'error')
            })
    };

    saveProfile = () => {
        let uri = '/profile';
        axios.put(url + uri, {
            first_name: this.state.first_name,
            last_name: this.state.last_name,
        })
            .then(response => {
                this.setMessage('Зміни профілю збережено.', 'success')
            })
            .catch(error => {
                this.setMessage('Не вдалося зберегти дані.', 'error')
            })
    };

    savePhone = () => {
        let uri = '/phone';
        axios.put(url + uri, {
            phone: this.state.phone_number,
        })
            .then(response => {
                this.setMessage('Зміни номеру телефону збережено.', 'success')
            })
            .catch(error => {
                this.setMessage('Не вдалося зберегти данні', 'error')
            })
    };

    saveToDatabase = (event) => {
        if (!this.state.phone_error) {
            this.savePhone();
        }
        this.saveProfile();
        this.setState({
            save_disabled: true,
        });
    };

    componentDidMount() {
        if (savedState.save_disabled === true && savedState.phone_error === false) {
            this.getProfile();
            this.getUserData();
        } else {
            this.setState(savedState);
        }

    };

    componentWillUnmount() {
        savedState = this.state;
    };

    checkSaveActive = (name, surname, number, error) => {
        if (name === this.state.initial_first_name &&
            surname === this.state.initial_last_name) {
            if (error) {
                this.setState({save_disabled: true});
            } else if (number !== this.state.initial_phone_number) {
                this.setState({save_disabled: false});
            } else {
                this.setState({save_disabled: true});
            }
        } else {
            this.setState({save_disabled: false});
        }
    };

    textFieldChangeFirstName = (event) => {
        let checked = event.target.value;
        this.setState({first_name: checked})
        this.checkSaveActive(checked, this.state.last_name,
            this.state.phone_number, this.state.phone_error)
    };

    textFieldChangeLastName = (event) => {
        let checked = event.target.value;
        this.setState({last_name: checked});
        this.checkSaveActive(this.state.first_name, checked,
            this.state.phone_number, this.state.phone_error)
    };

    textFieldChangePhoneNumber = (event) => {
        let checked = event.target.value;
        let error = this.handlePhoneNumber(checked);
        this.setState({
            phone_number: checked,
            phone_error: error,
        });
        this.checkSaveActive(this.state.first_name, this.state.last_name,
            checked, error)
    };

    handlePhoneNumber = (phone) => {
        let regex = /^\+380[0-9]{9}$/;
        return !regex.test(String(phone).toLowerCase());
    };

    onClickAdvancedBtn = () => {
        this.setState({openAdvancedModal: true});
    };


    modalAdvancedClose = () => {
        this.setState({openAdvancedModal: false});
    };

    removeTelegramClick = (event) => {
        let uri = '/profile/telegram_id';
        axios.put(url + uri, {
            telegram_id: null
        })
            .then(response => {
                this.setMessage('Telegram успішно відключено', 'success')
                this.setState({telegram_id: undefined})
            })
            .catch(error => {
                this.setMessage('Telegram не вдалось відключити', 'error')
            })
    };

    telegramRedirectClick = (event) => {
        let uri = '/profile/telegram_access_token';
        let token = this.generateToken();

        axios.put(url + uri, {
            token: token
        })
            .then(response => {
                window.open(telegram_bot_url + '?start=' + token, '_blank');
                this.setState({telegram_id: 'placeholder'});
            })
            .catch(error => {
                this.setMessage('Не вдалося підключити Telegram, спробуйте пізніше', 'error')
            })

    };

    generateToken = () => {
        return Math.random().toString(36).substring(2);
    };

    render() {
        return (
            <div className="profileTabDiv">

                <TextField
                    className="emailField"
                    variant="outlined"
                    value={this.state.email}
                    disabled={true}
                />

                <div className="profileFields">
                    <TextField
                        label="Ім'я"
                        margin="normal"
                        variant="filled"
                        value={this.state.first_name}
                        onChange={this.textFieldChangeFirstName}
                    />
                </div>

                <div className="profileFields">
                    <TextField
                        label="Прізвіще"
                        margin="normal"
                        variant="filled"
                        value={this.state.last_name}
                        onChange={this.textFieldChangeLastName}
                    />
                </div>

                <div className="profileFields">
                    <TextField
                        label={this.state.phone_error ? "Некоректний номер" : "Номер телефону"}
                        margin="normal"
                        variant="filled"
                        value={this.state.phone_number || "+380"}
                        onChange={this.textFieldChangePhoneNumber}
                        error={this.state.phone_error}
                    />
                </div>

                <Chip
                    className="telegramChip"
                    color="primary"
                    label={this.state.telegram_id ? "Відключити телеграм" : "Підключити телеграм"}
                    onClick={this.state.telegram_id ? null : this.telegramRedirectClick}
                    onDelete={this.state.telegram_id ? this.removeTelegramClick : null}
                    clickable={!this.state.telegram_id}
                    avatar={
                        <Avatar>
                            <FontAwesomeIcon icon={faTelegram}/>
                        </Avatar>
                    }
                />

                <Button
                    className="saveButton"
                    variant="contained"
                    color="primary"
                    size="large"
                    disabled={this.state.save_disabled}
                    onClick={this.saveToDatabase}>
                    Зберегти
                </Button>

                <Tooltip title="Додаткові Налаштування">
                    <IconButton
                        color="primary"
                        aria-label="Додаткові Налаштування"
                        onClick={this.onClickAdvancedBtn}
                        size="medium"
                    >
                        <SettingsIcon/>
                    </IconButton>
                </Tooltip>

                <div>
                    <Modal
                        open={this.state.openAdvancedModal}
                        onClose={this.modalAdvancedClose}
                        disableAutoFocus={true}>
                        <AdvancedSettings
                            close={this.modalAdvancedClose}
                        />
                    </Modal>
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
