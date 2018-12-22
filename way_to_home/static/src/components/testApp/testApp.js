import React from 'react';


function TestApp(){
    const body = <section>body</section>
    return(
        <div>
            <h2>test title</h2>
            {body}
            <h3>creation date: {(new Date()).toDateString()}</h3>
        </div>
    )
}

export default TestApp;