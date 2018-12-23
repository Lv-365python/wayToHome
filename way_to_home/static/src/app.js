import React from 'react';
import ReactDOM from 'react-dom';

import {
    StartBtn,
    RouteSearchForm,
    LogInBtn,
    ResultForm,
    LoginForm,
    SignupForm,
} from './components'

ReactDOM.render(
    <div>
        <StartBtn></StartBtn>
        <RouteSearchForm></RouteSearchForm>
        <LogInBtn></LogInBtn>
        <ResultForm></ResultForm>
        <LoginForm></LoginForm>
        <SignupForm></SignupForm>
    </div>,
    document.querySelector('#root')
);
