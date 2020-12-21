from itertools import product
from functools import partial
import math

from gurobipy import GRB as Gurobi, quicksum as Σ, Model
from gurobipy.GRB import BINARY, CONTINOUS
import toml

from foncteur import foncteur

# Distance metrics
euclidean_distance = lambda a, b: math.hypot(*zip(a,b))

# TODO: Implement this
# spherical_distance = lambda a, b: pass

def report(self, result_code):
    if result_code == Gurobi.callback.MESSAGE:
        print(self.__output,
            self.cbGet(Gurobi.callback.MSG_STRING))

def optimize(clients, facilities):
    # Indexes and accessors
    𝕱 = range(len(facilities))
    𝕮 = range(len(clients))
    𝕮×𝕱 = foncteur(product(𝕮, 𝕱))
    𝕱• = foncteur(facilities.__getitem__)
    𝕮• = foncteur(clients.__getitem__)

    # Init model
    model = Model()
    model.__output = StringIO.StringIO()
    model.setParam('TimeLimit', 10)

    # Variables
    _commacat = lambda x: ','.join(x) if isinstance(x, list) else x
    _add_vars = lambda v, ix, t, **a: {
        i: model.addVar(name=f"{v}_{_commacat(i)}", vtype=t, **a)
        for i in ix	}
    x = _add_vars('x', 𝕱, BINARY)
    y = _add_var('t', 𝕮×𝕱, CONTINOUS)
    d = 𝕮×𝕱 >= (𝕮• @ 𝕱•) >= euclidean_distance
    model.update()

    # Constraints & Objective
    for ij in 𝕮×𝕱:
        model.addConstr(y[ij] <= x[ij[1]])
    for i in 𝕮:
        model.addConstr(1 == norm(y @ e[j]))
    model.setObjective(ρ.T @ x + norm(d @ y), MINIMIZE)

    # Run model
    model.optimize(self.report)
    if (model.status != 2):
        return ["error"]

   # Extract solutions
    solution1 = filter(lambda i: x[i].X > .5, 𝕱)
    solution2 = filter(lambda ij: y[ij].X > .5, 𝕮×𝕱)

    return [solution1, solution2, output.getvalue()]

def unpack_data(_dict):
    if all(i in _dict for i in ['clients', 'facilities']):
        return (_dict['clients'], _dict['facilities'])
    else raise Exception("Data missing: ", _dict)

data = unpack_data(toml.load(sys.stdin))
result = {result: optimize(*data)}

print(toml.dumps(result))
