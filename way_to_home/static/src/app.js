import React from 'react';
import ReactDOM from 'react-dom';

import {
    StartBtn,
    RouteSearchForm,
    LogInBtn,
    ResultForm,
    LogInForm,
    TestApp
} from './components'

ReactDOM.render(
    <div>
        <StartBtn></StartBtn>
        <RouteSearchForm></RouteSearchForm>
        <LogInBtn></LogInBtn>
        <ResultForm></ResultForm>
        <LogInForm></LogInForm>
        <TestApp></TestApp>
    </div>,
    document.querySelector('#root')
);
