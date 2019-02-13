import React, {Component} from 'react';
import Button from '@material-ui/core/Button';

import { CustomizedSnackbars } from '../..';
import InputPoint from './inputPoint';
import './routeForm.css';

export default class RouteSearchForm extends Component {

    state = {
        pointA: undefined,
        pointB: undefined,
        error: undefined,
    };

    onClick = () => {
        const { pointA, pointB } = this.state;
        const markerStart = this.props.pointMarkerStart;
        const markerEnd = this.props.pointMarkerEnd;
        const choice = this.props.choice;
        if((markerStart.lat !== markerEnd.lat && markerStart.lng !== markerEnd.lng) || (pointA && pointB)){
            if(choice === 'point' && (!(pointA && pointB) || pointA === pointB)){
                this.setError("Координати початку і кінця не повинні бути одинаковими чи пустими.");
                return;
            }
            this.props.getCoordsWay();

            if(choice === 'marker') {
                this.reflectAddress();
            }
            return;
        }

        this.setError("Введіть координати початку і кінця маршруту.");
    };

    reflectAddress = () =>{
        const markerStart = this.props.pointMarkerStart;
        const markerEnd = this.props.pointMarkerEnd;
        this.props.convertToAddress(markerStart.lat, markerStart.lng, this.setPointA);
        this.props.convertToAddress(markerEnd.lat, markerEnd.lng, this.setPointB);
    };

    getCurrentPosition = point => {
        if (!navigator.geolocation){
            this.setError("Геолокація не підтримується вашим браузером.");
            return;
        }
        navigator.geolocation.getCurrentPosition(
            position => this.handleSuccess(position, point),
            () => this.setError("Неможливо отримати ваше місцезнаходження.")
        );
    };

    handleSuccess = (position, point) => {
        let setFunc = point === 'A' ? this.setPointA : this.setPointB;
        let latitude  = position.coords.latitude;
        let longitude = position.coords.longitude;
        this.props.convertToAddress(latitude, longitude, setFunc);
        this.props.setChoice('point');
    };

    setPointA = pointA => {
        this.setState({ pointA });
        this.props.setStartPoint(pointA);
    };

    setPointB = pointB => {
        this.setState({ pointB });
        this.props.setEndPoint(pointB);
    };

    setError = (value) => {
        this.setState({
            error: value
        });
    };

    render() {
        const { error, pointA, pointB } = this.state;

        return (
            <div className='searchForm'>
                <div style={{marginTop: '50px'}}></div>
                <InputPoint name='Точка A' value={ pointA } onChange={this.setPointA} setChoice={this.props.setChoice}/>
                <div style={{marginTop: '50px'}}></div>
                <InputPoint name='Точка Б' value={ pointB } onChange={this.setPointB} setChoice={this.props.setChoice}/>
                <div style={{marginTop: '60px'}}></div>
                <Button variant='contained' color='primary' size='medium' onClick={this.onClick} className='Btn'>
                    ПОШУК
                </Button>
                { error && <CustomizedSnackbars message={error} reset={this.setError}/>}
                <button onClick={this.props.onClose} className="hideBtn">X</button>
                <button onClick={() => this.getCurrentPosition('A')} className="currPosBtn_1">O</button>
                <button onClick={() => this.getCurrentPosition('B')} className="currPosBtn_2">O</button>
            </div>
        )
    }
}
