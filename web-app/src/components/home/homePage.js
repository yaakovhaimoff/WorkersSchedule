import React from 'react';
import { Link } from 'react-router-dom';
import { auth } from '../../appConfig';

function HomePage() {
    return (
        <>
            <h1>Welcome To The Home Page</h1>
            <Link to="/signIn">Sign In</Link>
            <button onClick={auth.signOut}>Sign Out</button>
        </>
    );
}

export default HomePage;
