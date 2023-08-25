"""Creates a shift scheduling problem and solves it."""

from absl import app
from absl import flags

from ortools.sat.python import cp_model
from google.protobuf import text_format

import consts as c

_OUTPUT_PROTO = flags.DEFINE_string(
    "output_proto", "", "Output file to write the cp_model proto to."
)
_PARAMS = flags.DEFINE_string(
    "params", "max_time_in_seconds:10.0", "Sat solver parameters."
)


class ModelWrapper(object):
    def __init__(self, model):
        self._model = model
        self._work = {}
        self._solution_count = 0
        self.obj_int_vars = []
        self.obj_int_coeffs = []
        self.obj_bool_vars = []
        self.obj_bool_coeffs = []

    def get_model(self):
        return self._model

    def geet_solution_count(self):
        return self._solution_count

    def get_obj_int_vars(self):
        return self.obj_int_vars

    def get_obj_int_coeffs(self):
        return self.obj_int_coeffs

    def get_obj_bool_vars(self):
        return self.obj_bool_vars

    def get_obj_bool_coeffs(self):
        return self.obj_bool_coeffs

    def get_work(self):
        return self._work

    def set_model(self):
        self.create_shift_variables()
        self.set_exactly_one_shift_per_day()
        self.set_fixed_assignments()
        self.set_employee_requests()
        self.set_shift_constraints()
        self.set_weekly_sum_constraints()
        self.set_penalized_transitions()
        self.set_cover_constraints()

    def create_shift_variables(self):
        # Creates all shift variables for each worker.
        for e in range(c.num_employees):
            for s in range(c.num_shifts):
                for d in range(c.num_days):
                    self._work[e, s, d] = self._model.NewBoolVar("work%i_%i_%i" % (e, s, d))

    def set_exactly_one_shift_per_day(self):
        # Exactly one shift per day for each worker constraint.
        for e in range(c.num_employees):
            for d in range(c.num_days):
                self._model.AddExactlyOne(self._work[e, s, d] for s in range(c.num_shifts))

    def set_fixed_assignments(self):
        # Fixed assignments
        # (adding the fixed assignments as constraints thus they'll must be honored).
        for e, s, d in c.fixed_assignments:
            self._model.Add(self._work[e, s, d] == 1)

    def set_employee_requests(self):
        # Employee requests
        for e, s, d, w in c.requests:
            self.obj_bool_vars.append(self._work[e, s, d])
            self.obj_bool_coeffs.append(w)

    def set_shift_constraints(self):
        # Shift constraints
        for ct in c.shift_constraints:
            shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
            for e in range(c.num_employees):
                works = [self._work[e, shift, d] for d in range(c.num_days)]
                variables, coeffs = add_soft_sequence_constraint(
                    self._model,
                    works,
                    hard_min,
                    soft_min,
                    min_cost,
                    soft_max,
                    hard_max,
                    max_cost,
                    "shift_constraint(employee %i, shift %i)" % (e, shift),
                )
                self.obj_bool_vars.extend(variables)
                self.obj_bool_coeffs.extend(coeffs)

    def set_weekly_sum_constraints(self):
        # Weekly sum constraints
        for ct in c.weekly_sum_constraints:
            shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
            for e in range(c.num_employees):
                for w in range(c.num_weeks):
                    works = [self._work[e, shift, d + w * 7] for d in range(7)]
                    variables, coeffs = add_soft_sum_constraint(
                        self._model,
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
                    self.obj_int_vars.extend(variables)
                    self.obj_int_coeffs.extend(coeffs)

    def set_penalized_transitions(self):
        # Penalized transitions
        for previous_shift, next_shift, cost in c.penalized_transitions:
            for e in range(c.num_employees):
                for d in range(c.num_days - 1):
                    transition = [
                        self._work[e, previous_shift, d].Not(),
                        self._work[e, next_shift, d + 1].Not(),
                    ]
                    if cost == 0:
                        self._model.AddBoolOr(transition)
                    else:
                        trans_var = self._model.NewBoolVar(
                            "transition (employee=%i, day=%i)" % (e, d)
                        )
                        transition.append(trans_var)
                        self._model.AddBoolOr(transition)
                        self.obj_bool_vars.append(trans_var)
                        self.obj_bool_coeffs.append(cost)

    def set_cover_constraints(self):
        # Cover constraints
        for s in range(1, c.num_shifts):
            for w in range(c.num_weeks):
                for d in range(7):
                    works = [self._work[e, s, w * 7 + d] for e in range(c.num_employees)]
                    # Ignore Off shift.
                    min_demand = c.weekly_cover_demands[d][s - 1]
                    worked = self._model.NewIntVar(min_demand, c.num_employees, "")
                    self._model.Add(worked == sum(works))
                    over_penalty = c.excess_cover_penalties[s - 1]
                    if over_penalty > 0:
                        name = "excess_demand(shift=%i, week=%i, day=%i)" % (s, w, d)
                        excess = self._model.NewIntVar(0, c.num_employees - min_demand, name)
                        self._model.Add(excess == worked - min_demand)
                        self.obj_int_vars.append(excess)
                        self.obj_int_coeffs.append(over_penalty)


def solve_shift_scheduling(params, output_proto):
    """Solves the shift scheduling problem."""
    m_w = ModelWrapper(cp_model.CpModel())
    m_w.set_model()

    # Objective
    m_w.get_model().Minimize(
        sum(m_w.obj_bool_vars[i] * m_w.obj_bool_coeffs[i] for i in range(len(m_w.obj_bool_vars)))
        + sum(m_w.obj_int_vars[i] * m_w.obj_int_coeffs[i] for i in range(len(m_w.obj_int_vars)))
    )

    if output_proto:
        print("Writing proto to %s" % output_proto)
        with open(output_proto, "w") as text_file:
            text_file.write(str(m_w.get_model()))

    # Solve the model.
    solver = cp_model.CpSolver()
    if params:
        text_format.Parse(params, solver.parameters)
    solution_printer = cp_model.ObjectiveSolutionPrinter()
    status = solver.Solve(m_w.get_model(), solution_printer)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print()
        header = "          "
        for w in range(c.num_weeks):
            header += "M T W T F S S "
        print(header)
        for e in range(c.num_employees):
            schedule = ""
            for d in range(c.num_days):
                for s in range(c.num_shifts):
                    if solver.BooleanValue(m_w.get_work()[e, s, d]):
                        schedule += c.shifts[s] + " "
            print("worker %i: %s" % (e, schedule))
        print()
        print("Penalties:")
        for i, var in enumerate(m_w.obj_bool_vars):
            if solver.BooleanValue(var):
                penalty = m_w.obj_bool_coeffs[i]
                if penalty > 0:
                    print("  %s violated, penalty=%i" % (var.Name(), penalty))
                else:
                    print("  %s fulfilled, gain=%i" % (var.Name(), -penalty))

        for i, var in enumerate(m_w.obj_int_vars):
            if solver.Value(var) > 0:
                print(
                    "  %s violated by %i, linear penalty=%i"
                    % (var.Name(), solver.Value(var), m_w.obj_int_coeffs[i])
                )

    print()
    print("Statistics")
    print("  - status          : %s" % solver.StatusName(status))
    print("  - conflicts       : %i" % solver.NumConflicts())
    print("  - branches        : %i" % solver.NumBranches())
    print("  - wall time       : %f s" % solver.WallTime())


def add_soft_sequence_constraint(
        model, works, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost, prefix
):
    """Sequence constraint on true variables with soft and hard bounds.

    This constraint look at every maximal contiguous sequence of variables
    assigned to true. If forbids sequence of length < hard_min or > hard_max.
    Then it creates penalty terms if the length is < soft_min or > soft_max.

    Args:
      model: the sequence constraint is built on this model.
      works: a list of Boolean variables.
      hard_min: any sequence of true variables must have a length of at least
        hard_min.
      soft_min: any sequence should have a length of at least soft_min, or a
        linear penalty on the delta will be added to the objective.
      min_cost: the coefficient of the linear penalty if the length is less than
        soft_min.
      soft_max: any sequence should have a length of at most soft_max, or a linear
        penalty on the delta will be added to the objective.
      hard_max: any sequence of true variables must have a length of at most
        hard_max.
      max_cost: the coefficient of the linear penalty if the length is more than
        soft_max.
      prefix: a base name for penalty literals.

    Returns:
      a tuple (variables_list, coefficient_list) containing the different
      penalties created by the sequence constraint.
    """
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


def add_soft_sum_constraint(
        model, works, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost, prefix
):
    """Sum constraint with soft and hard bounds.

    This constraint counts the variables assigned to true from works.
    If forbids sum < hard_min or > hard_max.
    Then it creates penalty terms if the sum is < soft_min or > soft_max.

    Args:
      model: the sequence constraint is built on this model.
      works: a list of Boolean variables.
      hard_min: any sequence of true variables must have a sum of at least
        hard_min.
      soft_min: any sequence should have a sum of at least soft_min, or a linear
        penalty on the delta will be added to the objective.
      min_cost: the coefficient of the linear penalty if the sum is less than
        soft_min.
      soft_max: any sequence should have a sum of at most soft_max, or a linear
        penalty on the delta will be added to the objective.
      hard_max: any sequence of true variables must have a sum of at most
        hard_max.
      max_cost: the coefficient of the linear penalty if the sum is more than
        soft_max.
      prefix: a base name for penalty variables.

    Returns:
      a tuple (variables_list, coefficient_list) containing the different
      penalties created by the sequence constraint.
    """
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


def negated_bounded_span(works, start, length):
    """Filters an isolated sub-sequence of variables assined to True.

    Extract the span of Boolean variables [start, start + length), negate them,
    and if there is variables to the left/right of this span, surround the span by
    them in non negated form.

    Args:
      works: a list of variables to extract the span from.
      start: the start to the span.
      length: the length of the span.

    Returns:
      a list of variables which conjunction will be false if the sub-list is
      assigned to True, and correctly bounded by variables assigned to False,
      or by the start or end of works.
    """
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


def main(_):
    solve_shift_scheduling(_PARAMS.value, _OUTPUT_PROTO.value)


if __name__ == "__main__":
    app.run(main)
