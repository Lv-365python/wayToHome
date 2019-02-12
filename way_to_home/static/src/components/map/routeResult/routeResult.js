import React, {Component, Fragment} from 'react';
import './routeResult.css'

import DirectionsBusIcon from '@material-ui/icons/DirectionsBus'
import TramIcon from '@material-ui/icons/Tram'
import DirectionsWalkIcon from '@material-ui/icons/DirectionsWalk'
import TrainIcon from '@material-ui/icons/Train'

import ToggleDisplay from 'react-toggle-display';

export default class ResultForm extends Component {
    state = {
        open: true
    };

    isBus = () => {
        let style = {'display': 'flex', 'justifyContent': 'center', 'marginTop': '15%'};
         let info = this.props.routes.legs[0];

        if ((info.steps).length === 3) {
            return <td style={style} >
                {info.steps[1].transit.line.short_name}
            </td>
        } else if ((info.steps).length === 4) {
            return <td style={style} >
                {info.steps[1].transit.line.short_name}
                +
                {info.steps[2].transit.line.short_name}
            </td>
        }
        return <td>---</td>
    };

    isWalk = () => {
        return (this.props.routes.legs[0].steps).length > 1
    };

    isFare = () => {
        if ((this.props.routes.legs[0].steps).length > 5) {
            return <p></p>
        }
        if ((this.props.routes.legs[0].steps).length > 1) {
            return <p>Вартість: {this.props.routes.fare.value} грн</p>
        }
    };

    isRoute = () => {
        let info = this.props.routes.legs[0];
        if ((info.steps).length === 3) {
            return <p>
                ({parseInt(info.duration.value/60) -
            parseInt(info.steps[1].duration.value/60)}
                хв. пішки +
                {parseInt(info.steps[1].duration.value/60)}
                хв. транспортом )
            </p>
        }
        if ((info.steps).length === 4) {
            return <p>
                {parseInt((info.duration.value/60)) -
                (parseInt(info.steps[1].duration.value/60) +
                    parseInt(info.steps[2].duration.value/60))}
                хв. пішки +
                {parseInt(info.steps[1].duration.value/60) +
                parseInt(info.steps[2].duration.value/60)}
                хв. транспортом
            </p>
        }
    };

    handleTransportType = () => {
        let style = {'fontSize': '58px', 'paddingTop':'3%', 'color': 'orange'};
        let info = this.props.routes.legs[0];

        if ((info.steps).length > 1) {
            let type = info.steps[1].transit.line.vehicle.name;
            if (type === 'Share taxi' || type === 'Bus') {
                return <DirectionsBusIcon style={style}/>
            } else if (type === 'Tram') {
                return <TramIcon style={style}/>
            } else if (type === 'Trolleybus') {
                return <TrainIcon style={style}/>
            }
        } else return <DirectionsWalkIcon style={style}/>
    };


    render() {
        const {open} = this.state;

        return (

            <Fragment>
                {open  && <div className='resultForm'>
                    <div>
                        <h3 style={{'marginBottom': '4%'}}>Найоптимальніший маршрут: </h3>
                        <table className='routeInfo'>
                            <tr className='resultMess'>
                                <th>ТИП</th>
                                <th>МАРШРУТ</th>
                                <th>ВІДСТАНЬ</th>
                            </tr>
                            <tr className='routeResult'>
                                <td>{this.handleTransportType()}
                                </td>
                                {this.isBus()}
                                <td>
                                    {(this.props.routes.legs[0].distance.value/1000).toFixed(2)} км.
                                </td>
                            </tr>
                        </table>

                        <p>В дорозі: {parseInt(this.props.routes.legs[0].duration.value/60)} хв.</p>

                        <ToggleDisplay show={this.isWalk()}>
                            {this.isRoute()}
                        </ToggleDisplay>

                        <ToggleDisplay show={this.isWalk()}>
                            {this.isFare()}
                        </ToggleDisplay>

                        <h3 style={{'paddingTop': '4%'}}>Щасливої дороги!</h3>
                        <button onClick={this.props.onClose} className="hideResultForm">X</button>
                    </div>
                </div>}
            </Fragment>
        )
    }
}
