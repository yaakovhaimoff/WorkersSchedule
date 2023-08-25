import random

import algo_tryout as algo

# Define the days of the week
days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Define the shifts for each day of the week
shifts_per_day = {
    'Sunday': ['Morning', 'Afternoon', 'Night'],
    'Monday': ['Morning', 'Afternoon', 'Night'],
    'Tuesday': ['Morning', 'Afternoon', 'Night'],
    'Wednesday': ['Morning', 'Afternoon', 'Night'],
    'Thursday': ['Morning', 'Afternoon', 'Night'],
    'Friday': ['Morning', 'Afternoon', 'Night'],
    'Saturday': ['Morning', 'Afternoon', 'Night'],
    # 'Saturday': ['Small', 'Small', 'Afternoon', 'Afternoon', 'Night'],
}

shifts_in_nums = {
    'Morning': 0,
    'Afternoon': 1,
    'Night': 2,
    # 'Small': 3
}

days_in_nums = {
    'Sunday': 0,
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6
}

num_of_shifts = len(shifts_in_nums)
num_of_days = len(days_in_nums)
num_of_empolyees = 4

# Generate a list of unique employee IDs
employee_ids = [_ for _ in range(num_of_empolyees)]

# Create a dictionary to store submissions for each worker
worker_submissions = {employee_id: [] for employee_id in employee_ids}


def generate_rand_submissions():
    for day in days_of_week:
        for shift_type in shifts_per_day[day]:
            num_submissions = random.randint(0, num_of_days * num_of_shifts)
            for _ in range(num_submissions):
                employee_id = random.choice(employee_ids)
                submission = (day, shift_type)

                # Check if the worker has already submitted this shift
                if submission not in worker_submissions[employee_id]:
                    worker_submissions[employee_id].append(submission)


def set_requests():
    # Request: (employee, shift, day, weight)
    requests = []
    for employee_id, submissions in worker_submissions.items():
        for submission in submissions:
            day, shift_type = submission
            requests.append((employee_id, shifts_in_nums.get(shift_type), days_in_nums.get(day), -2))
    return requests


def add_missing_shifts_to_requests(requests):
    # Identify shifts that workers didn't submit
    all_shifts = set()
    for day, day_shifts in shifts_per_day.items():
        all_shifts.update([(day, shift) for shift in day_shifts])

    missing_shifts = []
    for employee_id in worker_submissions:
        for shift in all_shifts:
            if shift not in worker_submissions[employee_id] and shift not in missing_shifts:
                missing_shifts.append((employee_id, shifts_in_nums.get(shift[1]), days_of_week.index(shift[0]), 4))

    # Add the missing shifts to the requests list
    requests.extend(missing_shifts)
    return sorted(requests, key=lambda x: (x[0], x[2]))


def print_work_submissions():
    for employee_id, submissions in worker_submissions.items():
        print(f"Employee: {employee_id}")
        for submission in submissions:
            day, shift_type = submission
            print(f"Day: {day}, Shift: {shift_type}")
        print()


def print_requests(requests):
    for request in requests:
        print(request)
        # employee_id, shift_type, day, weight = request
        # print(f"Employee: {employee_id}, Day: {day}, Shift: {shift_type}, Weight: {weight}")
    print()


def main():
    # Generate random submissions
    generate_rand_submissions()

    # Request: (employee, shift, day, weight)
    requests = set_requests()

    requests = add_missing_shifts_to_requests(requests)

    algo.solve_shift_scheduling(requests)


if __name__ == "__main__":
    main()