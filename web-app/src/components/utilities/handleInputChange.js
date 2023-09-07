import React from "react";

const handleChange = (event, inputs, setInputs) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs((values) => ({ ...values, [name]: value }));
};

export default handleChange;

