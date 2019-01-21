import React, {Component} from 'react';
import MapLeaflet from "../map/map"

export default class Home extends Component{
    render(){
        return(
            <div>
              <MapLeaflet />
            </div>
        )
    }
}
