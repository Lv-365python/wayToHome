import React, {Component} from 'react';
import StartBtn from '../startBtn/startBtn';
import './home.css';

class Home extends Component {
    render(){
        return(
            <div className='homeDiv'>
                <StartBtn/>
            </div>
        )
    }
}

export default Home;
