from employee_shifts import Employee, Facility, FacilityShift
import pandas as pd
import macros


def set_employee_shifts(file):
    df = pd.read_csv(file)
    employees = {}

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        # Get the email address
        email = row['Email address']

        # Create an Employee instance if necessary
        if email not in employees:
            employees[email] = Employee(email)

        # Iterate over the non-null cells in the row
        for column_name, cell_value in row[row.notnull()].items():
            # Check if this is a shift cell
            if '[' in column_name:
                # Extract the day and facility from the column name
                day_name, column_desc = column_name.split('[', 1)
                english_day = macros.HEBREW_TO_ENGLISH_DAYS.get(day_name.strip())
                column_desc = column_desc.rstrip(']')  # Remove the closing square bracket
                english_facility = macros.HEBREW_TO_ENGLISH_FACILITIES.get(column_desc.strip())

                # Extract the shifts from the cell value
                shifts = cell_value.split(',')
                english_shifts = [macros.HEBREW_TO_ENGLISH_SHIFTS.get(shift.strip()) for shift in shifts if
                                  shift.strip() in macros.HEBREW_TO_ENGLISH_SHIFTS]
                # Add the shift to the employee
                employees[email].add_shift(english_day, english_facility, english_shifts)
    return employees


# Load the CSV file into a pandas DataFrame
file_name = 'work.csv'
# initial employees data
employees_data = set_employee_shifts(file_name)
for email, employee in employees_data.items():
    print(f"Email: {employee.email}")
    for shift in employee.shifts:
        print(f"Day: {shift.day}, Facility: {shift.facility}, Shifts: {shift.shifts}")
    print()
# initial facilities
facilities = {}

facilities['Raashi'] = Facility('Raashi', [FacilityShift('Sunday', True, '08:00', '16:00')])
