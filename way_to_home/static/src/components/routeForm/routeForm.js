import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import ResultForm from '../routeResult/routeResult';
import InputPoint from './inputPoint';
import axios from 'axios';
import './routeForm.css';


class RouteSearchForm extends Component {


    state = {
        pointA: undefined,
        pointB: undefined,
        open: false
    }

  onClick = () => {
    this.setState((state) => ({
        open: !state.open
    }));
  }

   getCurrentPosition = (props) => {
      if (!navigator.geolocation){
        console.log("Geolocation is not supported by your browser")
        return;
      }
      self = this
      function success(position) {
        let latitude  = position.coords.latitude;
        let longitude = position.coords.longitude;
        let url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat='+latitude+'&lon='+longitude
         axios.get(url)
            .then(function (response) {
                let addr = response.data.address.city + ', ' + response.data.address.road;
                if (response.data.address.house_number){
                    addr += ", " + response.data.address.house_number;
                }
                props == 'A' ? self.setPointA(addr) :  self.setPointB(addr);
            })
            .catch(function (error) {
                throw error;
            });
        }

      function error() {
         throw "Unable to retrieve your location";
        }

      navigator.geolocation.getCurrentPosition(success, error)
  }

  setPointA = (value) => {
    this.setState({pointA: value})
  }

  setPointB = (value) => {
    this.setState({pointB: value})
  }

  closeRouteResult = () =>{
      this.setState({
            open: false
         });
  }

    render() {
      const { open } = this.state;

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
            <button onClick={this.props.onClose} className="hideBtn">X</button>
            <button onClick={() => this.getCurrentPosition('A')} className="currPosBtn_1">O</button>
            <button onClick={() => this.getCurrentPosition('B')} className="currPosBtn_2">O</button>
            { open && <ResultForm onClose={this.closeRouteResult}/>}
        </div>
        )
    }
}

export default RouteSearchForm
