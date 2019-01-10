import React, {Component} from 'react';
import LoginBtn from '../loginBtn/loginBtn.js';
import './header.css'


class Header extends Component{
    render(){
        return(
            <div>
                <LoginBtn/>
            </div>
        )
    }
}

export default Header
