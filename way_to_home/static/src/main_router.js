import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import {Home, UserSettingsForm, Header, Map} from './components';

export const isAuthenticated = function() {
    return document.cookie.indexOf('sessionid') !== -1;
};


function PrivateRoute({ component: Component, ...rest }) {
  return (
    <Route
      {...rest}
      render={props =>
        isAuthenticated() ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{
              pathname: "/home",
              state: { from: props.location }
            }}
          />
        )
      }
    />
  );
}


export default class MainRouter extends React.Component {
    render(){
        return (
            <main>
                <Header/>
                <Map/>
                <Switch>
                    <Route path="/home" component={Home}/>
                    <PrivateRoute path="/profile" component={UserSettingsForm}/>
                    <Redirect path="*" to="/home"/>
                </Switch>
            </main>
        )
    }
}
