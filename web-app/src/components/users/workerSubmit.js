import React, {useState} from 'react';
import SubmitForm from "./submitForm";

function WorkerSubmit() {
    const [formData, setFormData] = useState({});
    const [collapsedDays, setCollapsedDays] = useState({});
    const [allCollapsed, setAllCollapsed] = useState(true);

    // Function to handle checkbox changes
    const handleCheckboxChange = (day, place, shift) => {
        // Determine whether the checkbox is checked
        const isChecked = !formData?.[day]?.[place]?.[shift];

        // Update the formData object based on the checkbox state
        setFormData((prevData) => ({
            ...prevData,
            [day]: {
                ...prevData[day],
                [place]: {
                    ...prevData[day]?.[place],
                    [shift]: isChecked,
                },
            },
        }));
    };

    // Function to handle form submission
    const handleSubmit = (e) => {
        // e.preventDefault();

        // Filter and log only the checked checkboxes
        const checkedCheckboxes = {};

        for (const day in formData) {
            for (const place in formData[day]) {
                for (const shift in formData[day][place]) {
                    if (formData[day][place][shift]) {
                        if (!checkedCheckboxes[day]) {
                            checkedCheckboxes[day] = {};
                        }
                        if (!checkedCheckboxes[day][place]) {
                            checkedCheckboxes[day][place] = [];
                        }
                        checkedCheckboxes[day][place].push(shift);
                    }
                }
            }
        }
        console.log('Checked Checkboxes:', checkedCheckboxes);
        setFormData({});
    }

    // Function to toggle the collapse state of a day
    const toggleDay = (day) => {
        setCollapsedDays((prevState) => ({
            ...prevState,
            [day]: !prevState[day],
        }));
    };

    // Function to toggle the collapse state of all days
    const toggleAll = () => {
        const newCollapsedDays = {};
        for (const day of days) {
            newCollapsedDays[day] = !allCollapsed;
        }
        setCollapsedDays(newCollapsedDays);
        setAllCollapsed(!allCollapsed);
    };

    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const places = ['Place Doesn\'t Matter', '1', '2', '3', '4'];
    const shifts = ['Shift Doesn\'t Matter', 'Morning', 'Afternoon', 'Night', 'Long Morning', 'Long Night'];

    return (
        <div style={{ backgroundColor: '#f2e6ff',
            padding: '20px',
            color: '#673ab7',
            justifyContent: 'center',
        }}>
            <h1>Worker Submissions:</h1>
            <button
                className="btn"
                style={{ backgroundColor: '#673ab7', color: 'white' }}
                type="button"
                onClick={toggleAll}
            >
                {allCollapsed ? 'Expand All' : 'Collapse All'}
            </button>
            <div>{"Press on day to submit its shifts."}</div>

            <SubmitForm days={days} handleSubmit={handleSubmit} handleCheckboxChange={handleCheckboxChange}
                        formData={formData}
                        setFormData={setFormData}
                        places={places}
                        shifts={shifts}
                        collapsedDays={collapsedDays}
                        toggleDay={toggleDay} />
        </div>
    );
}

export default WorkerSubmit;