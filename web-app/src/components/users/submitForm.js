import React from 'react';
import SubmitCheckbox from './submitCheckbox';

function SubmitForm({ days, places, shifts, formData, setFormData, handleCheckboxChange, handleSubmit, collapsedDays, toggleDay }) {
    const clearForm = () => {
        setFormData({});
    };

    return (
        <form onSubmit={handleSubmit}>
            {days.map((day) => (
                <div key={day}>
                    <button
                        className="btn"
                        style={{
                            backgroundColor: '#673ab7',
                            width: '100%',
                            display: 'flex',
                            justifyContent: 'center',
                            color: 'white',
                        }}
                        type="button"
                        data-toggle="collapse"
                        data-target={`#collapse-${day}`}
                        aria-expanded={!collapsedDays[day]}
                        onClick={() => toggleDay(day)}
                    >
                        {day}
                    </button>
                    <div className={`collapse multi-collapse ${collapsedDays[day] ? '' : 'show'}`}
                         id={`collapse-${day}`}>
                        <table className="table table-striped table-bordered rounded">
                            <thead>
                            <tr>
                                <th></th>
                                {shifts.map((shift) => (
                                    <th key={shift}>{shift}</th>
                                ))}
                            </tr>
                            </thead>
                            <SubmitCheckbox places={places}
                                            shifts={shifts}
                                            day={day}
                                            formData={formData}
                                            handleCheckboxChange={handleCheckboxChange} />
                        </table>
                    </div>
                    <br/>
                </div>
            ))}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <button
                    className="btn"
                    style={{
                        backgroundColor: '#673ab7',
                        color: 'white',
                    }}
                    type="submit"
                >
                    Submit
                </button>
                <button
                    className="btn"
                    type="button"
                    onClick={clearForm}
                    style={{color: '#673ab7',}}
                >
                    Clear form
                </button>

            </div>
            <p style={{
                display: 'flex',
                justifyContent: 'center',}}
            >{"Work Schedule"}</p>
        </form>
    );
}

export default SubmitForm;
