import numpy as np
def european_call_payoff(S_T, K, r, T):
    """
    Calculate the payoff of the option

    Parameters
    ----------
    S_T : np.ndarray
        Array of shape (n_paths, n_steps+1) containing simulated asset paths
    K : float
        Strike price 
    r : float
        Risk-free interest rate
    
    T : float
        Time horizon (years)
    
    Returns
    -------
    Payoff of the option
    """
    return np.exp(-r * T) * np.maximum(S_T - K, 0)