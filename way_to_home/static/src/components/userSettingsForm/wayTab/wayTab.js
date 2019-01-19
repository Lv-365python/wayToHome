import React, {Component} from 'react';
import axios from 'axios';

import Button from "@material-ui/core/Button";

import WayItem from './wayItem/wayItem';
import NewWayItem from './newWayItem/newWayItem'
import './wayTab.css';

const url = 'http://127.0.0.1:8000/api/v1/';


export default class WayTab extends Component{

    state = {
        ways: [],
        places: [],
        newWay: [],
    };

    getData = () => {
        let requestWays = 'way/';
        let requestPlaces = 'place/';

        axios.get(url + requestWays)
            .then(response => {
                this.setState({ ways: response.data });
            })
        .catch(error => console.log(error));

        axios.get(url + requestPlaces)
            .then(response => {
                this.setState({ places: response.data });
            })
        .catch(error => console.log(error));
    };

    componentDidMount() {
        this.getData();
    };

    handleAddButtonClick = () => {
        this.setState({
            newWay: [{name: ''}],
        })
    };

    handleDeleteNewItemClick = () => {
        this.setState({
            newWay: []
        })
    };

    handleDeleteExistItemClick = () => {
        console.log("TODO: Delete way")
    };

    handleSaveClick = (placeAid, placeBid, route) => {

        let placeA = this.state.places.find(place => place.id === placeAid);
        let placeB = this.state.places.find(place => place.id === placeBid);
        let name = `${placeA.name} - ${placeB.name}`;
        console.log(route);
        let data = {
            name: name,
            start_place: placeAid,
            end_place: placeBid,
            steps: route,
        };
        axios.post(url + 'way/', data)
            .then(response => {
                console.log(response);

            })
            .catch(error => {
                console.log(error)
            });

    };

    render(){

        return(
            <div>
                {this.state.ways.map(way => (
                    <WayItem
                        key={way.id}
                        way={way}
                        places={this.state.places}
                        deleteButton={this.handleDeleteExistItemClick}
                    />
                ))}

                {this.state.newWay.map(way => (
                    <NewWayItem
                        key={Date.now()}
                        way={way}
                        places={this.state.places}
                        deleteButton={this.handleDeleteNewItemClick}
                        saveRoute={this.handleSaveClick}
                    />
                ))}

                <div className="addButton" >
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={this.handleAddButtonClick}
                        disabled={this.state.newWay.length > 0 ? true : false}
                    >
                      Додати шлях
                    </Button>
                </div>
            </div>
        )
    }
}
