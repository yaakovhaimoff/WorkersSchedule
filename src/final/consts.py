# Data
num_employees = 8
num_weeks = 3
shifts = ["M", "A", "N"]

# Fixed assignment: (employee, shift, day).
# This fixes the first 2 days of the schedule.
fixed_assignments = [
    (0, 0, 0),  # Worker 0 if off on day 0.
    (1, 0, 0),  # Worker 1 if off on day 0.
    (2, 1, 0),  # Worker 2 works on the morning on day 0.
    (3, 1, 0),  # Worker 3 works on the morning on day 0.
    (4, 2, 0),  # Worker 4 works in the afternoon on day 0.
    (5, 2, 0),  # Worker 5 works in the afternoon on day 0.
    (6, 2, 0),  # Worker 6 works in the afternoon on day 3.
    (7, 3, 0),  # Worker 7 works on the night on day 0.

    (0, 1, 1),
    (1, 1, 1),
    (2, 2, 1),
    (3, 2, 1),
    (4, 2, 1),
    (5, 0, 1),
    (6, 0, 1),
    (7, 3, 1),
]

# Request: (employee, shift, day, weight)
# A negative weight indicates that the employee desire this assignment.
requests = [
    # Employee 3 does not want to work on the first Saturday (negative weight
    # for the Off shift).
    (3, 0, 5, -2),
    # Employee 5 wants a night shift on the second Thursday (negative weight).
    (5, 3, 10, -2),
    # Employee 2 does not want a night shift on the first Friday (positive
    # weight).
    (2, 3, 4, 4),
]

# Shift constraints on continuous sequence :
#     (shift, hard_min, soft_min, min_penalty,
#             soft_max, hard_max, max_penalty)
shift_constraints = [
    # One or two consecutive days of rest, this is a hard constraint.
    (0, 1, 1, 0, 2, 2, 0),
    # between 2 and 3 consecutive days of night shifts, 1 and 4 are
    # possible but penalized.
    (3, 1, 2, 20, 3, 4, 5),
]

# Weekly sum constraints on shifts days:
#     (shift, hard_min, soft_min, min_penalty,
#             soft_max, hard_max, max_penalty)
weekly_sum_constraints = [
    # Constraints on rests per week.
    (0, 1, 2, 7, 2, 3, 4),
    # At least 1 night shift per week (penalized). At most 4 (hard).
    (3, 0, 1, 3, 4, 4, 0),
]

# Penalized transitions:
#     (previous_shift, next_shift, penalty (0 means forbidden))
penalized_transitions = [
    # Afternoon to night has a penalty of 4.
    (2, 3, 4),
    # Night to morning is forbidden.
    (3, 1, 0),
]

# daily demands for work shifts (morning, afternoon, night) for each day
# of the week starting on Monday.
weekly_cover_demands = [
    (2, 3, 1),  # Monday
    (2, 3, 1),  # Tuesday
    (2, 2, 2),  # Wednesday
    (2, 3, 1),  # Thursday
    (2, 2, 2),  # Friday
    (1, 2, 3),  # Saturday
    (1, 3, 1),  # Sunday
]

# Penalty for exceeding the cover constraint per shift type.
excess_cover_penalties = (2, 2, 5)

num_days = num_weeks * 7
num_shifts = len(shifts)
