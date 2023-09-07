import React, {useState} from "react";
import {auth} from "../../appConfig";
import {useNavigate} from 'react-router-dom';
import Input from "./input";
import handleInputChange from "./handleInputChange";

const SignUser = ({signFunction, title, buttonMessage}) => {
    const [inputs, setInputs] = useState({});
    const navigate = useNavigate();


    const signUp = (e) => {
        e.preventDefault();
        console.log(inputs.email);
        signFunction(auth, inputs.email, inputs.password)
            .then((userCredential) => {
                console.log(userCredential);
                navigate('/workerSubmit');
            })
            .catch((error) => {
                console.log(error);
            });
    };

    const handleChange = (event) => {
        handleInputChange(event, inputs, setInputs);
    };


    return (
        <div style={{
            backgroundColor: '#f2e6ff',
        }}>
            <div className="container py-5">
                <div className="row d-flex justify-content-center align-items-center">
                    <div className="col-12 col-md-8 col-lg-6 col-xl-5">
                        <div className="card text-white" style={{backgroundColor: '#673ab7', borderRadius: "1rem"}}>
                            <div className="card-body p-5 text-center">
                                <div className="mb-md-5 mt-md-4 pb-5">
                                    <h2 className="fw-bold mb-2 text-uppercase">{title}</h2>
                                    <form onSubmit={signUp}>
                                        <div className="mb-3">
                                            <Input
                                                type="email"
                                                name="email"
                                                input={inputs.email}
                                                handleChange={handleChange}
                                                placeholder={"Enter your email"}/>
                                        </div>

                                        <div className="mb-3">
                                            <Input
                                                type="password"
                                                name="password"
                                                input={inputs.password}
                                                handleChange={handleChange}
                                                placeholder={"Enter your password"}/>
                                        </div>

                                        <button className="btn btn-outline-light btn-lg px-5 rounded-pill"
                                                type="submit">
                                            {buttonMessage}
                                        </button>
                                        <br/>
                                        <p className="mb-0"><a href="/forgotPassword" className="text-white-50 fw-bold">Forgotten
                                            password?</a>
                                        </p>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SignUser;
