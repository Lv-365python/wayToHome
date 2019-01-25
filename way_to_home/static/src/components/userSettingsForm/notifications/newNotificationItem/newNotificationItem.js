import React, {Component} from 'react';

import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import Done from '@material-ui/icons/Done';
import IconButton from '@material-ui/core/IconButton';
import MenuItem from "@material-ui/core/MenuItem/MenuItem";

import './newNotificationItem.css';


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
        clock: [
            {value: "06:00"},
            {value: "06:30"},
            {value: "07:00"},
            {value: "07:30"},
            {value: "08:00"},
            {value: "08:30"},
            {value: "09:00"},
            {value: "09:30"},
            {value: "10:00"},
            {value: "10:30"},
            {value: "11:00"},
            {value: "11:30"},
            {value: "12:00"},
            {value: "12:30"},
            {value: "13:00"},
            {value: "13:30"},
            {value: "14:00"},
            {value: "14:30"},
            {value: "15:00"},
            {value: "15:30"},
            {value: "16:00"},
            {value: "16:30"},
            {value: "17:00"},
            {value: "17:30"},
            {value: "18:00"},
            {value: "18:30"},
            {value: "19:00"},
            {value: "19:30"},
            {value: "20:00"},
            {value: "20:30"},
            {value: "21:00"},
            {value: "21:30"},
            {value: "22:00"},
            {value: "22:30"},
            {value: "23:00"}
        ]
    };

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
                        onClick={() => {this.props.saveNotification(this.state.week_day, this.state.time)}}>
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
