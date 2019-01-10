import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router} from 'react-router-dom';

import MainRouter from './main_router'

ReactDOM.render(
    <Router>
        <div>
            <MainRouter/>
        </div>
    </Router>,
    document.getElementById('root')
);
