import React, {Component} from 'react';
import axios from 'axios';
import Autosuggest from 'react-autosuggest';

import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MyLocationIcon from '@material-ui/icons/MyLocation';
import Tooltip from '@material-ui/core/Tooltip';

import {place_api_url, here_geocoder_url, here_suggestions_url} from './placeTab.js'
import { HERE_APP_CODE, HERE_APP_ID } from "src/settings";


export default class PlaceForm extends Component {

    state = {
        name: this.props.place ? this.props.place.name: '',
        address: this.props.place ? this.props.place.address: '',
        locationId: '',
        latitude: this.props.place ? this.props.place.latitude: null,
        longitude: this.props.place ? this.props.place.longitude: null,
        confirmDisabled: true,
        selected: false,
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


    onChangeAddress = (event, { newValue }) => {
        if (this.state.address.length === 0){
            this.setState({
                selected: false,
            });
        }
        this.setState({
            address: newValue,
            confirmDisabled: true
        });
    };


    onBlurAddress = () => {
        const {selected, address} = this.state;

        if (selected) return;

        axios.get(here_geocoder_url,  {
            crossdomain: true,
            params: {
                searchtext: address,
                country: 'UKR',
                language: 'uk',
                jsonattributes: 1,
                gen: 9,
                app_id: HERE_APP_ID,
                app_code: HERE_APP_CODE,

            }
        }).then(({data}) => {
            const {address, displayPosition} = data.response.view[0].result[0].location;
            if (address.city !== 'Львів')
                throw message;

            const formatted_address = this.formatAddress(address);
            this.setState({
                address: formatted_address,
                latitude: displayPosition.latitude,
                longitude: displayPosition.longitude,
                confirmDisabled: false,
            });
        }).catch(error => {
            this.setState({
                confirmDisabled: true,
            });
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


    onClickConfirm = () => {
        if (this.props.form_type === 'Зберегти')
            this.sendUpdate();
        else
            this.sendPost();
    };


    sendUpdate = () => {
        const id = this.props.place.id;
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
            'longitude': parseFloat(longitude),
            'latitude': parseFloat(latitude)
        }).then(response => {
            this.props.updatePlace(place);
            this.props.handleChangeName(name);
            this.props.close();
            this.props.setMessage('Успішне редагування!', 'success');
        }).catch(error =>{
            this.props.close();
            this.props.setMessage('Не вдалось редагувати місце. Спробуйте ще раз.');
        });
    };


    sendPost = () => {
        const {name, address, longitude, latitude} = this.state;

        axios.post(place_api_url,  {
            'name': name,
            'address': address,
            'longitude': longitude,
            'latitude': latitude
        }).then(response => {
            this.props.addPlace(response.data);
            this.props.close();
            this.props.setMessage('Успішне створення!', 'success');
        }).catch(error => {
            this.props.close();
            this.props.setMessage('Не вдалось створити місце. Спробуйте ще раз.');
        });
    };


    onSuggestionsClearRequested = () => {
        this.setState({
            selected: false,
            suggestions: []
        });
    };


    onSuggestionSelected = (event, {suggestion}) =>{
        const {locationId, address} = suggestion;
        this.setState({
            locationId: locationId,
            address: address,
            selected: true
        });
        this.retrieveCoordinates(locationId);
    };


    formatSuggestions = (suggestions) => {
        suggestions = suggestions.map(suggestion => {
            let address = this.formatAddress(suggestion.address);
            return {
                locationId: suggestion.locationId,
                address: address,
            };
        });
        return suggestions;
    };


    formatAddress = (address_information) => {
        let houseNumber = address_information.houseNumber || '' ;
        let address =  address_information.street + ' ' + houseNumber;

        address = this.prettifyAddress(address);

        return address;
    };


    prettifyAddress = (address) => {
        if (address.includes('вулиця'))
            address = 'вул. ' + address.replace('вулиця', '');
        else if (address.includes('проспект'))
            address = 'проспект ' + address.replace('проспект', '');

        return address
    };


    removeDuplicateSuggestions = (suggestions) => {
        let uniq = {};
        return suggestions.filter(suggestion =>
            !uniq[suggestion.address] && (uniq[suggestion.address] = true)
        );
    };


    getSuggestions = ({value}) => {
        axios.get(here_suggestions_url,  {
            crossdomain: true,
            params: {
                query: value,
                maxresults: 10,
                country: 'UKR',
                language: 'uk',
                prox: '49.84, 24.028667',
                app_id: HERE_APP_ID,
                app_code: HERE_APP_CODE
            }
        }).then(({data}) => {
            let suggestions = data.suggestions.filter(suggestion => {
                if (suggestion.label.includes('Львів') &&
                    suggestion.address.street) {
                    return suggestion;
                }
            });
            suggestions = this.formatSuggestions(suggestions);
            suggestions = this.removeDuplicateSuggestions(suggestions);
            this.setState({
                suggestions: suggestions
            });
        });
    };


    retrieveCoordinates = (locationId) => {
        axios.get(here_geocoder_url,  {
            crossdomain: true,
            params: {
                locationId: locationId,
                jsonattributes: 1,
                gen: 9,
                app_id: HERE_APP_ID,
                app_code: HERE_APP_CODE
            }
        }).then(({data}) => {
            const {latitude, longitude} = data.response.view[0].result[0].location.displayPosition;
            this.setState({
                latitude: latitude,
                longitude: longitude,
                confirmDisabled: false,
            });
        }).catch(error => {
            this.setState({
                confirmDisabled: true,
            });
        });
    };


    getSuggestionValue = (suggestion) => {
        return suggestion.address;
    };


    renderSuggestion = (suggestion) => (
        <div>
            {suggestion.address}
        </div>
    );


    onClickLocationIcon = () => {
        if (!navigator.geolocation){
            this.props.setMessage('Геолокація не підтримується Вашим браузером', 'info');
            return
        }
        navigator.geolocation.getCurrentPosition(
            position => this.onSuccessCurrentLocation(position),
            () => this.onFailCurrentLocation()
        );
    };


    onFailCurrentLocation = () => {
        this.props.setMessage('Не вдалось визначити Ваше місцезнаходження');
        this.setState({
            confirmDisabled: true
        })
    };


    onSuccessCurrentLocation = (position) => {
        const {latitude, longitude}  = position.coords;
        const open_street_map_url = 'https://nominatim.openstreetmap.org/reverse';
        axios.get(open_street_map_url, {
            params: {
                format: 'jsonv2',
                lat: latitude,
                lon: longitude
            }
        }).then(response => {
            let address = this.getCurrentAddress(response);
            address = this.prettifyAddress(address);
            this.setState({
                address: address,
                latitude: latitude,
                longitude: longitude,
                confirmDisabled: false,
                selected: true
            });
        }).catch(error => {
            this.props.setMessage('Не вдалось визначити Ваше місцезнаходження');
            this.setState({
                confirmDisabled: true
            })
        });
    };


    getCurrentAddress = response => {
        const address = response.data.address;
        let house_number = address.house_number || '';
        let formatted_address = address.road + ' ' + house_number;

        return formatted_address;
    };


    render() {
        const inputProps = {
            placeholder: 'Введіть адресу',
            value: this.state.address,
            type: 'search',
            onChange: this.onChangeAddress,
            onBlur: this.onBlurAddress
        };
        const {name, suggestions, confirmDisabled} = this.state;
        const {form_type, close} = this.props;

        return (
            <div className='placeForm'>
                <TextField
                    className='nameInput'
                    id='name-input'
                    label='Назва *'
                    margin='normal'
                    variant='filled'
                    fullWidth
                    value={name}
                    onChange={this.onChangeName}/>
                <Autosuggest
                    suggestions={suggestions}
                    onSuggestionsFetchRequested={this.getSuggestions}
                    onSuggestionsClearRequested={this.onSuggestionsClearRequested}
                    getSuggestionValue={this.getSuggestionValue}
                    renderSuggestion={this.renderSuggestion}
                    onSuggestionSelected={this.onSuggestionSelected}
                    inputProps={inputProps}/>
                <div className='locationIcon'>
                    <Tooltip
                        title='Обрати Ваше місцезнаходження'
                        placement='right'>
                        <IconButton
                            color='primary'
                            onClick={this.onClickLocationIcon}>
                            <MyLocationIcon fontSize='large'/>
                        </IconButton>
                    </Tooltip>
                </div>
                <div className='formButtons'>
                    <Button
                        className='confirmButton'
                        variant='contained'
                        color='primary'
                        size='medium'
                        onClick={this.onClickConfirm}
                        disabled={confirmDisabled}>
                        {form_type}
                    </Button>
                    <Button
                        variant='contained'
                        color='secondary'
                        size='medium'
                        onClick={close}>
                        Скасувати
                    </Button>
                </div>
            </div>
        );
    };
}
