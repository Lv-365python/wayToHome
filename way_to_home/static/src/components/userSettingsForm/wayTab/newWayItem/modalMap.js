import React from 'react';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import './newWayItem.css';


class ModalMap extends React.Component {
  state = {
      listRoutes: [],
  };


  componentWillMount() {
      let listRoutes = [];
      this.props.routes.map(route => {
          let busInfo = [];
          route.Sections.Sec.map(sec => {
              if (sec.mode !==20 ){
                  busInfo.push(sec.Dep.Transport.name)
              }
          });
          listRoutes.push({
              routeInfo: route,
              busInfo: busInfo,
              duration: route.duration,
          })
      });
      this.setState({listRoutes: listRoutes})
  }

    render() {
      const { listRoutes } = this.state;

      return (
          <div>
              <DialogTitle>Виберіть маршрут</DialogTitle>
              <DialogContent>
                  {listRoutes.map(route => (
                      <div key={route.routeInfo.id}>
                          <p>
                              Тривалість: { route.duration } ;
                              Транспорт № { route.busInfo.join() } ;

                              <Button
                                  variant="outlined"
                                  style={{color:"green"}}
                                  onClick={() => this.props.saveRoute(route.routeInfo.Sections.Sec)}
                              >
                                  Вибрати
                              </Button>
                          </p>
                      </div>
                  ))}
              </DialogContent>
              <DialogActions>

                  <Button
                      variant="outlined"
                      color="secondary"
                      onClick={this.props.onClose}
                  >
                      Скасувати
                  </Button>
              </DialogActions>
          </div>
      );
  }
}

export default ModalMap;
