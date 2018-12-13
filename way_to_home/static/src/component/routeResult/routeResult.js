import React, {Component} from 'react';
import './routeResult.css'

class ResultForm extends Component {

  constructor(props){
    super(props);

    this.state = {
    }
  }

  hideForm = () => {
      document.getElementsByClassName('resultForm')[0].style.display = 'none'
  }

  

    render() {

      return (
        <div className='resultForm'>
            <div className='resultMess'>
                <p>ТИП  |  МАРШРУТ  |   ПРИБУТТЯ ЧЕРЕЗ</p>
            </div>
            <div className='routeResult'>
                <p>&nbsp;A&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;00:02:30</p>
            </div>
            <div className='routeResult'>
                <p>&nbsp;B&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;00:03:20</p>
            </div>
            <div className='routeResult'>
                <p>&nbsp;A&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;00:05:20</p>
            </div>
            <button onClick={this.hideForm} className="hideBtnR">X</button>
        </div>
        )
    }
}

export default ResultForm