import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import {Home, UserSettings, Header} from './components';


export default class MainRouter extends React.Component {
    render(){
        return (
            <main>
                <Header/>
                <Switch>
                    <Route path="/home" component={Home}/>
                    <Route path="/settings" component={UserSettings}/>
                    <Redirect path="*" to="/home"/>
                </Switch>
            </main>
        )
    }
}
