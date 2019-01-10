import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Home from './components/home/home';


export default class MainRouter extends React.Component {
    render(){
        console.log("123")
        return (
            <main>
                <Switch>
                    <Route path="/home" component={Home}/>
                    <Redirect path="*" to="/home"/>
                </Switch>
            </main>
        )
    }
}