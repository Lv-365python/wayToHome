import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import axios from 'axios';
import WayTab from './wayTab/wayTab';
import './userSettingsForm.css';


class UserSettingsForm extends React.Component {
    state = {
        first_name: '',
        last_name: '',
        save_disabled: true,
        open: false
    };

    getProfile = () => {
        let url = "http://localhost:8000/api/v1/user/profile/";

        axios.get(url)
            .then(function(response){
                this.setState(state => ({
                    first_name: response.data.first_name,
                    first_name: response.data.last_name
                })
            )})
            .catch(function(error){
                console.log(error);
            })
    };

    postProfile = (event) => {
         let url = "http://localhost:8000/api/v1/user/profile/"
         axios.post(url, {
            first_name: this.state.first_name,
            last_name: this.state.last_name
         })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            })
    };

    componentDidMount() {
        this.getProfile();
        this.initial_state = {
            first_name: this.state.first_name,
            last_name: this.state.last_name
        };
    }

    checkChangesToSave = (event) => {
        let checked = event.target.value;
        this.setState(state=> {
            checked: checked
        })
        if (this.state.checked != initial_state.checked){
            this.setState({save_disabled: false});
        }
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
                <Button className = "saveButton"
                    variant="contained"
                    color='primary'
                    size='medium'
                    onClick={this.postProfile}
                />
            </div>
            )
        }
}

export default UserSettingsForm;

