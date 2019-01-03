import React, {Component, Fragment} from 'react';
import './routeResult.css'

class ResultForm extends Component {

  constructor(props){
    super(props);

    this.state = {
        show: true
    }
  }

  hideForm = () => {
            this.setState({
             show: false
         });
  }


    render() {
    const {show} = this.state
      return (
          <Fragment>
              {show  && <div className='resultForm'>
                <div className='resultMess'>
                    <p>ТИП  |  МАРШРУТ  |   ПРИБУТТЯ ЧЕРЕЗ</p>
                </div>
                <div className='routeResult'>
                    <p> A   |     5     |      00:02:30</p>
                </div>
                <div className='routeResult'>
                    <p> B   |     4     |      00:02:30</p>
                </div>
                <div className='routeResult'>
                    <p> A   |     3     |      00:02:30</p>
                </div>
                <button onClick={this.hideForm} className="hideBtnR">X</button>
            </div>}
          </Fragment>
        )
    }
}

export default ResultForm
