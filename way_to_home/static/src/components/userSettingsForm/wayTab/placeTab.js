import React, {Component} from 'react';
import Button from "@material-ui/core/Button";
import axios from 'axios';

import WayItem from './wayItem/wayItem';
import NewWayItem from './newWayItem/newWayItem'
import './placeTab.css';

export default class PlaceTab extends Component{

    state = {
        ways: [],
        newWays: [],
    };

    getData = () => {
        let url = 'http://127.0.0.1:8000/api/v1/';
        let type = 'way/';

        axios.get(url + type)
            .then(response => {
                this.setState({ ways: response.data });
            });
    };

    componentWillMount() {
        this.getData();
    };

    componentWillUnmount() {
        console.log("DID")
    };

    handleAddButtonClick = () => {
        this.setState({
            newWays: [...this.state.newWays, {name: ''}],
        })
    };

    handleDeleteNewItemClick = () => {
        this.setState({
            newWays: []
        })
    }

    render(){
        return(
            <div>
                {this.state.ways.map(way => (

                    <WayItem
                        key={way.id}
                        way={way}/>

                ))}

                {this.state.newWays.map(way => (

                    <NewWayItem
                        key={Date.now()}
                        way={way}
                        deleteButton={this.handleDeleteNewItemClick}
                    />

                ))}

                <div className="addButton" >
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={this.handleAddButtonClick}
                        disabled={this.state.newWays.length > 0 ? true : false}
                    >
                      Добавити шлях
                    </Button>
                </div>

                {/*<div className="saveButton">*/}
                    {/*<Button*/}
                        {/*variant="contained"*/}
                        {/*size="medium"*/}
                        {/*color="primary"*/}
                        {/*// onClick={this.handleAddButtonClick}*/}
                    {/*>*/}
                      {/*Зберегти*/}
                    {/*</Button>*/}
                {/*</div>*/}
            </div>
        )
    }
}
