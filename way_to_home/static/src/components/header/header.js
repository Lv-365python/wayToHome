import React, {Component} from 'react';
import LoginBtn from '../loginBtn/loginBtn.js';
import './header.css'
import StartBtn from "../startBtn/startBtn.js";


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
