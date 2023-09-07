function Password ({password, setPassword}) {
  return (
      <div className="mb-3">
          <input
              type="password"
              className="form-control"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
          />
      </div>
  )
}

export default Password;