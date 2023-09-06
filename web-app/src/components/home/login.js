import React from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import SignUser from "../utilities/signUser";

const SignIn = () => {
    return (
        <div className="sign-up-container">
            <SignUser signFunction={signInWithEmailAndPassword}
                      title={"Log In to your Account"}
                      buttonMessage={"Log In"}/>
        </div>
    );
};

export default SignIn;