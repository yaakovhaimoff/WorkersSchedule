import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';

import Form from "./components/admin/form";
import WorkerSubmit from "./components/users/workerSubmit";
import Home from "./components/home/homePage";
import SignIn from "./components/home/login";

function App() {
    return (
        <div className="App container">
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/signIn" element={<SignIn />} />
                    <Route path="/form" element={<Form/>}/>
                    <Route path="/workerSubmit" element={<WorkerSubmit/>}/>
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
