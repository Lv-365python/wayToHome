import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import {Home, UserSettingsForm, Header, Map} from './components';
import SetNewPassword from './components/confirm_reset_pass/SetNewPassword';
import ToggleDisplay from 'react-toggle-display';

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
      state = {
            show: true,
    };

    isResetPass = () => {
        let token = /^http:\/\/localhost:8000\/reset_password\/[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$/;
        if(token.test(window.location.href))
            return false
    };

    render(){
        return (
            <main>
                <ToggleDisplay show={this.isResetPass()}>
                    <Header/>
                </ToggleDisplay>
                <Map/>
                <Switch>
                    <Route path="/home" component={Home}/>
                    <Route path="/reset_password/:token" component={SetNewPassword} />
                    <PrivateRoute path="/profile" component={UserSettingsForm}/>
                    <Redirect path="*" to="/home"/>
                </Switch>
            </main>
        )
    }
}
