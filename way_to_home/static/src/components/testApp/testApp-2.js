import React from 'react';


function TestApp(props){
    const {testapp} = props
    const body = <section>{testapp.text}</section>
    return(
        <div>
            <h2>{testapp.title}</h2>
            {body}
            <h3>creation date: {(new Date(testapp.date)).toDateString()}</h3>
        </div>
    )
}

export default TestApp;