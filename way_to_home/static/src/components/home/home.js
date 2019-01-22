import React, {Component} from 'react';
import StartBtn from '../startBtn/startBtn';
import MapLeaflet from "../map/map"

class Home extends Component {
    render(){
        return(
            <div>
                <StartBtn/>
              <MapLeaflet />
            </div>
        )
    }
}

export default Home;
