import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Form from "./components/admin/form";
import WorkerSubmit from "./components/users/workerSubmit";
import Home from "./components/home/homePage";
import SignIn from "./components/home/login";
import FormResponse from "./components/users/formResponse";
import Navar from "./components/utilities/navar";

function App() {
    return (<>
            <Navar/>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/login" element={<SignIn/>}/>
                    <Route path="/form" element={<Form/>}/>
                    <Route path="/workerSubmit" element={<WorkerSubmit/>}/>
                    <Route path="/formResponse" element={<FormResponse/>}/>
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;