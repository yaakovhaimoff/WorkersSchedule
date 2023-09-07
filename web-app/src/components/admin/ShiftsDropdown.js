import React, { useState } from "react";
import { Dropdown, Form } from "react-bootstrap";

const ShiftsDropdown = ({items, selectedItems, handleCheckboxChange}) => {
    return (
        <Dropdown>
            <Dropdown.Toggle style={{background: '#673ab7'}} id="dropdown-basic">
                Select Items
            </Dropdown.Toggle>

            <Dropdown.Menu>
                    {items.map((item) => (
                        <Form.Check
                            key={item.id}
                            type="checkbox"
                            id={`checkbox-${item.id}`}
                            label={item.label}
                            checked={selectedItems.includes(item.id)}
                            onChange={() => handleCheckboxChange(item)}
                        />
                    ))}
            </Dropdown.Menu>
        </Dropdown>
    );
};

export default ShiftsDropdown;
