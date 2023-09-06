import React from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import SignUser from "../utilities/signUser";

const SignUp = () => {


    return (
        <div className="sign-up-container">
           <SignUser signFunction={createUserWithEmailAndPassword}
                     title={"Create Account"}
                     buttonMessage={"Sign Up"}/>
        </div>
    );
};

export default SignUp;