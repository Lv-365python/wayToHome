import React from 'react';
import ReactDOM from 'react-dom';

import {Header} from './components'
import {GoogleApiWrapper} from './components'

ReactDOM.render(
    <div>
        <Header/>
        <GoogleApiWrapper/>
    </div>,
    document.querySelector('#root')
);
