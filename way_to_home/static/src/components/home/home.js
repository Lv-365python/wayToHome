import React, {Component} from 'react';

import { StartBtn } from './index';
import './home.css';


export default class Home extends Component {
    render(){
        return(
            <div className='homeDiv'>
                <StartBtn/>
            </div>
        )
    }
}
