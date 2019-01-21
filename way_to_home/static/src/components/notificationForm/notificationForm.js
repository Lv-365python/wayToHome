import React, {Component} from 'react';
import Calendar from 'react-calendar'
import TimeField from 'react-simple-timefield';
import axios from 'axios'
import './notificationForm.css';

class NotificationForm extends Component {

    state = {
        pointA: String(undefined),
        pointB: String(undefined),
        OpenStartDate: false,
        OpenEndDate: false,
        StartDate: new Date(),
        EndDate: new Date(),
        notifications: [
            {id: 0, time: '08:30', text: 'ПН', active: false, openTimePicker: false, db_id: 0},
            {id: 1, time: '08:30', text: 'ВТ', active: false, openTimePicker: false, db_id: 0},
            {id: 2, time: '08:30', text: 'СР', active: false, openTimePicker: false, db_id: 0},
            {id: 3, time: '08:30', text: 'ЧТ', active: false, openTimePicker: false, db_id: 0},
            {id: 4, time: '08:30', text: 'ПТ', active: false, openTimePicker: false, db_id: 0},
            {id: 5, time: '08:30', text: 'СБ', active: false, openTimePicker: false, db_id: 0},
            {id: 6, time: '08:30', text: 'НД', active: false, openTimePicker: false, db_id: 0}
        ],
        saved_notifications: ''
    };

    showList = () => {
        return (
            <div>
                {this.state.notifications.map((not) => (
                    <li className={`not-done-${not.active} notification`}
                        onClick={() => this.updateNotActive(not.id)}>
                        <span className='changeTimeDiv'
                              onClick={(event) => {
                                  this.toggleTime(not.id);
                                  event.stopPropagation()
                              }}>+</span>
                        {not.time}
                        <span className='not_space'> </span>
                        {not.text}

                        {not.openTimePicker &&
                        <div className='timePicker'
                             onClick={(event) => {
                                 event.stopPropagation()
                             }}>
                            <TimeField value={not.time}
                                       className={'timeInput'}
                                       onChange={(value) => this.onChangeTime(value, not.id)}
                                       onClick={(event) => {
                                           event.stopPropagation()
                                       }}/>
                            <button className='saveTimeBtn'
                                    onClick={(event) => {
                                        this.toggleTime(not.id);
                                        event.stopPropagation()
                                    }}>ЗБЕРЕГТИ
                            </button>
                        </div>}
                    </li>
                ))}
            </div>
        )
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

    updateNotActive = (id) => {
        let notifications_new = this.state.notifications.map((not) => {
            if (not.id === id) {
                not.active = !not.active;
                if (not.active === true){
                    this.sendPost(
                        this.formatDate(this.state.StartDate),
                        this.formatDate(this.state.EndDate),
                        not.id,
                        not.time);
                } else {
                    this.sendDelete(not.db_id);
                }
            }
            return not;
        });
        return this.setState({
            notifications: notifications_new
        },() => {this.getData()});
    };

    toggleStartDate = () => {
        this.setState(state => ({
            OpenStartDate: !state.OpenStartDate
        }));
    };
1
    toggleEndDate = () => {
        this.setState(state => ({
            OpenEndDate: !state.OpenEndDate
        }));
    };

    onChangeStartDate = (newDate) => {
        this.setState(state => ({
            StartDate: newDate
        }));
        this.sendRequest();
        this.toggleStartDate();
    };

    onChangeEndDate = (newDate) => {
        this.setState(state => ({
            EndDate: newDate
        }));
        this.sendRequest();
        this.toggleEndDate();
    };

    toggleTime = (id) => {
        let notifications_new = this.state.notifications.map((not) => {
            if (not.id === id) {
                not.openTimePicker = !not.openTimePicker;
            } else {
                not.openTimePicker = false
            }
            return not;
        });
        this.setState({
            notifications: notifications_new
        },()=>{this.sendRequest();});
    };

    onChangeTime = (newTime, id) => {
        let notifications_new = this.state.notifications.map((not) => {
            if (not.id === id) {
                not.time = newTime;
            }
            return not;
        });
        this.setState({
            notifications: notifications_new
        });
    };

    getData = () => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let way_id = 1;
        let type = `way/${way_id}/notification/`;

        axios.get(url + `way/${way_id}`)
            .then((response) => {
                let name = response.data.name;
                this.setState(state => ({
                    pointA: name.split('-')[0],
                    pointB: name.split('-')[1]
                }));
            });

        axios.get(url + type)
            .then((response) => {

                this.setState(state => ({
                    saved_notifications: response.data
                }));

                let start_date;
                let end_date;

                if (response.data.length === 0) {
                    start_date = '2019-01-01';
                    end_date = '2019-01-01';
                } else {
                    start_date = response.data[0].start_time;
                    end_date = response.data[0].end_time;
                }

                let parsed_start_date = new Date(start_date.substring(0, 4),
                    start_date.substring(5, 7) - 1,
                    start_date.substring(8, 10));

                let parsed_end_date = new Date(end_date.substring(0, 4),
                    end_date.substring(5, 7) - 1,
                    end_date.substring(8, 10));

                this.setState(state => ({
                    StartDate: parsed_start_date,
                    EndDate: parsed_end_date
                }));

                for (let i = 0; i <= response.data.length - 1; i++) {
                    let notifications_new = self.state.notifications.map((not) => {
                        if (not.id === response.data[i].week_day) {
                            not.time = response.data[i].time.substring(0, 5);
                            not.active = true;
                            not.db_id = response.data[i].id
                        }
                        return not;
                    });
                    this.setState({
                        notifications: notifications_new
                    });
                }
            })
    };

    componentWillUnmount() {
        this.getData();
    };

    componentDidMount() {
        this.getData();
    };

    sendRequest = () => {
        let new_notifications = this.state.notifications;
        let old_notifications = this.state.saved_notifications;

        let new_start_date = this.formatDate(this.state.StartDate);
        let old_start_date;

        if (this.state.saved_notifications.length === 0) {
            old_start_date = '2019-01-01';
        } else {
            old_start_date = this.state.saved_notifications[0].start_time;
        }

        let new_end_date = this.formatDate(this.state.EndDate);
        let old_end_date;

        if (this.state.saved_notifications.length === 0) {
            old_end_date = '2019-01-02'
        } else {
            old_end_date = this.state.saved_notifications[0].end_time;
        }

        for (let i = 0; i < new_notifications.length; i++) {
            for (let j = 0; j < old_notifications.length; j++) {
                if (new_notifications[i].id === old_notifications[j].week_day) {
                    if ((new_notifications[i].time + ':00' !== old_notifications[j].time) &&
                        new_notifications[i].active === true) {
                        this.sendUpdateTime(
                            old_notifications[j].id,
                            new_start_date,
                            new_end_date,
                            new_notifications[i].time + ':00');
                        break;
                    } else if (
                        (new_start_date !== old_start_date || new_end_date !== old_end_date) &&
                        new_notifications[i].active === true) {
                        this.sendUpdateDate(old_notifications[j].id, new_start_date, new_end_date);
                        break;
                    } else {
                        break;
                    }
                }
            }
        }
    };

    sendUpdateDate = (id, start_time, end_time) => {
        let url = '/api/v1/';
        let way_id = 1;
        let type = `way/${way_id}/notification/${id}`;
        axios.put(url + type, {
            start_time: start_time,
            end_time: end_time
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });

    };

    sendUpdateTime = (id, start_time, end_time, new_time) => {
        let url = '/api/v1/';
        let way_id = 1;
        let type = `way/${way_id}/notification/${id}`;
        axios.put(url + type, {
            start_time: start_time,
            end_time: end_time,
            time: new_time
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    sendPost = (start_time, end_time, week_day, time) => {
        let url = '/api/v1/';
        let way_id = 1;
        let type = `way/${way_id}/notification/`;
        axios.post(url + type, {
            start_time: start_time,
            end_time: end_time,
            week_day: week_day,
            time: time
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    sendDelete = (id) => {
        let url = '/api/v1/';
        let way_id = 1;
        let type = `way/${way_id}/notification/${id}`;
        axios.delete(url + type, {})
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    render() {
        return (
            <div className='notificationForm'>
                <div className='wayAB'>
                    <div className='pointA'>
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
                    <Calendar onClickDay={this.onChangeStartDate}
                              value={this.state.StartDate} />
                </div> }
                { this.state.OpenEndDate &&
                <div className='endDate'>
                    <Calendar onClickDay={this.onChangeEndDate}
                              value={this.state.EndDate} />
                </div> }
            </div>
        )
    }
}

export default NotificationForm
