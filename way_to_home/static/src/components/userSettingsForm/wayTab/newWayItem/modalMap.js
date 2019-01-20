import React from 'react';
import MobileStepper from '@material-ui/core/MobileStepper';
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';


class ModalMap extends React.Component {
  state = {
      activeRoute: 0,
  };

  handleNext = () => {
      this.setState(prevState => ({
          activeRoute: prevState.activeRoute + 1,
      }));
  };

  handleBack = () => {
      this.setState(prevState => ({
          activeRoute: prevState.activeRoute - 1,
      }));
  };

  render() {
    const { routes } = this.props;
    const { activeRoute } = this.state;
    const maxRoutes = routes.length;
    console.log(routes);

    return (
        <div>
            <DialogTitle>Виберіть маршрут</DialogTitle>
            <DialogContent>
                <div>
                    TODO: MAP {routes[activeRoute].Sections.Sec[0].mode}
                </div>
            </DialogContent>
            <DialogActions>
                <MobileStepper
                    steps={maxRoutes}
                    position="static"
                    activeStep={activeRoute}
                    nextButton={
                        <Button size="small" onClick={this.handleNext} disabled={activeRoute === maxRoutes - 1}>
                          Вперед
                          <KeyboardArrowRight />
                        </Button>
                    }
                    backButton={
                        <Button size="small" onClick={this.handleBack} disabled={activeRoute === 0}>
                          <KeyboardArrowLeft />
                          Назад
                        </Button>
                    }
                />
                <Button
                    variant="outlined"
                    style={{color:"green"}}
                    onClick={() => this.props.saveRoute(routes[activeRoute].Sections.Sec)}

                >
                    Вибрати
                </Button>
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
