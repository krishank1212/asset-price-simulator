import numpy as np
import scipy.stats as stats
def black_scholes(S0, K, r, sigma, T):
    '''
    Black-Scholes formula for European call option pricing.
    
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
        
    Returns
    -------
    call_price : float
        Theoretical option price
    '''
    d1 = (np.log(S0 /K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S0 * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    return call_price