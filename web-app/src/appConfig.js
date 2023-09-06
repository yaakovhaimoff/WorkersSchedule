// Import the functions you need from the SDKs you need
import {initializeApp} from "firebase/app";
import {getAuth} from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyBzQj5kahE0SHA2BDhIoO70zZhn79d6CYc",
    authDomain: "work-schedule-66cb9.firebaseapp.com",
    projectId: "work-schedule-66cb9",
    storageBucket: "work-schedule-66cb9.appspot.com",
    messagingSenderId: "93978334930",
    appId: "1:93978334930:web:eb95c61dd4eea4b2b73f0b",
    measurementId: "G-41CQF4E061"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);