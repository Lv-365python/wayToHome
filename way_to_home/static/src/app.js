import React from 'react';
import ReactDOM from 'react-dom';

import {
    StartBtn,
    RouteSearchForm,
    LoginBtn,
    ResultForm,
} from './components'

ReactDOM.render(
    <div>
        <StartBtn/>
        <RouteSearchForm/>
        <LoginBtn/>
        <ResultForm/>
    </div>,
    document.querySelector('#root')
);
