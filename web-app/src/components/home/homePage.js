import React from 'react';
import { auth } from '../../appConfig';

function HomePage() {
    return (
        <>
            <h1>Welcome To The Home Page</h1>
            <button onClick={auth.signOut}>Sign Out</button>
            <i className="bi bi-caret-right-fill"></i>
            <i className="bi bi-caret-down-fill"></i>
        </>
    );
}

export default HomePage;
