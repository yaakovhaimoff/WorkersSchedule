from ortools.sat.python import cp_model
import src.consts.consts as c


def solve_shift_scheduling(requests):
    model = cp_model.CpModel()

    work = {}
    for e in range(c.num_employees):
        for s in range(c.num_shifts):
            for d in range(c.num_days):
                work[e, s, d] = model.NewBoolVar("work%i_%i_%i" % (e, s, d))

    # Linear terms of the objective in a minimization context.
    obj_int_vars = []
    obj_int_coeffs = []
    obj_bool_vars = []
    obj_bool_coeffs = []

    # Exactly one shift per day.
    for e in range(c.num_employees):
        for d in range(c.num_days):
            model.AddExactlyOne(work[e, s, d] for s in range(c.num_shifts))

    # Employee requests
    for e, s, d, w in requests:
        if w > 0:
            model.Add(work[e, s, d] == 0)
        else:
            obj_bool_vars.append(work[e, s, d])
            obj_bool_coeffs.append(w)

    # Shift constraints
    for ct in c.shift_constraints:
        shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
        for e in range(c.num_employees):
            works = [work[e, shift, d] for d in range(c.num_days)]
            variables, coeffs = add_soft_sequence_constraint(
                model,
                works,
                hard_min,
                soft_min,
                min_cost,
                soft_max,
                hard_max,
                max_cost,
                "shift_constraint(employee %i, shift %i)" % (e, shift),
            )
            obj_bool_vars.extend(variables)
            obj_bool_coeffs.extend(coeffs)

    # Weekly sum constraints
    for ct in c.weekly_sum_constraints:
        shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
        for e in range(c.num_employees):
            for w in range(c.num_weeks):
                works = [work[e, shift, d + w * 7] for d in range(7)]
                variables, coeffs = add_soft_sum_constraint(
                    model,
                    works,
                    hard_min,
                    soft_min,
                    min_cost,
                    soft_max,
                    hard_max,
                    max_cost,
                    "weekly_sum_constraint(employee %i, shift %i, week %i)"
                    % (e, shift, w),
                )
                obj_int_vars.extend(variables)
                obj_int_coeffs.extend(coeffs)

    # Penalized transitions
    for previous_shift, next_shift, cost in c.penalized_transitions:
        for e in range(c.num_employees):
            for d in range(c.num_days - 1):
                transition = [
                    work[e, previous_shift, d].Not(),
                    work[e, next_shift, d + 1].Not(),
                ]
                if cost == 0:
                    model.AddBoolOr(transition)
                else:
                    trans_var = model.NewBoolVar(
                        "transition (employee=%i, day=%i)" % (e, d)
                    )
                    transition.append(trans_var)
                    model.AddBoolOr(transition)
                    obj_bool_vars.append(trans_var)
                    obj_bool_coeffs.append(cost)

    # Cover constraints
    for s in range(1, c.num_shifts):
        for w in range(c.num_weeks):
            for d in range(7):
                works = [work[e, s, w * 7 + d] for e in range(c.num_employees)]
                # Ignore Off shift.
                min_demand = c.weekly_cover_demands[d][s - 1]
                worked = model.NewIntVar(min_demand, c.num_employees, "")
                model.Add(worked == sum(works))
                over_penalty = c.excess_cover_penalties[s - 1]
                if over_penalty > 0:
                    name = "excess_demand(shift=%i, week=%i, day=%i)" % (s, w, d)
                    excess = model.NewIntVar(0, c.num_employees - min_demand, name)
                    model.Add(excess == worked - min_demand)
                    obj_int_vars.append(excess)
                    obj_int_coeffs.append(over_penalty)

    # Objective
    model.Minimize(
        sum(obj_bool_vars[i] * obj_bool_coeffs[i] for i in range(len(obj_bool_vars)))
        + sum(obj_int_vars[i] * obj_int_coeffs[i] for i in range(len(obj_int_vars)))
    )

    solver = cp_model.CpSolver()
    solution_printer = cp_model.ObjectiveSolutionPrinter()
    status = solver.Solve(model, solution_printer)

    print_solution(solver, work, status)
    print_penalties(solver, obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs)
    print_stats(solver, status)


def add_soft_sequence_constraint(
        model, works, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost, prefix
):
    cost_literals = []
    cost_coefficients = []

    # Forbid sequences that are too short.
    for length in range(1, hard_min):
        for start in range(len(works) - length + 1):
            model.AddBoolOr(negated_bounded_span(works, start, length))

    # Penalize sequences that are below the soft limit.
    if min_cost > 0:
        for length in range(hard_min, soft_min):
            for start in range(len(works) - length + 1):
                span = negated_bounded_span(works, start, length)
                name = ": under_span(start=%i, length=%i)" % (start, length)
                lit = model.NewBoolVar(prefix + name)
                span.append(lit)
                model.AddBoolOr(span)
                cost_literals.append(lit)
                # We filter exactly the sequence with a short length.
                # The penalty is proportional to the delta with soft_min.
                cost_coefficients.append(min_cost * (soft_min - length))

    # Penalize sequences that are above the soft limit.
    if max_cost > 0:
        for length in range(soft_max + 1, hard_max + 1):
            for start in range(len(works) - length + 1):
                span = negated_bounded_span(works, start, length)
                name = ": over_span(start=%i, length=%i)" % (start, length)
                lit = model.NewBoolVar(prefix + name)
                span.append(lit)
                model.AddBoolOr(span)
                cost_literals.append(lit)
                # Cost paid is max_cost * excess length.
                cost_coefficients.append(max_cost * (length - soft_max))

    # Just forbid any sequence of true variables with length hard_max + 1
    for start in range(len(works) - hard_max):
        model.AddBoolOr([works[i].Not() for i in range(start, start + hard_max + 1)])
    return cost_literals, cost_coefficients


def negated_bounded_span(works, start, length):
    sequence = []
    # Left border (start of works, or works[start - 1])
    if start > 0:
        sequence.append(works[start - 1])
    for i in range(length):
        sequence.append(works[start + i].Not())
    # Right border (end of works or works[start + length])
    if start + length < len(works):
        sequence.append(works[start + length])
    return sequence


def add_soft_sum_constraint(
        model, works, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost, prefix
):
    cost_variables = []
    cost_coefficients = []
    sum_var = model.NewIntVar(hard_min, hard_max, "")
    # This adds the hard constraints on the sum.
    model.Add(sum_var == sum(works))

    # Penalize sums below the soft_min target.
    if soft_min > hard_min and min_cost > 0:
        delta = model.NewIntVar(-len(works), len(works), "")
        model.Add(delta == soft_min - sum_var)
        # TODO(user): Compare efficiency with only excess >= soft_min - sum_var.
        excess = model.NewIntVar(0, 7, prefix + ": under_sum")
        model.AddMaxEquality(excess, [delta, 0])
        cost_variables.append(excess)
        cost_coefficients.append(min_cost)

    # Penalize sums above the soft_max target.
    if soft_max < hard_max and max_cost > 0:
        delta = model.NewIntVar(-7, 7, "")
        model.Add(delta == sum_var - soft_max)
        excess = model.NewIntVar(0, 7, prefix + ": over_sum")
        model.AddMaxEquality(excess, [delta, 0])
        cost_variables.append(excess)
        cost_coefficients.append(max_cost)

    return cost_variables, cost_coefficients


def print_solution(solver, work, status):
    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print()
        header = "          "
        for w in range(c.num_weeks):
            header += "S M T W T F S "
        print(header)
        for e in range(c.num_employees):
            schedule = ""
            for d in range(c.num_days):
                for s in range(c.num_shifts):
                    if solver.BooleanValue(work[e, s, d]):
                        schedule += c.shifts[s] + " "
            print("worker %i: %s" % (e, schedule))
        print()


def print_penalties(solver, obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs):
    print("Penalties:")
    for i, var in enumerate(obj_bool_vars):
        if solver.BooleanValue(var):
            penalty = obj_bool_coeffs[i]
            if penalty > 0:
                print("  %s violated, penalty=%i" % (var.Name(), penalty))
            else:
                print("  %s fulfilled, gain=%i" % (var.Name(), -penalty))

    for i, var in enumerate(obj_int_vars):
        if solver.Value(var) > 0:
            print(
                "  %s violated by %i, linear penalty=%i"
                % (var.Name(), solver.Value(var), obj_int_coeffs[i])
            )


def print_stats(solver, status):
    print()
    print("Statistics")
    print("  - status          : %s" % solver.StatusName(status))
    print("  - conflicts       : %i" % solver.NumConflicts())
    print("  - branches        : %i" % solver.NumBranches())
    print("  - wall time       : %f s" % solver.WallTime())
