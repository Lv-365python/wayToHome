import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import './userSettingsForm.css';


class userSettingsForm extends React.Component {
  state = {
    value: 0,
  };

  handleChange = (event, value) => {
    this.setState({ value });
  };

  render() {
    const { value } = this.state;

    return (
      <div className="settingsForm">
        <AppBar position="static">
          <Tabs value={value} onChange={this.handleChange}>
            <Tab label="Профіль" />
            <Tab label="Шляхи" />
          </Tabs>
        </AppBar>
          {value === 0 && <div>asdasdas</div>}
          {value === 1 && <div>vbbcbbcccv</div>}
      </div>
    );
  }
}

export default userSettingsForm;
