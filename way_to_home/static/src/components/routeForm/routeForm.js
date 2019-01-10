import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import ResultForm from '../routeResult/routeResult';
import InputPoint from './inputPoint';
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
            open: false
         });
  }

    render() {
      const { open } = this.state;

      return (
        <div className='searchForm'>
          <div style={{marginTop: '50px'}}></div>
          <InputPoint name='Point A' onChange={this.setPointA}/>
          <div style={{marginTop: '50px'}}></div>
          <InputPoint name='Point B' onChange={this.setPointB}/>
          <div style={{marginTop: '60px'}}></div>
            <Button variant='contained' color='primary' size='medium' onClick={this.onClick} className='Btn'>
              ПОШУК
            </Button>
            <button onClick={this.props.onClose} className="hideBtn">X</button>
            <button onClick={this.getCurrentPosition} className="currPosBtn_1">O</button>
            <button onClick={this.getCurrentPosition} className="currPosBtn_2">O</button>
            { open && <ResultForm onClose={this.closeRouteResult}/>}
        </div>
        )
    }
}

export default RouteSearchForm
