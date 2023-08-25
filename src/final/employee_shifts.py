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

