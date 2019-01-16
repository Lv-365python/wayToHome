import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router} from 'react-router-dom';

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
