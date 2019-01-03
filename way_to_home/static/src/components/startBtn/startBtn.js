import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import RouteSearchForm from '../routeForm/routeForm';
import './startBtn.css'

class StartBtn extends Component{

     constructor(props){
        super(props)

        this.state = {
            isRouteFormOpen: false
        }
     }

     toggleRouteForm = () => {
         this.setState(prevState => ({
            isRouteFormOpen: !prevState.isRouteFormOpen
         }));
     }

     closeRouteForm = () => {
         this.setState({
             isRouteFormOpen: false
         });
     }

    render(){
        const { isRouteFormOpen } = this.state;

        return(
            <div className='StartBtnDiv'>
                <Button variant="contained" color='primary' size='large' onClick={this.toggleRouteForm}>
                    ПРОКЛАСТИ МАРШРУТ
                </Button>
                {
                    isRouteFormOpen &&
                        <RouteSearchForm onClose={this.closeRouteForm} />
                }
            </div>
        )
    }
}

export default StartBtn;
