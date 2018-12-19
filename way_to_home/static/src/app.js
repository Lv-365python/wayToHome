import React from 'react';
import ReactDOM from 'react-dom';

import {StartBtn, RouteSearchForm, LogInBtn, ResultForm, LogInForm} from './components'

ReactDOM.render(
    <div>
        <StartBtn></StartBtn>
        <RouteSearchForm></RouteSearchForm>
        <LogInBtn></LogInBtn>
        <ResultForm></ResultForm>
        <LogInForm></LogInForm>
    </div>,
    document.querySelector('#root')
);
