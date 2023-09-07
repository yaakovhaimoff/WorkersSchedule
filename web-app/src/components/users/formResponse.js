import React from 'react';

function FormResponse() {
    const cardStyle = {
        backgroundColor: 'white', // White background for the card
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        borderTop: '10px solid #673ab7', // Purple border on top
    };

    return (
        <div style={{backgroundColor: '#f2e6ff', height: '100vh'}}>
            <div className="card" style={cardStyle}>
                <div className="card-body">
                    <h3 style={{color: 'black',}}>Worker Submission</h3>
                    <p>Your response has been recorded.</p>
                    <a href="/workerSubmit">Submit another response</a>
                </div>
            </div>
            <p style={{
                display: 'flex',
                justifyContent: 'center',
            }}
            >{"Work Schedule"}</p>
        </div>
    );
}

export default FormResponse;
