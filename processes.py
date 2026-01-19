import numpy as np
def simulate_gbm(S0, r, sigma, T, Z):
    """
    Simulate n_paths of a Geometric Brownian Motion (GBM).

    Parameters
    ----------
    S0 : float
        Initial stock price
    r : float
        Risk-free interest rate
    sigma : float
        Volatility
    T : float
        Time horizon (years)
    n_steps : int
        Number of time steps
    n_paths : int
        Number of simulated paths
    seed : int or None
        Random seed for reproducibility

    Returns
    -------
    S : np.ndarray
        Array of shape (n_paths, n_steps+1) containing simulated asset paths
    """
    
    dt = T / Z.shape[1]
    dW = np.sqrt(dt) * Z
    log_increment = ((r - 0.5 * sigma**2)*dt + sigma*dW)
    log_S = np.cumsum(log_increment, axis=1)
    S = S0 * np.exp(log_S)
    
    return S
