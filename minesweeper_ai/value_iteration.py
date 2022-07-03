from environment import Environment

def get_initial_U(mdp):
    U = {}
    for s in mdp.get_possible_states():
        U[mdp.getIdByState(s)] = mdp.getReward(s)
    return U


def Q_Value(mdp, s, a, U):
    Q = 0.0
    possible_states = mdp.get_possible_states()
    for s_p in possible_states:
        P = mdp.get_transition_prob(a, s_p, s)
        R = mdp.getReward(s_p, a)
        Q += P * (R + U[mdp.getIdByState(s_p)])
    return Q


def ValueIteration(mdp, error=0.00001):
    # from AIMA 4th edition without discount gamma
    U_p = get_initial_U(mdp)  # U_p = U'
    delta = float('inf')
    while delta > error:
        U = {}
        for s in mdp.get_possible_states():
            U[mdp.getIdByState(s)] = U_p[mdp.getIdByState(s)]
        print_U(U, mdp)  # to illustrate the iteration process
        delta = 0
        for s in mdp.get_possible_states():
            max_a = float('-inf')
            for a in mdp.get_actions():
                q = Q_Value(mdp, s, a, U)
                if q > max_a:
                    max_a = q
            U_p[mdp.getIdByState(s)] = max_a
            if abs(U_p[mdp.getIdByState(s)] - U[mdp.getIdByState(s)]) > delta:
                delta = abs(U_p[mdp.getIdByState(s)] - U[mdp.getIdByState(s)])
    return U


def print_U(U, mdp):
    print('Utilities:')
    for key, value in U.items():
        print(mdp.getStateById(key), '->', value)
    print('                   ', end='')


def print_policy(pi, mdp):
    print('Policy:')
    for key, value in pi.items():
        print(mdp.getStateById(key), '->', value)
    print('                   ', end='')



def train():
    mdp = Environment(2, 3, 1, -0.04, 1)
    U = ValueIteration(mdp)
    print_U(U, mdp)

    pi_star = {}
    for s in mdp.get_possible_states():
        if mdp.isDone(s):
            continue  # policy is not needed in stop states
        max_a = float('-inf')
        argmax_a = None
        for action in mdp.get_actions():
            q = Q_Value(mdp, s, action, U)
            if q > max_a:
                max_a = q
                argmax_a = action
        pi_star[mdp.getIdByState(s)] = argmax_a

    print_policy(pi_star, mdp)
    return pi_star