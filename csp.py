import copy
from operator import neg
from utils import first
from utils import count
from utils import argmin_random_tie
from problem import Problem
from collections import defaultdict
from sortedcontainers import SortedSet


class CSP(Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        count = 0
        for v in self.neighbors[(var)]:
            if len(assignment) == 0:
                return count
            else:
                tmp = v in assignment and not self.constraints(var, val, v, assignment[v])
            count += tmp

        return count

    def display(self, assignment):
        print(assignment)

    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            ls=[]
            for val in self.domains[var]:
                if self.nconflicts(var, val, assignment) == 0:
                    ls.append((var,val))

            return ls

    def result(self, state, action):
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    def conflicted_vars(self, current):
        return [var for var in self.variables if self.nconflicts(var, current[var], current) > 0]


class UniversalDict:
    def __init__(self, value): self.value = value

    def __getitem__(self, key): return self.value

    def __repr__(self): return '{{Any: {0!r}}}'.format(self.value)


class InstruCSP(CSP):

    def __init__(self, variables, domains, neighbors, constraints):
        super().__init__(variables, domains, neighbors, constraints)
        self.assignment_history = []

    def assign(self, var, val, assignment):
        super().assign(var, val, assignment)
        self.assignment_history.append(copy.deepcopy(assignment))

    def unassign(self, var, assignment):
        super().unassign(var, assignment)
        self.assignment_history.append(copy.deepcopy(assignment))


def different_values_constraint(A, a, B, b):
    return a != b


def MapColoringCSP(colors, neighbors):
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)


def parse_neighbors(neighbors):
    dic = defaultdict(list)
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        for B in Aneighbors.split():
            dic[A].append(B)
            dic[B].append(A)
    return dic


def make_instru(csp):
    return InstruCSP(csp.variables, csp.domains, csp.neighbors, csp.constraints)


# ---------------------------------------------------------------------------
# ----------------------------------- AC3 -----------------------------------
# ---------------------------------------------------------------------------

def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised


def dom_j_up(csp, queue):
    csp = csp
    queue = queue
    ss = SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))

    return ss


def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = set()
        for Xi in csp.variables:
            for Xk in csp.neighbors[(Xi)]:
                queue.add((Xi, (Xk)))

    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True


# ---------------------------------------------------------------------------
# ------------------------------ BACKTRACKING -------------------------------
# ---------------------------------------------------------------------------

def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])


def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)


def no_inference(csp, var, value, assignment, removals):
    return True


def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            conflicts = csp.nconflicts(var, value, assignment)
            if 0 == conflicts:
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0
                     for val in csp.domains[var])


def nconflicts(self, var, val, assignment):
    def conflict(var2):
        return (var2 in assignment and
                not self.constraints(var, val, var2, assignment[var2]))

    return count(conflict(v) for v in self.neighbors[var])


def mrv(assignment, csp):
    return argmin_random_tie(
        [v for v in csp.variables if v not in assignment],
        key=lambda var: num_legal_values(csp, var, assignment))


def lcv(var, assignment, csp):
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))


def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)