import UploadFile from './uploadFile';
import React, {useState} from 'react';
import Input from "../utilities/input";
import handleInputChange from "../utilities/handleInputChange";
import ShiftsDropdown from "./ShiftsDropdown";

function Form() {
    const [inputs, setInputs] = useState({});
    const [selectedItems, setSelectedItems] = useState([]);

    const items = [
        { id: 1, label: "Morning" },
        { id: 2, label: "Afternoon" },
        { id: 3, label: "Night" },
        { id: 4, label: "Long Morning" },
        { id: 5, label: "Long Night" },
    ];

    const handleCheckboxChange = (item) => {
        if (selectedItems.includes(item.id)) {
            setSelectedItems(selectedItems.filter((id) => id !== item.id));
        } else {
            setSelectedItems([...selectedItems, item.id]);
        }
    };

    const handleChange = (event) => {
        handleInputChange(event, inputs, setInputs);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        // Create an array of selected shift labels based on the selectedItems
        const selectedShifts = items
            .filter((item) => selectedItems.includes(item.id))
            .map((item) => item.label);

        // Combine the selected shifts into a string
        const selectedShiftsString = selectedShifts.join(', ');

        console.log("Form Submitted", inputs);
        console.log(`Selected Shifts: ${selectedShiftsString}`);


        setInputs({});
        setSelectedItems([]);
    }


    return (
        <div className="container">
            <form onSubmit={handleSubmit}>
                <h2>Work Schedule Form</h2>
                <label className="form-label">Name:</label>
                <Input
                    type="text"
                    name="username"
                    input={inputs.username}
                    handleChange={handleChange}
                    placeholder={""}/>

                <label className="form-label">Email: </label>
                <Input
                    type="email"
                    name="email"
                    input={inputs.email}
                    handleChange={handleChange}
                    placeholder={""}/>

                <label className="form-label">Weeks:</label>
                <Input
                    type="number"
                    name="weeks"
                    input={inputs.weeks}
                    handleChange={handleChange}
                    placeholder={""}/>

                <label className="form-label">Message:</label>
                <textarea
                    name="message"
                    type="text"
                    value={inputs.message || ""}
                    className="form-control"
                    onChange={handleChange}></textarea>

                <label className="form-label">Shifts:</label>
                <ShiftsDropdown
                    items={items}
                    selectedItems={selectedItems}
                    handleCheckboxChange={handleCheckboxChange}
                />

                <button className="btn m-3" type="submit" style={{background: '#673ab7', color: 'white'}}>
                    Submit
                </button>
            </form>
        </div>
    )
}

export default Form;