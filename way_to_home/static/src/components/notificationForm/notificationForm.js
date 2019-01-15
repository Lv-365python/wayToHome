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
            {id: 0, time: '09:30', text: 'ПН', active: true, openTimePicker: false},
            {id: 1, time: '08:30', text: 'ВТ', active: false, openTimePicker: false},
            {id: 2, time: '08:30', text: 'СР', active: true, openTimePicker: false},
            {id: 3, time: '08:30', text: 'ЧТ', active: false, openTimePicker: false},
            {id: 4, time: '08:30', text: 'ПТ', active: true, openTimePicker: false},
            {id: 5, time: '08:30', text: 'СБ', active: true, openTimePicker: false},
            {id: 6, time: '08:30', text: 'НД', active: false, openTimePicker: false}
        ]
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
                        <span className='not_space'></span>
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
        let url = 'http://127.0.0.1:8000/api/v1/'
        let way_id = 1
        let type = `way/${way_id}/notification/`

        axios.get(url+type)
            .then(function (response) {
                console.log(response.data.length)
                for (let i = 0; i<=response.data.length-1; i++){
                    console.log(response.data[i])
                }
            })
    }

    componentDidMount()
    {
        this.getData()
    }

    sendRequest = () => {
        let url ='http://127.0.0.1:8000/api/v1/'
        let type = ''

    }

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
