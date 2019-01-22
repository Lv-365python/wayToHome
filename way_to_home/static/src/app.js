import React from 'react';
import ReactDOM from 'react-dom';
import Router from 'react-router-dom/BrowserRouter';

import MainRouter from './main_router'

ReactDOM.render(
    <Router>
        <div>
            <MainRouter/>
        </div>
    </Router>,
    document.getElementById('root')
);
