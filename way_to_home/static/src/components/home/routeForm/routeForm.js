import React, {Component} from 'react';
import axios from 'axios';

import Button from '@material-ui/core/Button';

import { CustomizedSnackbars } from '../../index';
import { ResultForm } from '../index';
import InputPoint from './inputPoint';
import './routeForm.css';


export default class RouteSearchForm extends Component {

    state = {
        pointA: undefined,
        pointB: undefined,
        open: false,
        error: undefined,
    };

    onClick = () => {
        this.setState((state) => ({
            open: !state.open
        }));
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
        let latitude  = position.coords.latitude;
        let longitude = position.coords.longitude;
        let url = 'https://nominatim.openstreetmap.org/reverse';
        axios.get(url, {
            params: {
                format: 'jsonv2',
                lat: latitude,
                lon: longitude
            }
        })
            .then(response => {
                const address = this.getAddress(response);
                if (point === 'A')
                    this.setPointA(address);
                else
                    this.setPointB(address);
            })
            .catch(error => {
                this.setError("Неможливо визначити адресу.");
            });
    };

    getAddress = response => {
        const address = response.data.address;
        let addr = `${address.town || address.city}, ${address.road || address.path || address.suburb}`;

        if (address.house_number)
            addr += `, ${address.house_number}`;

        if (addr.includes("undefined"))
            addr = "Неможливо визначити вашу геолокацію.";

        return addr;
    };

    setPointA = pointA => {
        this.setState({ pointA });
    };

    setPointB = pointB => {
        this.setState({ pointB });
    };

    closeRouteResult = () =>{
        this.setState({
            open: false
        });
    };

    setError = (value) => {
        this.setState({
            error: value
        });
    };

    render() {
        const { open, error } = this.state;

        return (
            <div className='searchForm'>
                <div style={{marginTop: '50px'}}></div>
                <InputPoint name='Точка A' value={this.state.pointA} onChange={this.setPointA}/>
                <div style={{marginTop: '50px'}}></div>
                <InputPoint name='Точка Б' value={this.state.pointB} onChange={this.setPointB}/>
                <div style={{marginTop: '60px'}}></div>
                <Button variant='contained' color='primary' size='medium' onClick={this.onClick} className='Btn'>
                    ПОШУК
                </Button>
                { error && <CustomizedSnackbars message={error} reset={this.setError}/>}
                <button onClick={this.props.onClose} className="hideBtn">X</button>
                <button onClick={() => this.getCurrentPosition('A')} className="currPosBtn_1">O</button>
                <button onClick={() => this.getCurrentPosition('B')} className="currPosBtn_2">O</button>
                { open && <ResultForm onClose={this.closeRouteResult}/>}
            </div>
        )
    }
}
