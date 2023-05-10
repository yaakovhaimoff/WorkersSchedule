from employee_shifts import Employee
from facilities import Facility, FacilityShift
import pandas as pd
import macros


def set_employee_shifts(file):
    # Load the CSV file into a pandas DataFrame
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


def set_facilities():
    raashi_regular_day = [FacilityShift('', shift) for shift in
                          ['Morning'] * macros.raashi_morning +
                          ['Double Morning'] +
                          ['Afternoon'] * macros.raashi_afternoon +
                          ['Night'] * macros.raashi_night]

    raashi_friday = [FacilityShift('', shift) for shift in
                     ['Morning'] * macros.raashi_night +
                     ['Afternoon'] * macros.raashi_small_shift +
                     ['Night'] * macros.raashi_night]

    raashi_saturday = [FacilityShift('', shift) for shift in
                       ['Morning'] * macros.raashi_small_shift +
                       ['Afternoon'] * macros.raashi_small_shift +
                       ['Night'] * macros.raashi_night]

    Maatz_regular_day = [FacilityShift('', shift) for shift in
                         ['Morning'] * macros.Maatz_morning +
                         ['Double Morning'] +
                         ['Afternoon'] * macros.Maatz_small_shift +
                         ['Night'] * macros.Maatz_small_shift]

    Maatz_weekend = [FacilityShift('', shift) for shift in
                     ['Morning'] * macros.Maatz_small_shift +
                     ['Afternoon'] * macros.Maatz_small_shift +
                     ['Night'] * macros.Maatz_small_shift]

    full_day_one_guy = [FacilityShift('', shift) for shift in
                        ['Morning'] * macros.full_week +
                        ['Afternoon'] * macros.full_week +
                        ['Night'] * macros.full_week]

    raashi_days = {
        'Sunday': raashi_regular_day,
        'Monday': raashi_regular_day,
        'Tuesday': raashi_regular_day,
        'Wednesday': raashi_regular_day,
        'Thursday': raashi_regular_day,
        'Friday': raashi_friday,
        'Saturday': raashi_saturday,
    }

    Maatz_days = {
        'Sunday': Maatz_regular_day,
        'Monday': Maatz_regular_day,
        'Tuesday': Maatz_regular_day,
        'Wednesday': Maatz_regular_day,
        'Thursday': Maatz_regular_day,
        'Friday': Maatz_weekend,
        'Saturday': Maatz_weekend,
    }

    half_day = [FacilityShift('', shift) for shift in
                ['Morning'] * macros.short_week +
                ['Afternoon'] * macros.short_week]

    half_day_one_guy = {
        'Sunday': half_day,
        'Monday': half_day,
        'Tuesday': half_day,
        'Wednesday': half_day,
        'Thursday': half_day,
    }

    full_day_one_guy_days = {
        'Sunday': full_day_one_guy,
        'Monday': full_day_one_guy,
        'Tuesday': full_day_one_guy,
        'Wednesday': full_day_one_guy,
        'Thursday': full_day_one_guy,
        'Friday': full_day_one_guy,
        'Saturday': full_day_one_guy,
    }

    short_day_one_guy = {
        'Sunday': [FacilityShift('', 'Morning')],
        'Monday': [FacilityShift('', 'Morning')],
        'Tuesday': [FacilityShift('', 'Morning')],
        'Wednesday': [FacilityShift('', 'Morning')],
        'Thursday': [FacilityShift('', 'Morning'),]
    }

    double_day_one_guy = {
        'Sunday': [FacilityShift('', 'Double Morning')],
        'Monday': [FacilityShift('', 'Double Morning')],
        'Tuesday': [FacilityShift('', 'Double Morning')],
        'Wednesday': [FacilityShift('', 'Double Morning')],
        'Thursday': [FacilityShift('', 'Double Morning')],

    }
    # print_shifts(Maatz_days)
    return [
        Facility('Raashi', raashi_days),
        Facility('Maatz', Maatz_days),
        Facility('Koresh', full_day_one_guy_days),
        Facility('Ararim', full_day_one_guy_days),
        Facility('Ezrachit', full_day_one_guy_days),
        Facility('Rashut_hataagidim', short_day_one_guy),
        Facility('Apak_ertsi', half_day_one_guy),
        Facility('Patentim', half_day_one_guy),
        Facility('Melech_david', double_day_one_guy),
        Facility('Sharai', short_day_one_guy),
        Facility('Rasham_mekarkein', short_day_one_guy),
        Facility('Tabu_mifkach', short_day_one_guy),
        Facility('Sanagoria', short_day_one_guy),
        Facility('Siyua_mishpati', short_day_one_guy),
        Facility('Yechidat_haseder', short_day_one_guy),
        Facility('Vaadat_arar', short_day_one_guy),
        Facility('Machash', half_day_one_guy),
        Facility('Maarachot_meida', short_day_one_guy),
        Facility('Rasham_yerushot', short_day_one_guy),
        Facility('Yechidot_miktsoiot', short_day_one_guy),
    ]


def print_employees_data():
    for email, employee in employees_data.items():
        print(f"Email: {employee.email}")
        for shift in employee.shifts:
            print(f"Day: {shift.day}, Facility: {shift.facility}, Shifts: {shift.shifts}")
        print()


def print_shifts(shifts):
    for day, val in shifts.items():
        print(day, [(x.permanent_employee, x.shift_name) for x in val])


if __name__ == '__main__':
    # initial employees data
    employees_data = set_employee_shifts(macros.file_name)
    # initial facilities
    facilities = set_facilities()
    for facility in facilities:
        print(f"Facility: {facility.facility_name}")
        for day, shifts in facility.days.items():
            print(f"Day: {day}")
            for shift in shifts:
                print(f"Shift: {shift.shift_name}, Worker: {shift.worker}")
        print()
