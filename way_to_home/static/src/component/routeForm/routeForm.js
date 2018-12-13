import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
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
            onChange={this.handleChange}
          />
        </div>)
    }
}

class RouteSearchForm extends Component {

  constructor(props){
    super(props);

    this.state = {
      pointA: undefined,
      pointB: undefined,
    }
  }

  onClick = () => {
    this.sendRequest();
    this.openResultForm();
  }

  sendRequest = () => {
    alert(this.state.pointA + ' ' + this.state.pointB)
  }

  hideForm = () => {
    document.getElementsByClassName('searchForm')[0].style.display = 'none'
  }
  
  openResultForm = () => {
    document.getElementsByClassName('resultForm')[0].style.display = 'block'
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

    render() {

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
          <button onClick={this.hideForm} className="hideBtn">X</button>
          <button onClick={this.getCurrentPosition} className="currPosBtn_1">O</button>
          <button onClick={this.getCurrentPosition} className="currPosBtn_2">O</button>
        </div>
        )
    }
}

export default RouteSearchForm

