import React, {Component} from 'react';
import LoginBtn from '../loginBtn/loginBtn.js';
import StartBtn from "../startBtn/startBtn.js";
import './header.css';


export default class Header extends Component{
    render(){
        return(
            <div>
                <StartBtn/>
                <LoginBtn/>
            </div>
        )
    }
}
