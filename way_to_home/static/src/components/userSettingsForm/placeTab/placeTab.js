import React from 'react';

import axios from 'axios';
import Modal from '@material-ui/core/Modal';
import Button from '@material-ui/core/Button'

import PlaceForm from './placeForm.js';
import PlaceItem from './placeItem.js'
import './place.css'

export const place_api_url = '/api/v1/place/';


export default class PlaceTab extends React.Component {

    state = {
        open: false,
        places: []
    };

    onClickAddBtn = () => {
        this.setState({open: true});
    };

    modalClose = () => {
        this.setState({open: false});
    };

    componentDidMount(){
        this.getData();
    }

    getData = () => {
        axios.get(place_api_url)
            .then((response) => {
                this.setState({
                    places: response.data
                });
            });
    };

    removePlace = (id) => {
        let places = this.state.places.filter(place => place.id !== id);

        this.setState({
            places: places
        });
    };

    updatePlace = (new_place) => {
        let places = this.state.places.map(place => {
            if (place.id === new_place.id) {
                place.name = new_place.name;
                place.address = new_place.address;
                place.longitude = new_place.longitude;
                place.latitude = new_place.latitude;
            }
            return place;
        });

        this.setState({
            places: places
        });
    };

    sendDelete = (id) => {
        axios.delete(place_api_url + id)
            .then((response) => {
                this.removePlace(id);
            });
    };

    addPlace = (place) => {
        this.setState({
            places: [...this.state.places, place]
        })
    };

    render(){
        return (
            <div>
                <div className='placeList'>
                    {this.state.places.map((place) => (
                        <PlaceItem
                            key={place.id}
                            place={place}
                            deleteButton={this.sendDelete}
                            updatePlace={this.updatePlace}
                        />
                    ))}
                    <div>
                        <Modal
                            open={this.state.open}
                            onClose={this.modalClose}
                            disableAutoFocus='True'>

                            <PlaceForm
                                form_type='Додати'
                                addPlace={this.addPlace}
                                close={this.modalClose}
                            />
                        </Modal>
                    </div>
                </div>
                <div className="addButton" >
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={this.onClickAddBtn}
                    >
                      Додати місце
                    </Button>
                </div>
            </div>
        );
    }
}
