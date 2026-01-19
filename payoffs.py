import numpy as np
def european_call_payoff(S_T, K, r, T):
    return np.exp(-r * T) * np.maximum(S_T - K, 0)