import React, {Component} from 'react';
import axios from 'axios';

import Button from "@material-ui/core/Button";

import WayItem from './wayItem/wayItem';
import NewWayItem from './newWayItem/newWayItem'
import CustomizedSnackbars from '../../message/message';
import './wayTab.css';

const url = '/api/v1/';


export default class WayTab extends Component{

    state = {
        ways: [],
        places: [],
        newWay: [],
        ajaxError: undefined,
    };

    getData = () => {
        this.getWays();
        this.getPlaces();
    };

    getWays = () => {
        let requestWays = 'way/';

        axios.get(url + requestWays)
            .then(response => {
                if (response.status === 200) {
                    this.setState({ways: response.data});
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError("Не вдалося завантантажити шляхи"));
    };

    getPlaces = () => {
        let requestPlaces = 'place/';

        axios.get(url + requestPlaces)
            .then(response => {
                if (response.status === 200) {
                    if (response.data.length === 0){
                        this.setError("Спочатку збережіть місця");
                    }
                    this.setState({places: response.data});
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError("Не вдалося завантажити місця"));
    };

    componentWillMount() {
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

    setError = (error) => {
        this.setState({ajaxError: error});
    };

    handleDeleteExistItemClick = (id) => {
        axios.delete(url + `way/${id}`)
            .then(response => {
                if (response.status === 200 ) {
                    const ways = this.state.ways.filter(way => way.id !== id);
                    this.setState({ways: ways})
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError(error));
    };

    handleSaveClick = (placeAid, placeBid, route) => {

        let placeA = this.state.places.find(place => place.id === placeAid);
        let placeB = this.state.places.find(place => place.id === placeBid);
        let name = `${placeA.name} - ${placeB.name}`;

        let data = {
            name: name,
            start_place: placeAid,
            end_place: placeBid,
            steps: route,
        };
        axios.post(url + 'way/', data)
            .then(response => {
                if (response.status === 201) {
                    this.setState({
                        ways: [...this.state.ways, response.data],
                        newWay: []
                    })
                } else {
                    this.setError(response.data);
                }
            })
            .catch(error => this.setError(error));
    };

    render(){

        let { ajaxError, ways, newWay, places} = this.state;

        return(
            <div>
                {ways.map(way => (
                    <WayItem
                        key={way.id}
                        way={way}
                        places={places}
                        deleteButton={this.handleDeleteExistItemClick}
                    />
                ))}

                {newWay.map(way => (
                    <NewWayItem
                        key={Date.now()}
                        way={way}
                        places={places}
                        deleteButton={this.handleDeleteNewItemClick}
                        saveRoute={this.handleSaveClick}
                        setError={this.setError}
                    />
                ))}

                <div className="addButton" >
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={this.handleAddButtonClick}
                        disabled={newWay.length > 0 ? true : false}
                    >
                      Додати шлях
                    </Button>
                </div>
                {ajaxError && <CustomizedSnackbars message={ajaxError} reset={this.setError}/>}
            </div>
        )
    }
}
