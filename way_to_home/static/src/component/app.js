import React, {Component} from 'react';
import StartBtn from './startBtn/startBtn.js'
import RouteSearchForm from './routeForm/routeForm.js'
import LogInBtn from './logInBtn/logInBtn.js'
import ResultForm from './routeResult/routeResult.js'

class App extends Component{
    render(){
        return(
            <div>
                <StartBtn></StartBtn>
                <RouteSearchForm></RouteSearchForm>
                <LogInBtn></LogInBtn>
                <ResultForm></ResultForm>
            </div>
        )
    }
}

export default App



