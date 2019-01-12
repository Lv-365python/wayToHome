import React, {Component} from 'react';
import Calendar from 'react-calendar'
import TimePicker from 'react-time-picker';
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
            {id: 1, time: '08:30', text: 'ПН', active: true},
            {id: 2, time: '08:30', text: 'ВТ', active: false},
            {id: 3, time: '08:30', text: 'СР', active: true },
            {id: 4, time: '08:30', text: 'ЧТ', active: false},
            {id: 5, time: '08:30', text: 'ПТ', active: true},
            {id: 6, time: '08:30', text: 'СБ', active: true},
            {id: 7, time: '08:30', text: 'НД', active: false}
        ]
    }

    showList = () => {
        return (
            <div>
                {this.state.notifications.map((not) => (
                    <li className={`not-done-${not.active} notification`}
                        onClick={() => this.updateNotActive(not.id)}>
                        <span>{not.time}</span>
                        >----->
                        {not.text}
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
            </div>
        );
    }
}

export default NotificationForm
