from pyeda.inter import exprvar, And, Or, expr2bdd
from pyeda.boolalg.bdd import BinaryDecisionDiagram
from typing import Tuple
from PetriNet import PetriNet
from collections import deque
import numpy as np


def bdd_reachable(pn: PetriNet) -> Tuple[BinaryDecisionDiagram, int]:
    # TODO trả về BinaryDecisionDiagram và số lượng reachable makes ()

    # Create BDD variables for each place
    place_vars = [exprvar(place_id) for place_id in pn.place_ids]

    # BFS to find all reachable markings
    visited = set()
    queue = deque()

    # Convert initial marking to tuple for hashing
    initial_marking_tuple = tuple(pn.M0)
    queue.append(pn.M0.copy())
    visited.add(initial_marking_tuple)

    reachable_markings = [pn.M0.copy()]

    # Add safety limit to prevent infinite loops
    MAX_ITERATIONS = 100000
    iterations = 0

    # Get the actual number of transitions from the matrix shape
    num_transitions = pn.I.shape[0]

    while queue and iterations < MAX_ITERATIONS:
        iterations += 1
        current_marking = queue.popleft()

        # Try firing each transition
        for t_idx in range(num_transitions):
            input_places = pn.I[t_idx]
            output_places = pn.O[t_idx]

            # Check if transition can fire
            # All input places must have enough tokens
            can_fire = True
            for i in range(len(current_marking)):
                if current_marking[i] < input_places[i]:
                    can_fire = False
                    break

            if can_fire:
                # Calculate new marking
                new_marking = current_marking - input_places + output_places

                # Check if new marking is valid (non-negative and respects 1-safe constraint)
                if np.all(new_marking >= 0) and np.all(new_marking <= 1):
                    new_marking_tuple = tuple(new_marking)

                    if new_marking_tuple not in visited:
                        visited.add(new_marking_tuple)
                        queue.append(new_marking.copy())
                        reachable_markings.append(new_marking.copy())

    # Build BDD from reachable markings
    # Each marking is a conjunction of literals (p_i if marking[i] > 0, ~p_i if marking[i] == 0)
    marking_expressions = []
    for marking in reachable_markings:
        literals = []
        for i, place_var in enumerate(place_vars):
            if marking[i] > 0:
                literals.append(place_var)
            else:
                literals.append(~place_var)
        marking_expressions.append(And(*literals))

    # Create the BDD as disjunction of all reachable markings
    bdd_expr = Or(*marking_expressions)
    bdd = expr2bdd(bdd_expr)

    return bdd, len(reachable_markings)
