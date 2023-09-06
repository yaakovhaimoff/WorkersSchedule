import React, {useState} from 'react';

function WorkerSubmit() {
    const [formData, setFormData] = useState({});

    // Function to handle checkbox changes
    const handleCheckboxChange = (day, place, shift) => {
        // Determine whether the checkbox is checked
        const isChecked = !formData?.[day]?.[place]?.[shift];

        // Log the value to the console (for debugging purposes)
        // console.log(`Checkbox for ${day}, Place: ${place}, Shift: ${shift} is checked: ${isChecked}`);

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
        e.preventDefault();

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

        // Log the checked checkboxes to the console
        console.log('Checked Checkboxes:', checkedCheckboxes);

        // Clear the formData for the next submission
        setFormData({});
    };


    // Define the list of days, places, and shifts
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const places = ['Doesn\'t Matter', '1', '2', '3', '4'];
    const shifts = ['Doesn\'t Want', 'Morning', 'Afternoon', 'Night', 'Long Morning', 'Long Night'];

    return (
        <div style={{ backgroundColor: '#f2e6ff', padding: '20px' }}>
        <h1>Worker Submissions:</h1>
            <form onSubmit={handleSubmit}>
                {days.map((day) => (
                    <div key={day}>
                        <br/>
                        <h4>{day}</h4>
                        <table className={"table table-striped table-bordered"}>
                            <thead>
                            <tr>
                                <th></th>
                                {shifts.map((shift) => (
                                    <th key={shift}>{shift}</th>
                                ))}
                            </tr>
                            </thead>
                            <tbody>
                            {places.map((place) => (
                                <tr key={place}>
                                    <td>{place}</td>
                                    {shifts.map((shift) => (
                                        <td key={shift}>
                                            <div className="form-check">
                                                <input
                                                    className="form-check-input"
                                                    type="checkbox"
                                                    id={`${day}-${place}-${shift}`}
                                                    checked={formData?.[day]?.[place]?.[shift] || false}
                                                    onChange={() => handleCheckboxChange(day, place, shift)}
                                                />
                                            </div>
                                        </td>
                                    ))}
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                ))}
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default WorkerSubmit;