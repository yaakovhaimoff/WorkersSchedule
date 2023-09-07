function SubmitCheckbox({places, shifts, day, formData, handleCheckboxChange}) {
    // Calculate the width for each cell based on the number of shifts
    const cellWidth = `${100 / (shifts.length + 1)}%`;

    return (
        <tbody>
        {places.map((place) => (
            <tr key={place}>
                <td style={{width: cellWidth}}>{place}</td>
                {shifts.map((shift) => (
                    <td key={shift} style={{width: cellWidth}}>
                        <div className="form-check">
                            <input
                                className="form-check-input"
                                type="checkbox"
                                id={`${day}-${place}-${shift}`}
                                checked={formData?.[day]?.[place]?.[shift] || false}
                                onChange={() => handleCheckboxChange(day, place, shift)}
                                style={{
                                    backgroundColor: formData?.[day]?.[place]?.[shift] ? '#673ab7' : 'transparent',
                                }}
                            />
                        </div>
                    </td>
                ))}
            </tr>
        ))}
        </tbody>
    );
}

export default SubmitCheckbox;
