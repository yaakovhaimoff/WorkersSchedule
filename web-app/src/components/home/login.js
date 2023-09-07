import React from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import SignUser from "../utilities/signUser";

const SignIn = () => {
    return (
        <SignUser signFunction={signInWithEmailAndPassword}
                  title={"Log In to your Account"}
                  buttonMessage={"Log In"}/>
    );
};

export default SignIn;