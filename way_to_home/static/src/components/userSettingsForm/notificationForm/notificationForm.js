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
        ]
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
        });
    };

    toggleStartDate = () => {
        this.setState(state => ({
            OpenStartDate: !state.OpenStartDate
        }));
    };

    toggleEndDate = () => {
        this.setState(state => ({
            OpenEndDate: !state.OpenEndDate
        }));
    };

    onChangeStartDate = (newDate) => {

        if (newDate >= this.state.EndDate){
            alert('Початкова дата не може бути більшою або рівною за кінцеву')
        } else {
            this.setState({StartDate: newDate});

            let new_notifications = this.state.notifications;

            for (let i = 0; i < new_notifications.length; i++) {
                if (new_notifications[i].db_id !== 0 && new_notifications[i].active === true) {
                    this.sendUpdateDate(
                        new_notifications[i].db_id,
                        this.formatDate(newDate),
                        this.formatDate(this.state.EndDate)
                    );
                }
            }

            this.toggleStartDate();
        }
    };

    onChangeEndDate = (newDate) => {
        if (newDate <= this.state.StartDate){
            alert('Кінцева дата не може бути меншою або рівною за початкову')
        } else {
            this.setState({EndDate: newDate});

            let new_notifications = this.state.notifications;

            for (let i = 0; i < new_notifications.length; i++) {
                if (new_notifications[i].db_id !== 0 && new_notifications[i].active === true) {
                    this.sendUpdateDate(
                        new_notifications[i].db_id,
                        this.formatDate(this.state.StartDate),
                        this.formatDate(newDate),
                    );
                }
            }

            this.toggleEndDate();
        }
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
        });
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

        let new_notifications = this.state.notifications;

        for (let i = 0; i < new_notifications.length; i++) {
            if (new_notifications[i].db_id !== 0 && new_notifications[i].id === id) {
                this.sendUpdateTime(
                    new_notifications[i].db_id,
                    this.formatDate(this.state.StartDate),
                    this.formatDate(this.state.EndDate),
                    new_notifications[i].time + ':00')
            }
        }
    };

    getData = () => {
        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/`;

        axios.get(url + `way/${this.props.way.id}`)
            .then((response) => {
                let name = response.data.name;
                this.setState(state => ({
                    pointA: name.split('-')[0],
                    pointB: name.split('-')[1]
                }));
            });

        axios.get(url + type)
            .then((response) => {

                let start_date;
                let end_date;

                let new_date = new Date();

                if (response.data.length === 0) {
                    start_date = '2019-01-01';
                    end_date = String(this.formatDate(new_date));
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

                this.setState(() => ({
                    StartDate: parsed_start_date,
                    EndDate: parsed_end_date
                }));

                for (let i = 0; i <= response.data.length - 1; i++) {
                    let notifications_new = this.state.notifications.map((not) => {
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

    componentDidMount() {
        this.getData();
    };

    sendUpdateDate = (id, start_time, end_time) => {
        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/${id}`;
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
        let type = `way/${this.props.way.id}/notification/${id}`;
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
        let type = `way/${this.props.way.id}/notification/`;
        axios.post(url + type, {
            start_time: start_time,
            end_time: end_time,
            week_day: week_day,
            time: time + ':00'
        })
            .then( (response) => {
                let notifications_new = this.state.notifications.map((item) => {
                    if (item.id === response.data.week_day) {
                        item.time = response.data.time.substring(0, 5);
                        item.active = true;
                        item.db_id = response.data.id
                    }
                    return item;
                });
                this.setState({
                    notifications: notifications_new
                });
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    sendDelete = (id) => {
        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/${id}`;
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
                    <p>{this.formatDate(this.state.StartDate)}</p>
                </div>
                <div className='pickEndDate' onClick={this.toggleEndDate}>
                    <p>{this.formatDate(this.state.EndDate)}</p>
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
            </div>
        )
    }
}

export default NotificationForm
