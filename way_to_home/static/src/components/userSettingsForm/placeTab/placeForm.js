import React, {Component} from 'react';

import Autosuggest from 'react-autosuggest';
import axios from 'axios';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

import {place_api_url} from './placeTab.js'


class PlaceForm extends Component {

    state = {
        name: ((!this.props.place)? '': this.props.place.name),
        address: ((!this.props.place)? '': this.props.place.address),
        locationId: '',
        latitude: ((!this.props.place)? null: this.props.place.latitude),
        longitude: ((!this.props.place)? null: this.props.place.longitude),
        confirmDisabled: true,
        suggestions: [],
    };


    onChangeName = (event) => {
        let name = event.target.value;
        let disabled = true;

        if (this.props.form_type === 'Зберегти')
            disabled = this.handleEditForm(name, this.state.address);
        else
            disabled = this.handleAddForm(this.state.address);

        this.setState({
            name: name,
            confirmDisabled: disabled
        });
    };


    handleAddForm = (address) => {
        const {latitude, longitude} = this.state;
        return !(address && longitude && latitude);
    };


    handleEditForm = (name, address) => {
        const {place} = this.props;
        const {latitude, longitude} = this.state;
        let disabled = true;

        if (place.name === name && place.address === address) {
            disabled = place.latitude === latitude && place.longitude === longitude;
        }
        else if (place.name !== name && place.address === address) {
            disabled = !(place.latitude === latitude && place.longitude === longitude);
        }
        else if (place.address !== address) {
            disabled = place.latitude === latitude && place.longitude === longitude;
        }

        return disabled;
    };

    onChangeAddress = (event, { newValue }) => {
        this.setState({
            address: newValue,
            confirmDisabled: true
        });
    };


    onClickConfirm = () => {
        if (this.props.form_type === 'Зберегти'){
            this.sendUpdate();
        }
        else {
            this.sendPost();
        }
        this.props.close();
    };


    getSuggestions = ({value}) => {
        let url = `http://autocomplete.geocoder.api.here.com/6.2/suggest.json?query=${value}&maxresults=20&app_id=ctrJV3imNpgpWu5urnAa&app_code=4lPfKEUtIyz_PXCcimqv2w&country=UKR&language=uk`;
        axios.get(url,  { crossdomain: true })
            .then(({data}) => {
                let suggestions = data.suggestions.filter(suggestion => {
                    if (suggestion.address.county === 'Львівська область' && suggestion.address.street) {
                        return suggestion;
                    }
                });
                suggestions = suggestions.map(suggestion => {
                    let houseNumber = suggestion.address.houseNumber || '' ;
                    let address =  suggestion.address.street + ' ' + houseNumber;
                    address = address.replace('вулиця', 'вул.');
                    return {
                        locationId: suggestion.locationId,
                        address: address,
                    };
                });
                this.setState({
                    suggestions: suggestions
                });
            }).catch(error => {
                // TODO: message component
                console.log('Can not retrieve exceptions');
        });
    };


    sendUpdate = () => {
        let id = this.props.place.id;
        const {name, address, longitude, latitude} = this.state;
        let place = {
            id: id,
            name: name,
            address: address,
            longitude: longitude,
            latitude: latitude
        };

        axios.put(place_api_url + id,  {
            'name': name,
            'address': address,
            'longitude': longitude,
            'latitude': latitude
        }).then(( response) => {
            this.props.updatePlace(place);
        });
    };


    sendPost = () => {
        const {name, address, longitude, latitude} = this.state;

        axios.post(place_api_url,  {
            'name': name,
            'address': address,
            'longitude': longitude,
            'latitude': latitude
        }).then(( {data}) => {
            this.props.addPlace(data);
        });
    };


    retrieveCoordinates = (locationId) => {
        let url = `http://geocoder.api.here.com/6.2/geocode.json?locationid=${locationId}&jsonattributes=1&gen=9&app_id=ctrJV3imNpgpWu5urnAa&app_code=4lPfKEUtIyz_PXCcimqv2w`;

        axios.get(url,  { crossdomain: true })
            .then(({data} ) => {
                let coordinates = data.response.view[0].result[0].location.displayPosition;
                this.setState({
                    latitude: coordinates.latitude,
                    longitude: coordinates.longitude,
                    confirmDisabled: false,
                });
            }).catch(error => {
                // TODO: messeage component
                console.log('Can not retrieve coordinate');
            });
    };


    onSuggestionsClearRequested = () => {
        this.setState({
            suggestions: []
        });
    };


    onSuggestionSelected = (event, {suggestion}) =>{
        const {locationId, address} = suggestion;
        this.setState({
            locationId: locationId,
            address: address
        });
        this.retrieveCoordinates(locationId);
    };


    getSuggestionValue = (suggestion) => {
        return suggestion.address;
    };


    renderSuggestion = (suggestion) => (
        <div>
            {suggestion.address}
        </div>
    );


    render() {
        const inputProps = {
            placeholder: 'Введіть адрес',
            value: this.state.address,
            onChange: this.onChangeAddress,
            type: 'search',
        };

        return (
            <div className='placeForm'>
                <TextField
                    className='nameInput'
                    id='name-input'
                    label='Назва *'
                    margin='normal'
                    variant='filled'
                    fullWidth
                    value={this.state.name}
                    onChange={this.onChangeName}
                />
                <Autosuggest
                    suggestions={this.state.suggestions}
                    onSuggestionsFetchRequested={this.getSuggestions}
                    onSuggestionsClearRequested={this.onSuggestionsClearRequested}
                    getSuggestionValue={this.getSuggestionValue}
                    renderSuggestion={this.renderSuggestion}
                    onSuggestionSelected={this.onSuggestionSelected}
                    inputProps={inputProps}
                  />

                <div className='formButtons'>
                    <Button
                        className='confirmButton'
                        variant='contained'
                        color='primary'
                        size='medium'
                        onClick={this.onClickConfirm}
                        disabled={this.state.confirmDisabled}>
                        {this.props.form_type}
                    </Button>
                    <Button
                        variant='contained'
                        color='secondary'
                        size='medium'
                        className='Btn'
                        onClick={this.props.close}>
                        Скасувати
                    </Button>
                </div>

            </div>
        );
    };
}

export default PlaceForm;
