import React from 'react';
import ReactDOM from 'react-dom';

import {Header} from './components'
import {GoogleApiWrapper} from './components'

ReactDOM.render(
    <div>
        <GoogleApiWrapper/>
         <Header/>
    </div>,
    document.querySelector('#root')
);
