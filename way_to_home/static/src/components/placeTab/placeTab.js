import React, {Component} from 'react';
import Button from "@material-ui/core/Button";
import axios from 'axios';

import WayItem from '../wayItem/wayItem';
import './placeTab.css';

export default class PlaceTab extends Component{

    state = {
        request_type: 'place',
        url: 'http://127.0.0.1:8000/api/v1/',
        ways: [
            {
				id: 101,
				name: 'new_test_name',
				user_id: 100,
				routes: []
			},
			{
				id: 100,
				name: 'test_name',
				user_id: 100,
				routes: []
			}
        ]
    };


    getData = () => {
        let type = this.state.request_type;
        let url = this.state.url;

        axios.get(url + type)
            .then(function (response) {
                console.log(response);
            })
    };

    componentWillMount() {
        this.getData();
    };

    handleAddButtonClick = () => {
        this.setState({ways: [...this.state.ways, {name: 'test_name'}]})
    };

    render(){
        return(
            <div>
                {this.state.ways.map(way => (

                    <WayItem way={way}/>

                ))}

                <div className="addButton" >
                    <Button
                        variant="contained"
                        size="medium"
                        color="primary"
                        onClick={this.handleAddButtonClick}
                    >
                      Добавити шлях
                    </Button>
                </div>
            </div>
        )
    }
}
