import numpy as np
def control_variate_estimator(X, Y, Y_expectation):
    cov_XY = np.cov(X, Y, ddof=1)[0, 1]
    var_Y = np.var(Y, ddof=1)
    beta = cov_XY / var_Y
    return X.mean() + beta * (Y_expectation - Y.mean())

def antithetic_normals(n_paths, n_steps, seed=None):
    if seed is not None:
        np.random.seed(seed)
    Z_half = np.random.normal(0, 1, size=(n_paths // 2, n_steps))
    return np.vstack([Z_half, -Z_half])
    