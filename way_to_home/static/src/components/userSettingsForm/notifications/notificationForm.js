import React, {Component} from 'react';
import axios from 'axios';
import Button from "@material-ui/core/Button";
import CustomizedSnackbars from '../../message/message';
import NotificationItem from './notificationItem/notificationItem';
import NewNotificationItem from './newNotificationItem/newNotificationItem'
import './notificationForm.css';
import Calendar from "react-calendar";
import Chip from "@material-ui/core/Chip/Chip";
import TrendingFlat from '@material-ui/icons/TrendingFlat';


class NotificationForm extends Component{

    state = {
        pointA: String(undefined),
        pointB: String(undefined),
        OpenStartDate: false,
        OpenEndDate: false,
        StartDate: new Date(),
        EndDate: new Date(),
        notifications: [],
        newNotifications: [],
        ajaxError: undefined,
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
                if (response.status === 200) {

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

                    this.setState({notifications: response.data});
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError("Не вдалося завантантажити нотифікації"));
    };

    componentDidMount() {
        alert('dsgsdfg')
        this.getData();
    };

    handleAddButtonClick = () => {
        this.setState({
            newNotifications: [{time: ''}],
        })
    };

    handleDeleteNewItemClick = () => {
        this.setState({
            newNotifications: []
        })
    };

    setError = (error) => {
        this.setState({ajaxError: error});
    };

    handleDeleteExistItemClick = (id) => {
        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/${id}`;
        axios.delete(url + type)
            .then( (response) => {
                if (response.status === 200 ) {
                    let notifications = this.state.notifications.filter(notification => notification.id !== id);
                    this.setState({notifications: notifications})
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError(error));
    };

    handleSaveClick = (week_day, time) => {
        let url = '/api/v1/';
        let type = `way/${this.props.way.id}/notification/`;
        axios.post(url + type, {
            start_time: this.formatDate(this.state.StartDate),
            end_time: this.formatDate(this.state.EndDate),
            week_day: week_day,
            time: time + ':00'
        })
            .then(response => {
                if (response.status === 201) {
                    this.setState({
                        notifications: [...this.state.notifications, response.data],
                        newNotifications: []
                    })
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError(error));
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

            this.state.notifications.map(notification => {
                this.sendUpdateDate(
                    notification.id,
                    this.formatDate(newDate),
                    this.formatDate(this.state.EndDate)
                );
            });
            this.toggleStartDate();
        }
    };

    onChangeEndDate = (newDate) => {
        let today = new Date();
        if (newDate <= this.state.StartDate || newDate <= today){
            alert('Кінцева дата не може бути меншою або рівною за початкову та сьогоднішню дату')
        } else {
            this.setState({EndDate: newDate});

            this.state.notifications.map(notification => {
                this.sendUpdateDate(
                    notification.id,
                    this.formatDate(this.state.StartDate),
                    this.formatDate(newDate)
                );
            });
            this.toggleEndDate();
        }
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

    render(){
        return(
            <div>
                <div className='notificationForm'>
                    <div className="wayName">
                        <Chip
                            className="wayNames"
                            color="primary"
                            label={this.state.pointA.toUpperCase()}
                            variant="default" />
                        <TrendingFlat className="notificationArrow"/>
                        <Chip
                            className="wayNames"
                            color="primary"
                            label={this.state.pointB.toUpperCase()}
                            variant="default" />
                    </div>

                    {this.state.notifications.map(notification => (
                        <NotificationItem
                            key={Date.now()}
                            id={notification.id}
                            time={notification.time}
                            week_day={notification.week_day}
                            start_date={this.state.StartDate}
                            end_date={this.state.EndDate}
                            way={this.props.way}
                            deleteButton={this.handleDeleteExistItemClick} /> ))}

                    {this.state.newNotifications.map(notification => (
                        <NewNotificationItem
                            key={Date.now()}
                            deleteButton={this.handleDeleteNewItemClick}
                            saveNotification={this.handleSaveClick}
                            setError={this.setError} /> ))}

                    <div className="addButton" >
                        <Button
                            variant="contained"
                            size="medium"
                            color="primary"
                            onClick={this.handleAddButtonClick}
                            disabled={this.state.newNotifications.length > 0 ? true : false} >
                            Додати нотифікацію
                        </Button>
                    </div>
                    <div className="pickStartDate" >
                        <Button
                            variant="contained"
                            size="medium"
                            color="primary"
                            onClick={this.toggleStartDate} >
                            Змінити початкову дату: {this.formatDate(this.state.StartDate)}
                        </Button>
                    </div>
                    <div className="pickEndDate" >
                        <Button
                            variant="contained"
                            size="medium"
                            color="primary"
                            onClick={this.toggleEndDate} >
                            Змінити кінцеву дату: {this.formatDate(this.state.EndDate)}
                        </Button>
                    </div>
                    <div className="returnButton" >
                        <Button
                            variant="contained"
                            size="medium"
                            color="secondary"
                            onClick={this.props.toggleNotificationForm}>
                            Повернутись
                        </Button>
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
                    {this.state.ajaxError && <CustomizedSnackbars message={this.state.ajaxError} reset={this.setError}/>}
                </div>
            </div>
        )
    }
}

export default NotificationForm;
