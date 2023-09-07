function Email ({email, setEmail}) {
  return (
      <div className="mb-3">
          <input
              type="email"
              className="form-control"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
          />
      </div>
  )
}

export default Email;