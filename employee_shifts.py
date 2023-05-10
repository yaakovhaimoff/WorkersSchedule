class Shift:
    def __init__(self, day, facility, shifts):
        self.day = day
        self.facility = facility
        self.shifts = shifts

class Employee:
    def __init__(self, email):
        self.email = email
        self.shifts = []

    def add_shift(self, day, facility, shifts):
        shift = Shift(day, facility, shifts)
        self.shifts.append(shift)

class Facility:
    def __init__(self, name, shifts):
        self.name = name
        self.shifts = shifts

class FacilityShift:
    def __init__(self, day, permanent_employee, start_time, end_time):
        self.day = day
        self.permanent_employee = permanent_employee
        self.start_time = start_time
        self.end_time = end_time

