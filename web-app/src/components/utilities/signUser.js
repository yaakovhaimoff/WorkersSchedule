import React, {useState} from "react";
import {auth} from "../../appConfig";
import {useNavigate} from 'react-router-dom';
import Email from "./email";
import Password from "./password";

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

                                        <Email email={email} setEmail={setEmail}/>
                                        <Password password={password} setPassword={setPassword}/>

                                        <button className="btn btn-outline-light btn-lg px-5 rounded-pill"
                                                type="submit">
                                            {buttonMessage}
                                        </button>
                                        <br/>
                                        <p className="mb-0"> <a href="/forgotPassword" className="text-white-50 fw-bold">Forgotten password?</a>
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
