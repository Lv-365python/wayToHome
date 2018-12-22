import React from 'react';
import ReactDOM from 'react-dom';

import {
    StartBtn,
    RouteSearchForm,
    LogInBtn,
    ResultForm,
    LoginForm,
} from './components'

ReactDOM.render(
    <div>
        <StartBtn></StartBtn>
        <RouteSearchForm></RouteSearchForm>
        <LogInBtn></LogInBtn>
        <ResultForm></ResultForm>
        <LoginForm></LoginForm>
    </div>,
    document.querySelector('#root')
);
