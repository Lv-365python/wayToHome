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
        openStartDate: false,
        openEndDate: false,
        startDate: new Date(),
        endDate: new Date(),
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
                        startDate: parsed_start_date,
                        endDate: parsed_end_date
                    }));

                    this.setState({notifications: response.data});
                } else {
                    this.setError("Не вдалося завантажити нотифікації");
                }
            })
            .catch(error => this.setError("Не вдалося завантажити нотифікації"));
    };

    componentDidMount() {
        this.getData();
    };

    handleAddButtonClick = () => {
        this.setState({
            newNotifications: [{}],
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
                    this.setError("Не вдалося видалити нотифікацію");
                }
            })
            .catch(error => this.setError("Не вдалося видалити нотифікацію"));
    };

    handleSaveClick = (notification) => {
        let notifications = [...this.state.notifications, notification];

        this.setState({
            notifications: notifications,
            newNotifications: []
        })
    };

    toggleStartDate = () => {
        this.setState(state => ({
            openStartDate: !state.openStartDate
        }));
    };

    toggleEndDate = () => {
        this.setState(state => ({
            openEndDate: !state.openEndDate
        }));
    };

    onChangeStartDate = (newDate) => {
        if (newDate >= this.state.EndDate){
            this.setError('Початкова дата не може бути більшою або рівною за кінцеву')
        } else {
            this.setState({startDate: newDate});

            this.state.notifications.map(notification => {
                this.sendUpdateDate(
                    notification.id,
                    this.formatDate(newDate),
                    this.formatDate(this.state.endDate)
                );
            });
            this.toggleStartDate();
        }
    };

    onChangeEndDate = (newDate) => {
        let today = new Date();
        if (newDate <= this.state.startDate || newDate <= today){
            this.setError('Кінцева дата не може бути меншою або рівною за початкову та сьогоднішню дату')
        } else {
            this.setState({EndDate: newDate});

            this.state.notifications.map(notification => {
                this.sendUpdateDate(
                    notification.id,
                    this.formatDate(this.state.startDate),
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
            .catch(error => this.setError("Не вдалося обновити нотифікацію"))
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
                            key={notification.id}
                            id={notification.id}
                            time={notification.time}
                            week_day={notification.week_day}
                            start_date={this.state.startDate}
                            end_date={this.state.endDate}
                            way={this.props.way}
                            deleteButton={this.handleDeleteExistItemClick} /> ))}

                    {this.state.newNotifications.map(() => (
                        <NewNotificationItem
                            key={Date.now()}
                            deleteButton={this.handleDeleteNewItemClick}
                            startDate={this.state.startDate}
                            endDate={this.state.endDate}
                            way={this.props.way}
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
                            Змінити початкову дату: {this.formatDate(this.state.startDate)}
                        </Button>
                    </div>
                    <div className="pickEndDate" >
                        <Button
                            variant="contained"
                            size="medium"
                            color="primary"
                            onClick={this.toggleEndDate} >
                            Змінити кінцеву дату: {this.formatDate(this.state.endDate)}
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
                    { this.state.openStartDate &&
                    <div className='startDate'>
                        <Calendar onChange={this.onChangeStartDate}
                                  value={this.state.startDate} />
                    </div> }
                    { this.state.openEndDate &&
                    <div className='endDate'>
                        <Calendar onChange={this.onChangeEndDate}
                                  value={this.state.endDate} />
                    </div> }
                    {this.state.ajaxError && <CustomizedSnackbars message={this.state.ajaxError} reset={this.setError}/>}
                </div>
            </div>
        )
    }
}

export default NotificationForm;
