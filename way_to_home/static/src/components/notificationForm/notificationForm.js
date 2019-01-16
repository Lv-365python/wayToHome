import React, {Component} from 'react';
import Calendar from 'react-calendar'
import TimeField from 'react-simple-timefield';
import Button from '@material-ui/core/Button';
import axios from 'axios'
import './notificationForm.css';

class NotificationForm extends Component{

    state = {
        pointA: String(undefined),
        pointB: String(undefined),
        OpenStartDate: false,
        OpenEndDate: false,
        StartDate: new Date(),
        EndDate: new Date(),
        notifications: [
            {id: 0, time: '08:30', text: 'ПН', active: false, openTimePicker: false},
            {id: 1, time: '08:30', text: 'ВТ', active: false, openTimePicker: false},
            {id: 2, time: '08:30', text: 'СР', active: false, openTimePicker: false},
            {id: 3, time: '08:30', text: 'ЧТ', active: false, openTimePicker: false},
            {id: 4, time: '08:30', text: 'ПТ', active: false, openTimePicker: false},
            {id: 5, time: '08:30', text: 'СБ', active: false, openTimePicker: false},
            {id: 6, time: '08:30', text: 'НД', active: false, openTimePicker: false}
        ],
        saved_notifications: ''
    }

    showList = () => {
        return (
            <div>
                {this.state.notifications.map((not) => (
                    <li className={`not-done-${not.active} notification`}
                        onClick={() => this.updateNotActive(not.id)}>
                        <span className='changeTimeDiv'
                              onClick={(event) => {this.toggleTime(not.id); event.stopPropagation()}}>+</span>
                        {not.time}
                        <span className='not_space'> </span>
                        {not.text}

                        { not.openTimePicker &&
                        <div className='timePicker'
                             onClick={(event) => {event.stopPropagation()}}>
                            <TimeField value={not.time}
                                       className={'timeInput'}
                                       onChange={(value) => this.onChangeTime(value, not.id)}
                                       onClick={(event) => {event.stopPropagation()} }/>
                            <button className='saveTimeBtn'
                                    onClick={(event) => {this.toggleTime(not.id); event.stopPropagation()}}>ЗБЕРЕГТИ</button>
                        </div> }
                    </li>
                ))}
            </div>
        )
    }

    formatDate = (date) => {
        let d = date,
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    }

    updateNotActive = (id) => {
        let notifications_new = this.state.notifications.map((not) => {
            if (not.id === id){
                not.active = !not.active;
            }
            return not;
        });
        return this.setState({
            notifications: notifications_new
        });
    }

    toggleStartDate = () => {
        this.setState(state => ({
            OpenStartDate: !state.OpenStartDate
        }));
    }

    toggleEndDate = () => {
        this.setState(state => ({
            OpenEndDate: !state.OpenEndDate
        }));
    }

    onChangeStartDate = (newDate) => {
        this.setState(state => ({
            StartDate: newDate
        }));
        this.toggleStartDate()
    }

    onChangeEndDate = (newDate) => {
        this.setState(state => ({
            EndDate: newDate
        }));
        this.toggleEndDate()
    }

    toggleTime = (id) => {
        let notifications_new = this.state.notifications.map((not) => {
            if (not.id === id){
                not.openTimePicker = !not.openTimePicker;
            } else {
                not.openTimePicker = false
            }
            return not;
        });
        return this.setState({
            notifications: notifications_new
        });
    }

    onChangeTime = (newTime, id) => {
        let notifications_new = this.state.notifications.map((not) => {
            if (not.id === id){
                not.time = newTime
            }
            return not;
        });
        return this.setState({
            notifications: notifications_new
        });
    }

    getData = () => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let way_id = 1;
        let type = `way/${way_id}/notification/`;

        let self = this;

        axios.get(url+`way/${way_id}`)
            .then(function (response) {
                let name = response.data.name;
                self.setState(state => ({
                    pointA: name.split('-')[0],
                    pointB: name.split('-')[1]
                }));
            });

        axios.get(url+type)
            .then(function (response) {

                self.setState(state => ({
                    saved_notifications: response.data
                }));

                let start_date = response.data[0].start_time;
                let end_date = response.data[0].end_time;

                let parsed_start_date = new Date(start_date.substring(0,4),
                    start_date.substring(5,7)-1,
                    start_date.substring(9,11));
                let parsed_end_date = new Date(end_date.substring(0,4),
                    end_date.substring(5,7)-1,
                    end_date.substring(9,11));

                self.setState(state => ({
                    StartDate: parsed_start_date,
                    EndDate: parsed_end_date
                }));

                for (let i = 0; i<=response.data.length-1; i=i+1){
                    let notifications_new = self.state.notifications.map((not) => {
                        if (not.id === response.data[i].week_day){
                            not.time = response.data[i].time.substring(0,5);
                            not.active = true;
                        }
                        return not;
                    });
                    self.setState({
                        notifications: notifications_new
                    });
                }
            })
    };

    componentDidMount(){
        this.getData();
    }

    sendRequest = () => {

        let new_notifications = this.state.notifications;
        let old_notifications = this.state.saved_notifications;

        let new_start_date = this.formatDate(this.state.StartDate);
        let old_start_date = this.state.saved_notifications[0].start_time;

        let new_end_date = this.formatDate(this.state.EndDate);
        let old_end_date = this.state.saved_notifications[0].end_time;

        for (let i = 0; i <= new_notifications.length-1; i++){
            console.log(new_notifications[i])
            for (let j = 0; j <= old_notifications.length-1; j++){
                if (new_notifications[i].id === old_notifications[j].week_day) {
                    if (new_notifications[i].active === false) {
                        this.sendDelete(old_notifications[j].id)
                    }
                    else if (
                        (new_start_date != old_start_date || new_end_date != old_end_date) &&
                        new_notifications[i].active === true){
                        this.sendUpdateDate(old_notifications[j].id, new_start_date, new_end_date)
                    }
                    else if (new_notifications[i].time + ':00' != old_notification[j].time &&
                        new_notifications[i].active === true) {
                        this.sendUpdateTime(
                            old_notifications[j].id,
                            new_start_date,
                            new_end_date,
                            new_notifications[i].time)
                    }
                } else if (new_notifications[i].active === true){
                    this.sendPost(
                        new_start_date,
                        new_end_date,
                        new_notifications[i].id,
                        new_notifications[i].time,
                        old_notifications[j].way)
                }
            }
        }
    };

    sendUpdateDate = (id, start_time, end_time) => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let type = `notification/${id}/`;
        axios.put(url + type, {
            start_time: start_time,
            end_time: end_time
        })
            .then(function (response) {
                console.log(response);
                this.props.close();
            })
            .catch(function (error) {
                console.log(error);
            });

    };

    sendUpdateTime = (id, start_time, end_time, new_time) => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let type = `notification/${id}/`;
        axios.put(url + type, {
            start_time: start_time,
            end_time: end_time,
            time: new_time
        })
            .then(function (response) {
                console.log(response);
                this.props.close();
            })
            .catch(function (error) {
                console.log(error);
            });
    };


    sendPost = (start_time, end_time, week_day, time, way) => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let type = `notification/`;
        axios.post(url + type, {
            start_time: start_time,
            end_time: end_time,
            week_day: week_day,
            time: time,
            way: way
        })
            .then(function (response) {
                console.log(response);
                this.props.close();
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    sendDelete = (id) => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let type = `notification/${id}/`;
        axios.delete(url + type, {
        })
            .then(function (response) {
                console.log(response);
                this.props.close();
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    render() {
        return (
            <div className='notificationForm'>

                <div className='wayAB'>
                    <div className='pointA'
                         onClick={this.sendRequest}>
                        {this.state.pointA.toUpperCase()}
                    </div>
                    <div className='space'>
                        >>>>>>>
                    </div>
                    <div className='pointB'>
                        {this.state.pointB.toUpperCase()}
                    </div>
                </div>
                <ul className='notFormUl'>
                    {this.showList()}
                </ul>
                <div className='pickStartDate' onClick={this.toggleStartDate}>
                    <p>ПОЧАТКОВА ДАТА</p>
                </div>
                <div className='pickEndDate' onClick={this.toggleEndDate}>
                    <p>КІНЦЕВА ДАТА</p>
                </div>
                { this.state.OpenStartDate &&
                <div className='startDate'>
                    <Calendar onChange={this.onChangeStartDate}
                              value={this.state.StartDate} />
                </div> }
                { this.state.OpenEndDate &&
                <div className='endDate'>
                    <Calendar onChange={this.onChangeEndDate}
                              value={this.state.EndDate} />
                </div> }
                <div className='SaveBtn'>

                    <Button variant="contained" color='primary' size='large' onClick={this.sendRequest}>
                        ЗБЕРЕГТИ
                    </Button>
                </div>
            </div>
        );
    }
}

export default NotificationForm
