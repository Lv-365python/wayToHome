import React, {Component} from 'react';
import Header from "../header/header";
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import axios from 'axios';

export default class UserSettings extends Component{
    state = {
        request_type: 'put',
        first_name: '',
        last_name: '',
        save_disabled: true,
        open: false
    };

    initial_state = state

    checkChangesToSave = (event) => {
        let checked = event.target.value;
        this.setState(checked: checked)
        if (this.state.checked != initial_state.checked){
            this.setState({save_disabled: false});
        }
    }

    saveClick = (event) =>{
        this.initial_state = this.state
        let type = this.state.request_type;
        axios.post('http://127.0.0.1:8000/api/v1/user/profile/' + type, {
            first_name: this.state.first_name
            last_name: this.state.last_name
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render(){
        return(
            <div className="UserProfileDiv">
                <TextField
                    id="first_name-input"
                    type="first_name"
                    name="first_name"
                    autoComplete="first_name"
                    margin="normal"
                    variant="filled"
                    value={this.state.first_name}
                    onChange={this.checkChangesToSave}
                />
                <TextField
                    id="last_name-input"
                    type="last_name"
                    name="last_name"
                    autoComplete="last_name"
                    margin="normal"
                    variant="filled"
                    value={this.state.last_name}
                    onChange={this.checkChangesToSave}
                />
                <div className='PlacesButtonDiv'>
                    <Modal open={this.state.open}
                       onClose={this.modalClose}
                       disableAutoFocus="True">

                    <LoginForm close={this.modalClose} />

                    </Modal>
                    <Button variant="contained"
                        color='primary'
                        size='large'
                        onClick={this.onClickLoginBtn}
                        className='Btn'>
                        log in
                    </Button>
                </div>
                <Button className = "saveButton"
                    variant="contained"
                    color='primary'
                    size='medium'
                    onClick={this.saveClick}
                />

            </div>
        )
    }
}
