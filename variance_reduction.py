import numpy as np
def control_variate_estimator(X, Y, Y_expectation):
    """
    Uses a control variate to reduce variance in estimating the expectation of X.

    Parameters
    ----------
    X : float
        payoff
    Y : float
        a random variable whose expectation is known
    Y_expectation : float
        The expectation of Y
    
    Returns
    -------
    A low variance estimate for the expectation of X.
    """
    cov_XY = np.cov(X, Y, ddof=1)[0, 1]
    var_Y = np.var(Y, ddof=1)
    beta = cov_XY / var_Y
    return X.mean() + beta * (Y_expectation - Y.mean())

def antithetic_normals(n_paths, n_steps, seed=None):
    """
    Generates an array of values drawn from the standard normal distribution, and, for each value, its negative.

    Parameters
    ----------
    n_steps : int
        Number of time steps
    n_paths : int
        Number of simulated paths
    seed : int or None
        Random seed for reproducibility
    
    Returns
    -------
    Z : ndarray
        array of values from the standard normal distribution
    """
    if seed is not None:
        np.random.seed(seed)
    Z_half = np.random.normal(0, 1, size=(n_paths // 2, n_steps))
    return np.vstack([Z_half, -Z_half])
    