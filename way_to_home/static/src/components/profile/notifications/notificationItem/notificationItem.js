import React, {Component} from 'react';
import axios from "axios";

import Chip from '@material-ui/core/Chip';
import IconButton from '@material-ui/core/IconButton';
import TimeIcon from '@material-ui/icons/Alarm';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import TimeField from "react-simple-timefield";

import './notificationItem.css';


export default class NotificationItem extends Component{

    state = {
        id: this.props.id,
        isTimePickerOpen: false,
        deleteAlertOpen: false,
        time: this.props.time.substring(0, 5),
        week_day: this.props.week_day,
        day: "",
        days: [
            { value: 0, label: 'Понеділок' },
            { value: 1, label: 'Вівторок' },
            { value: 2, label: 'Середа' },
            { value: 3, label: 'Четвер' },
            { value: 4, label: 'Пятниця' },
            { value: 5, label: 'Субота' },
            { value: 6, label: 'Неділя' },
        ],
    };

    componentDidMount(){
        this.dayCheck()
    }

    dayCheck = () => {
        this.state.days.map(day => {
            if (day.value === this.state.week_day){
                this.setState({
                    day: day.label
                })
            }
        });
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

    toggleDeleteAlert = () => {
        this.setState(state => ({
            deleteAlertOpen: !state.deleteAlertOpen
        }));
    };

    toggleTime = () => {
        this.setState(state => ({
            isTimePickerOpen: !state.isTimePickerOpen
        }));
    };

    onChangeTime = (newTime) => {
        let startDate = this.formatDate(this.props.start_date);
        let endDate = this.formatDate(this.props.end_date);
        let time = newTime + ':00';

        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/${this.state.id}`;
        axios.put(url + type, {
            start_time: startDate,
            end_time: endDate,
            time: time
        })
            .then(response => {
                this.props.setMessage('Час успішно оновлений', 'success');
            })
            .catch(error => {
                this.props.setMessage('Не вдалося оновити час', 'error')
            });
;
    };

    render(){
        return(
            <div>
                <div className="wayItem">
                    <Chip
                        className="textField"
                        color="primary"
                        label={this.state.day + " " + this.state.time}
                        variant="outlined" />
                    <Tooltip title="Змінити час">
                        <IconButton color="primary" aria-label="Змінити час" onClick={this.toggleTime}>
                            <TimeIcon/>
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Видалити">
                        <IconButton color="secondary" aria-label="Видалити" onClick={this.toggleDeleteAlert}>
                            <DeleteIcon/>
                        </IconButton>
                    </Tooltip>

                    {this.state.isTimePickerOpen &&
                    <div>
                        <div className='timePicker'>
                            <TimeField value={this.state.time}
                                       className={'timeInput'}
                                       onChange={this.onChangeTime}/>
                            <button className='saveTimeBtn'
                                    onClick={this.toggleTime}>
                                ЗБЕРЕГТИ
                            </button>
                        </div>
                    </div>}

                    <Dialog
                        open={this.state.deleteAlertOpen}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description" >
                        <DialogTitle id="alert-dialog-title">{"Видалити нотифікацію?"}</DialogTitle>
                        <DialogContent>
                            <DialogContentText id="alert-dialog-description">
                                Ви впевнені що хочете видалити нотифікацію?
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button
                                onClick={this.toggleDeleteAlert}
                                variant="outlined"
                                color="primary" >
                                Скасувати
                            </Button>
                            <Button
                                onClick={() => {this.props.deleteButton(this.state.id)}}
                                variant="outlined"
                                color="primary"
                                autoFocus >
                                Видалити
                            </Button>
                        </DialogActions>
                    </Dialog>
                </div>
            </div>
        )
    }
}
