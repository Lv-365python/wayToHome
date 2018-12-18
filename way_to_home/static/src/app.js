import React from 'react';
import ReactDOM from 'react-dom';

import {StartBtn, RouteSearchForm, LogInBtn, ResultForm} from './components'

ReactDOM.render(
    <div>
        <StartBtn></StartBtn>
        <RouteSearchForm></RouteSearchForm>
        <LogInBtn></LogInBtn>
        <ResultForm></ResultForm>
    </div>,
    document.querySelector('#root')
);

