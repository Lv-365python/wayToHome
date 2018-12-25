import React from 'react';
import ReactDOM from 'react-dom';

import {
    StartBtn,
    RouteSearchForm,
    LoginBtn,
    ResultForm,
    SignupForm,
} from './components'

ReactDOM.render(
    <div>
        <StartBtn/>
        <RouteSearchForm/>
        <LoginBtn/>
        <ResultForm/>
        <SignupForm/>
    </div>,
    document.querySelector('#root')
);
