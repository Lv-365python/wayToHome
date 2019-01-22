import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import ResultForm from '../routeResult/routeResult';
import InputPoint from './inputPoint';
import axios from 'axios';
import CustomizedSnackbars from '../message/message';
import './routeForm.css';


class RouteSearchForm extends Component {


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
            this.setError("Geolocation is not supported by your browser");
            return;
        }
        navigator.geolocation.getCurrentPosition(
            position => this.handleSuccess(position, point),
            () => this.handleError("Unable to retrieve your location")
        );
    };

    handleSuccess = (position, point) => {
        let latitude  = position.coords.latitude;
        let longitude = position.coords.longitude;
        let url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat='+latitude+'&lon='+longitude;
        axios.get(url)
            .then(response => {
                const address = this.getAddress(response);
                if (point === 'A'){
                    this.setPointA(address);
                }else{
                    this.setPointB(address);
                }
            })
            .catch(error => {
                    this.setError(error.response.data);
            });
    }

    getAddress = response => {
        const data = response.data.address;
        let addr = `${data.town || data.city}, ${data.road}`;

        if (data.house_number) {
            addr += `, ${data.house_number}`;
        }

        if (addr.includes("undefined")){
            addr = "Неможливо визначити.";
        }
        return addr;
    }

    handleError = error => {
        this.setError(error);
    }

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
                <InputPoint name='Point A' value={this.state.pointA} onChange={this.setPointA}/>
                <div style={{marginTop: '50px'}}></div>
                <InputPoint name='Point B' value={this.state.pointB} onChange={this.setPointB}/>
                <div style={{marginTop: '60px'}}></div>
                <Button variant='contained' color='primary' size='medium' onClick={this.onClick} className='Btn'>
                    ПОШУК
                </Button>
                { error && <CustomizedSnackbars message={this.state.error} reset={this.setError}/>}
                <button onClick={this.props.onClose} className="hideBtn">X</button>
                <button onClick={() => this.getCurrentPosition('A')} className="currPosBtn_1">O</button>
                <button onClick={() => this.getCurrentPosition('B')} className="currPosBtn_2">O</button>
                { open && <ResultForm onClose={this.closeRouteResult}/>}
            </div>
        )
    }
}

export default RouteSearchForm
