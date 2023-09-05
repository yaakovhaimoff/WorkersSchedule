import random
import algo_tryout as algo
import src.consts.consts as c

# Generate a list of unique employee IDs
employee_ids = [_ for _ in range(c.num_employees)]

# Create a dictionary to store submissions for each worker
worker_submissions = {employee_id: [] for employee_id in employee_ids}


def generate_rand_submissions():
    for day in c.days_of_week:
        for shift_type in c.shifts_per_day[day]:
            num_submissions = random.randint(0, c.num_total_shifts)
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
            requests.append((employee_id, c.shifts_in_nums.get(shift_type), c.days_in_nums.get(day), c.want_to_work))
    return requests


def add_missing_shifts_to_requests(requests):
    # Identify shifts that workers didn't submit
    all_shifts = set()
    for day, day_shifts in c.shifts_per_day.items():
        all_shifts.update([(day, shift) for shift in day_shifts])

    missing_shifts = []
    for employee_id in worker_submissions:
        for shift in all_shifts:
            if shift not in worker_submissions[employee_id] and shift not in missing_shifts:
                missing_shifts.append((employee_id, c.shifts_in_nums.get(shift[1]), c.days_of_week.index(shift[0]), c.doesnt_want_work))

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
