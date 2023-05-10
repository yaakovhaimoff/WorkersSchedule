class Facility:
    def __init__(self, facility_name, days):
        self.facility_name = facility_name
        self.days = days

class FacilityShift:
    def __init__(self, permanent_employee, shift_name):
        self.permanent_employee = permanent_employee
        self.shift_name = shift_name
        if permanent_employee != '':
            self.worker = permanent_employee
        else:
            self.worker = ''

