import React, {Component} from 'react';
import StartBtn from '../startBtn/startBtn.js';
import LoginBtn from '../loginBtn/loginBtn.js';
import './header.css'


class Header extends Component{
    render(){
        return(
            <div>
                <StartBtn/>
                <LoginBtn/>
            </div>
        )
    }
}

export default Header
