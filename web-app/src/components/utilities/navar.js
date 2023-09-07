import React, {useEffect} from 'react';
import {auth} from "../../appConfig";

function Navbar() {
    const {user, signout} = auth

    const handleLogout = async () => {
        try {
            await signout(); // Sign out the user using Firebase's signout function
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };

    useEffect(() => {
        console.log("user", user)
    }, []);

    return (
        <div className="navbar navbar-expand-lg" style={{ background: '#f2e6ff' }}>
            <div className="navbar-nav container">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <a href="/" className="nav-link">Home</a>
                    </li>
                    <li className="nav-item">
                        <a href="/About" className="nav-link">About</a>
                    </li>
                    <li className="nav-item">
                        <a href="/OurAdvantages" className="nav-link">Advantages</a>
                    </li>
                    <li className="nav-item">
                        <a href="/fqa" className="nav-link">Q&A</a>
                    </li>
                    <li className="nav-item">
                        <a href="/contact" className="nav-link">Contact</a>
                    </li>
                </ul>
            </div>
            <div className="navbar-nav ml-auto">
                <a href="/login" className="nav-link">Login</a>
            </div>
            {user ? (
                <div className="logout">
                    <span>{user.displayName || user.email}</span> |
                    <span>[USER, ADMIN]</span>
                    <button onClick={handleLogout} style={{ display: 'inline', marginLeft: '10px' }}>
                        Logout
                    </button>
                </div>
            ) : null}
        </div>
    );

}

export default Navbar;
