function Input ({type, name, input, handleChange, placeholder}) {
    return (
        <input
            type={type}
            className="form-control"
            name={name}
            placeholder={placeholder}
            value={input || ""}
            onChange={handleChange}
        />
    )
}

export default Input;