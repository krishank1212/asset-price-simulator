import numpy as np
from processes import simulate_gbm
from payoffs import european_call_payoff
from variance_reduction import control_variate_estimator, antithetic_normals
def monte_carlo(S0, K, r, sigma, T, n_steps, n_paths, seed=None):
    """
    Monte Carlo simulation to price a European call option.

    Parameters
    ----------
    S0 : float
        Initial stock price
    K : float
        Strike price
    r : float
        Risk-free interest rate
    sigma : float
        Volatility
    T : float
        Time to maturity (years)
    n_steps : int
        Number of time steps
    n_paths : int
        Number of simulated paths
    seed : int or None
        Random seed for reproducibility

    Returns
    -------
    X : float
        Estimated option price
    """
    Z = antithetic_normals(n_paths, n_steps)
    S = simulate_gbm(S0, r, sigma, T, Z)
    X = european_call_payoff(S[:, -1], K, r, T)
    Y = np.exp(-r * T) * S[:, -1]
    return control_variate_estimator(X, Y, S0)
