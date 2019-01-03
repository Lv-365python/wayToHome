import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ResultForm from '../routeResult/routeResult.js';
import './routeForm.css'

class TextFields extends Component {

  constructor(props){
    super(props);

    this.state = {
      name: this.props.name,
      value: undefined,
      multiline: 'Controlled',
    }
  }

  handleChange = event => {
      let value = event.target.value;
      if (value.length > 3){
        this.props.onChange(value)
      }else{
        this.props.onChange(undefined);
      }
  };

    render() {

      return (
        <div>
          <TextField
            label={this.state.name}
            value={this.state.value}
            onChange={this.handleChange}/>
        </div>
      )
    }
};

class RouteSearchForm extends Component {

  constructor(props){
    super(props);

    this.state = {
        pointA: undefined,
        pointB: undefined,
        isRouteResult: false
    }
  }

  onClick = () => {
    this.setState((state) => ({
        isRouteResult: !state.isRouteResult
    }));
  }

   getCurrentPosition = () => {
     alert('get and write current position')
   }

  setPointA = (value) => {
    this.setState({pointA: value})
  }

  setPointB = (value) => {
    this.setState({pointB: value})
  }

  closeRouteResult = () =>{
      this.setState({
             isRouteResult: false
         });
  }

    render() {
      const { isRouteResult } = this.state;

      return (
        <div className='searchForm'>
          <div style={{marginTop: '50px'}}></div>
          <TextFields name='Point A' onChange={this.setPointA}/>
          <div style={{marginTop: '50px'}}></div>
          <TextFields name='Point B' onChange={this.setPointB}/>
          <div style={{marginTop: '60px'}}></div>
            <Button variant='contained' color='primary' size='medium' onClick={this.onClick} className='Btn'>
              ПОШУК
            </Button>
            <button onClick={this.props.onClose} className="hideBtn">X</button>
            <button onClick={this.getCurrentPosition} className="currPosBtn_1">O</button>
            <button onClick={this.getCurrentPosition} className="currPosBtn_2">O</button>
            { isRouteResult && <ResultForm onClose={this.closeRouteResult}/>}
        </div>
        )
    }
}

export default RouteSearchForm
