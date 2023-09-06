import React, {useState} from "react";
import {auth} from "../../appConfig";
import { useNavigate } from 'react-router-dom';

const SignUser = ({signFunction, title, buttonMessage}) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();


    const signUp = (e) => {
        e.preventDefault();
        signFunction(auth, email, password)
            .then((userCredential) => {
                console.log(userCredential);
                navigate('/workerSubmit');
            })
            .catch((error) => {
                console.log(error);
            });
    };

    return (
        <div className="container py-5 h-100">
            <div className="row d-flex justify-content-center align-items-center h-100">
                <div className="col-12 col-md-8 col-lg-6 col-xl-5">
                    <div className="card bg-dark text-white" style={{borderRadius: "1rem"}}>
                        <div className="card-body p-5 text-center">
                            <div className="mb-md-5 mt-md-4 pb-5">
                                <h2 className="fw-bold mb-2 text-uppercase">{title}</h2>
                                <form onSubmit={signUp}>
                                    <div className="mb-3">
                                        <input
                                            type="email"
                                            className="form-control"
                                            placeholder="Enter your email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </div>
                                    <div className="mb-3">
                                        <input
                                            type="password"
                                            className="form-control"
                                            placeholder="Enter your password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                        />
                                    </div>
                                    <button className="btn btn-outline-light btn-lg px-5 rounded-pill" type="submit">
                                        {buttonMessage}
                                    </button>
                                    <p className="mb-0">
                                        Already have an account? <a href="/workerSubmit"
                                                                    className="text-white-50 fw-bold">Login!</a>
                                    </p>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SignUser;
