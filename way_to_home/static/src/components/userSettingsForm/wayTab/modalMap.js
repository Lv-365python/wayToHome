import React from 'react';
import MobileStepper from '@material-ui/core/MobileStepper';
import Button from '@material-ui/core/Button';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';


const tutorialSteps = [
  {
    label: 'San Francisco – Oakland Bay Bridge, United States',
    imgPath:
      'https://images.unsplash.com/photo-1537944434965-cf4679d1a598?auto=format&fit=crop&w=400&h=250&q=60',
  },
  {
    label: 'Bird',
    imgPath:
      'https://images.unsplash.com/photo-1538032746644-0212e812a9e7?auto=format&fit=crop&w=400&h=250&q=60',
  },
  {
    label: 'Bali, Indonesia',
    imgPath:
      'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=400&h=250&q=80',
  },
  {
    label: 'NeONBRAND Digital Marketing, Las Vegas, United States',
    imgPath:
      'https://images.unsplash.com/photo-1518732714860-b62714ce0c59?auto=format&fit=crop&w=400&h=250&q=60',
  },
  {
    label: 'Goč, Serbia',
    imgPath:
      'https://images.unsplash.com/photo-1512341689857-198e7e2f3ca8?auto=format&fit=crop&w=400&h=250&q=60',
  },
];


class ModalMap extends React.Component {
  state = {
    activeStep: 0,
  };

  getData = () => {
      const { placeA, placeB } = this.props;

      var today = new Date();
      let tomorrow = new Date(today.getTime() + (24 * 60 * 60 * 1000)).toISOString();

      const url = `https://transit.api.here.com/v3/route.json
      ?dep=${placeA.longitude}%2C${placeA.latitude}
      &arr=${placeB.longitude}%2C${placeB.latitude}
      &time=${tomorrow}
      &app_id={APP_ID}
      &app_code={APP_CODE}
      &routing=tt`;

      console.log(url)
  };

  componentDidMount = () => {
      this.getData()
  };


    handleNext = () => {
    this.setState(prevState => ({
      activeStep: prevState.activeStep + 1,
    }));
  };

  handleBack = () => {
    this.setState(prevState => ({
      activeStep: prevState.activeStep - 1,
    }));
  };

  render() {

    const { activeStep } = this.state;
    const maxSteps = tutorialSteps.length;

    return (
        <div>
            <DialogTitle>Виберіть маршрут</DialogTitle>
            <DialogContent>
                <div>
                     TODO: MAP
                </div>
            </DialogContent>
            <DialogActions>
                <MobileStepper
                    steps={maxSteps}
                    position="static"
                    activeStep={activeStep}
                    nextButton={
                        <Button size="small" onClick={this.handleNext} disabled={activeStep === maxSteps - 1}>
                          Вперед
                          <KeyboardArrowRight />
                        </Button>
                    }
                    backButton={
                        <Button size="small" onClick={this.handleBack} disabled={activeStep === 0}>
                          <KeyboardArrowLeft />
                          Назад
                        </Button>
                    }
                    />
                <Button onClick={this.props.onClose} style={{color:"green"}}>
                    Вибрати
                </Button>
                <Button onClick={this.props.onClose} color="secondary">
                    Скасувати
                </Button>
            </DialogActions>
        </div>
    );
  }
}

export default ModalMap;
