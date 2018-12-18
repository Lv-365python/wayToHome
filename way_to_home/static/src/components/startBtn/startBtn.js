import React, {Component} from 'react';
import Button from '@material-ui/core/Button';
import './startBtn.css'

class StartBtn extends Component{

    constructor(props){
        super(props)

        this.state = {
        }
    }

    openRouteForm = () => {
        document.getElementsByClassName('searchForm')[0].style.display = 'block';
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
}

export default StartBtn;

