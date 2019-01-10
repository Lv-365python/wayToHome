import React, {Component, Fragment} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ResultForm from '../routeResult/routeResult.js';
import './routeForm.css'
import axios from 'axios';

class TextFields extends Component {

  constructor(props){
    super(props);

    this.state = {
      name: this.props.name,
      value: this.props.value,
      multiline: 'Controlled',
    }
  }

  handleChange = event => {
      console.log('event', event);
      let value = event.target.value;
      if (value.length > 3){
        this.props.onChange(value)
      }else{
        this.props.onChange(undefined);
      }
  };

    render() {
      return (
        <Fragment>
          <TextField
            label={this.props.name}
            value={this.props.value}
            InputLabelProps={{ shrink: true }}
            onChange={this.handleChange}/>
        </Fragment>
      )
    }
};

class RouteSearchForm extends Component {

  constructor(props){
    super(props);

    this.state = {
        pointA: undefined,
        pointB: undefined,
        open: false,
    }
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
         axios.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat='+latitude+'&lon='+longitude+'')
            .then(function (response) {
                let addr = response.data.address.city + ', ' + response.data.address.road + ', ' + response.data.address.house_number
                if (props == 'A') {
                    self.setPointA(addr)
                }else{
                    self.setPointB(addr)
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        }

      function error() {
          console.log("Unable to retrieve your location")
        }

      navigator.geolocation.getCurrentPosition(success, error)
  }

  setPointA = (value) => {
    this.setState({pointA: value});
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
          <TextFields name='Point A' value={this.state.pointA} onChange={this.setPointA}/>
          <div style={{marginTop: '50px'}}></div>
          <TextFields name='Point B' value={this.state.pointB} onChange={this.setPointB}/>
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
