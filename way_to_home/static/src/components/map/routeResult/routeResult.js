import React, {Component, Fragment} from 'react';
import './routeResult.css'


export default class ResultForm extends Component {
    state = {
        open: true
    };

    hideForm = () => {
        this.setState({
            open: false
        });
    };

    render() {

        const { open } = this.state;

        return (
            <Fragment>
                {open  && <div className='resultForm'>
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
