function CollapsedDayButton ({day, collapsedDays, toggleDay}) {
  return (
      <button
          className="btn"
          style={{
              backgroundColor: '#673ab7',
              width: '100%',
              display: 'flex',
              color: 'white',
          }}
          type="button"
          data-toggle="collapse"
          data-target={`#collapse-${day}`}
          aria-expanded={!collapsedDays[day]}
          onClick={() => toggleDay(day)}
      >
          <div className="row">
              <div className="col align-self-start">
                  {collapsedDays[day] ? <i className="bi bi-caret-right-fill"></i> : <i className="bi bi-caret-down-fill"></i>}
              </div>
              <div className="col align-self-center">
                  {day}
              </div>
          </div>
      </button>
  )
}

export default CollapsedDayButton;