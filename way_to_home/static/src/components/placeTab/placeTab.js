import React, {Component} from 'react';
import Button from "@material-ui/core/Button";

import WayItem from '../wayItem/wayItem';
import './placeTab.css';

export default class PlaceTab extends Component{
    render(){
        return(
            <div>
                <WayItem />
                <div className="addButton" >
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                    >
                      Добавити шлях
                    </Button>
                </div>
            </div>
        )
    }
}
