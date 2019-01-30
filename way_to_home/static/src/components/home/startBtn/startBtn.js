import React, {Component} from 'react';
import Button from '@material-ui/core/Button';

import { RouteSearchForm } from '../index';
import './startBtn.css'


export default class StartBtn extends Component{
    state = {
        isRouteFormOpen: false
    };

    toggleRouteForm = () => {
        this.setState(prevState => ({
            isRouteFormOpen: !prevState.isRouteFormOpen
        }));
    };

    closeRouteForm = () => {
        this.setState({
            isRouteFormOpen: false
        });
    };

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
