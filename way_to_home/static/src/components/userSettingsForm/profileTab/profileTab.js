import React from 'react';

import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import InputLabel from '@material-ui/core/InputLabel';

import axios from 'axios';

import './profileTab.css';

let savedState = {
    first_name: '',
    last_name: '',
    save_disabled: true,
    initial_first_name: '',
    initial_last_name: ''
}

export default class ProfileTab extends React.Component {
    state = {
        first_name: '',
        last_name: '',
        save_disabled: true,
        initial_first_name: '',
        initial_last_name: ''
    };



    getProfile = () => {
        let url = 'api/v1/user/profile';
        axios.get(url)
            .then(response => {
                this.setState({
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                    initial_first_name: response.data.first_name,
                    initial_last_name: response.data.last_name
                });
            })
            .catch(error => {
                console.log(error);
            })
    };

    postProfile = (event) => {
         let url = 'api/v1/user/profile';
         axios.put(url, {
            first_name: this.state.first_name,
            last_name: this.state.last_name
         })
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.log(error);
            })
    };

    componentDidMount(){
        if(savedState.save_disabled==true){
            this.getProfile();
        } else {
            this.setState(state=>savedState);
        }

    };

    componentWillUnmount(){
        savedState = this.state;
    };

    textFieldChangeFirstName = (event) => {
        let checked = event.target.value;
        this.setState({first_name: checked})
        if (checked !== this.state.initial_first_name){
            this.setState({save_disabled: false});
        } else if(this.state.last_name == this.state.initial_last_name){
            this.setState({save_disabled: true});
        }
    }

    textFieldChangeLastName = (event) => {
        let checked = event.target.value;
        this.setState({last_name: checked})
        if (checked != this.state.initial_last_name){
            this.setState({save_disabled: false});
        } else if (this.state.first_name == this.state.initial_first_name) {
            this.setState({save_disabled: true});
        }
    }


    render(){
        return(
            <div className="profileTabDiv">
                <div className="firstName">
                    <InputLabel>
                        Ім`я
                    </InputLabel>
                    <TextField
                        margin="normal"
                        variant="filled"
                        value={this.state.first_name}
                        onChange={this.textFieldChangeFirstName}
                    />
                </div>

                <div className="lastName">
                    <InputLabel>
                        Прізвіще
                    </InputLabel>
                    <TextField
                        margin="normal"
                        variant="filled"
                        value={this.state.last_name}
                        onChange={this.textFieldChangeLastName}
                    />
                </div>

                <Button
                    className="saveButton"
                    variant="contained"
                    color="primary"
                    size="large"
                    disabled={this.state.save_disabled}
                    onClick={this.postProfile}>
                    Зберегти
                </Button>
            </div>
            )
        }
}
