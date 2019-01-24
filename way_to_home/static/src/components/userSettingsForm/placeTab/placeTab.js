import React from 'react';

import axios from 'axios';
import Modal from '@material-ui/core/Modal';
import Button from '@material-ui/core/Button'

import PlaceForm from './placeForm.js';
import PlaceItem from './placeItem.js'
import CustomizedSnackbars from '../../message/message';
import './place.css'

export const place_api_url = '/api/v1/place/';
export const here_suggestions_url = 'http://autocomplete.geocoder.api.here.com/6.2/suggest.json';
export const here_geocoder_url = 'http://geocoder.api.here.com/6.2/geocode.json';


export default class PlaceTab extends React.Component {

    state = {
        openAddModal: false,
        ajaxError: undefined,
        places: [],
    };


    onClickAddBtn = () => {
        this.setState({openAddModal: true});
    };


    modalAddClose = () => {
        this.setState({openAddModal: false});
    };


    componentWillMount() {
        this.getPlaces();
    }


    removePlace = (id) => {
        let places = this.state.places.filter(place => place.id !== id);

        this.setState({
            places: places
        });
    };


    addPlace = (place) => {
        let places = [...this.state.places, place];

        this.setState({
            places: places
        })
    };


    getPlaces = () => {
        axios.get(place_api_url)
            .then(response => {
                this.setState({
                    places: response.data
                });
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
            .then(response => {
                this.removePlace(id);
            });
    };


    setError = (error) => {
        this.setState({ajaxError: error});
    };


    render(){
        return (
            <div>
                <div className='placeList'>
                    {this.state.places.map(place => (
                        <PlaceItem
                            key={place.id}
                            place={place}
                            deleteButton={this.sendDelete}
                            updatePlace={this.updatePlace}
                            setError={this.setError}/>
                    ))}
                    <div>
                        <Modal
                            open={this.state.openAddModal}
                            onClose={this.modalAddClose}
                            disableAutoFocus={true}>

                            <PlaceForm
                                form_type='Додати'
                                addPlace={this.addPlace}
                                close={this.modalAddClose}
                                setError={this.setError}/>
                        </Modal>
                    </div>
                </div>
                <div className='addButton' >
                    <Button
                        variant='contained'
                        size='medium'
                        color='primary'
                        onClick={this.onClickAddBtn}>
                      Додати місце
                    </Button>
                </div>
                {this.state.ajaxError && <CustomizedSnackbars message={this.state.ajaxError} reset={this.setError}/>}
            </div>
        );
    };
}
