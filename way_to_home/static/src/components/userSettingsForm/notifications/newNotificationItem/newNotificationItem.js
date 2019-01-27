import React, {Component} from 'react';

import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import Done from '@material-ui/icons/Done';
import IconButton from '@material-ui/core/IconButton';
import MenuItem from "@material-ui/core/MenuItem/MenuItem";

import './newNotificationItem.css';
import axios from "axios";

class NewNotificationItem extends Component{

    state = {
        time: "08:30",
        week_day: 0,
        isTimePickerOpen: false,
        day: 'Понеділок',
        days: [
            {
                value: 0,
                label: 'Понеділок',
            },
            {
                value: 1,
                label: 'Вівторок',
            },
            {
                value: 2,
                label: 'Середа',
            },
            {
                value: 3,
                label: 'Четвер',
            },
            {
                value: 4,
                label: 'Пятниця',
            },
            {
                value: 5,
                label: 'Субота',
            },
            {
                value: 5,
                label: 'Неділя',
            },
        ],
        clock: []
    };

    formatDate = (date) => {
        let d = date,
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    };

    addTime = () => {
        let minutes = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"];
        let times = [];
        for(let i = 6; i < 23; i++){
            for(let j = 0; j < minutes.length; j++){
                let f = (i < 10? '0'+i : i);
                let t = {value: f + ":" + minutes[j]};
                times.push(t);
            }
        }
        this.setState({
            clock: times
        })
    };

    componentDidMount(){
        this.addTime()
    }

    handleChange = name => event => {
        this.setState({
            [name]: event.target.value
        });

        let d = event.target.value;
        this.state.days.map(day => {
            if (day.label.trim() === d){
                this.setState({
                    week_day: day.value
                })
            }
        });
    };

    sendPost = () => {
        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/`;
        axios.post(url + type, {
            start_time: this.formatDate(this.props.StartDate),
            end_time: this.formatDate(this.props.EndDate),
            week_day: this.state.week_day,
            time: this.state.time + ':00'
        })
            .then(response => {
            this.props.saveNotification(response.data);
            this.props.close();
        }).catch(error => {
            this.props.close();
            this.props.setError("Не вдалось створити місце. Спробуйте ще раз.");
        });
    };

    render() {
        return (
            <div className="newNotificationItem">
                <TextField
                    select
                    className="textField"
                    label="Виберіть день нотифікації"
                    value={this.state.day}
                    onChange={this.handleChange("day")}
                >
                    {this.state.days.map(day => (
                        <MenuItem key={day.value} value={day.label}>
                            {day.label}
                        </MenuItem>
                    ))}
                </TextField>

                <div className="space"></div>

                <TextField
                    select
                    className="textField"
                    label="Виберіть час нотифікації"
                    value={this.state.time}
                    onChange={this.handleChange("time")}
                    >
                {this.state.clock.map(time => (
                        <MenuItem key={time.value} value={time.value}>
                            {time.value}
                        </MenuItem>
                    ))}
                </TextField>

                <div className="space"></div>

                <Tooltip title="Зберегти">
                    <IconButton
                        color="primary"
                        aria-label="Зберегти"
                        onClick={this.sendPost}>
                        <Done/>
                    </IconButton>
                </Tooltip>

                <Tooltip title="Видалити">
                    <IconButton
                        color="secondary"
                        aria-label="Видалити"
                        onClick={this.props.deleteButton}>
                        <DeleteIcon/>
                    </IconButton>
                </Tooltip>
            </div>
        )
    }
}

export default NewNotificationItem
