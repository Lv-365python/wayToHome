import React, {Component} from 'react';
import './startBtn.css'
import Button from '@material-ui/core/Button';

class StartBtn extends Component{

    constructor(props){
        super(props)

        this.state = {
        }
    }

    render(){
        return(
            <div className='StartBtnDiv'>
                <Button variant="contained" color='primary' size='large' onClick={this.openRouteForm}>
                    ПРОКЛАСТИ МАРШРУТ
                </Button>
            </div>
        )
    }

    openRouteForm = () => {
        document.getElementsByClassName('searchForm')[0].style.display = 'block';
    }
}

export default StartBtn;
