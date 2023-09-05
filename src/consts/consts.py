# Data
shifts = ["O", "M", "A", "N"]
# shifts = ["M", "A", "N"]
num_employees = 3
num_weeks = 1
num_days = num_weeks * 7
num_shifts = len(shifts)
# num_total_shifts = len(shifts) * num_weeks * num_days
num_total_shifts = len(shifts) * num_weeks * num_days

# Penalty for exceeding the cover constraint per shift type.
excess_cover_penalties = (2, 2, 5)

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

# Shift constraints on continuous sequence :
#     (shift, hard_min, soft_min, min_penalty,
#             soft_max, hard_max, max_penalty)
shift_constraints = [
    # One or two consecutive days of rest, this is a hard constraint.
    (0, 1, 1, 0, 2, 2, 0),
    # between 2 and 3 consecutive days of night shifts, 1 and 4 are
    # possible but penalized.
    # (3, 1, 2, 20, 3, 4, 5),
    (2, 1, 2, 20, 3, 4, 5),
]

# Weekly sum constraints on shifts days:
#     (shift, hard_min, soft_min, min_penalty,
#             soft_max, hard_max, max_penalty)
weekly_sum_constraints = [
    # Constraints on rests per week.
    (0, 1, 2, 7, 2, 3, 4),

    # # At least 1 night shift per week (penalized). At most 4 (hard).
    # # (3, 0, 1, 3, 4, 4, 0),
    # (2, 0, 1, 3, 4, 4, 0),
]

# Penalized transitions:
#     (previous_shift, next_shift, penalty (0 means forbidden))
penalized_transitions = [
    # Afternoon to night has a penalty of 4.
    # (2, 3, 4),
    (1, 2, 4),
    # Night to morning is forbidden.
    # (3, 1, 0),
    (2, 0, 0),
]

# daily demands for work shifts (morning, afternoon, night) for each day
# of the week starting on Monday.
weekly_cover_demands = [
    (1, 1, 1),  # Sunday
    (1, 1, 1),  # Monday
    (1, 1, 1),  # Tuesday
    (1, 1, 1),  # Wednesday
    (1, 1, 1),  # Thursday
    (1, 1, 1),  # Friday
    (1, 1, 1),  # Saturday
]