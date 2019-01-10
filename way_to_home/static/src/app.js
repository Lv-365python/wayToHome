import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router} from 'react-router-dom';

import {Header} from './components'
import MainRouter from './main_router'

ReactDOM.render(
    <Router>
        <div>
            <Header/>
            <MainRouter/>
        </div>
    </Router>,
    document.getElementById('root')
);
