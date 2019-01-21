import React from 'react';
import ReactDOM from 'react-dom';
import Router from 'react-router-dom/BrowserRouter';

import MainRouter from './main_router'
import Header from "src/components/header/header";

ReactDOM.render(
    <Router>
        <div>
            <Header/>
            <MainRouter/>
        </div>
    </Router>,
    document.getElementById('root')
);
