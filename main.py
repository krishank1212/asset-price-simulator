import matplotlib.pyplot as plt
from analytics import black_scholes
from pricing import monte_carlo
S0 = 100
K = 100
r = 0.03
sigma = 0.2
T = 1.0
n_steps = 252


path_counts = [500, 1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000]
mean_errors = []
M = 30
bs_price = black_scholes(S0, K, r, sigma, T)
for N in path_counts:
    error = 0
    for i in range(M):
        mc_price = monte_carlo(S0, K, r, sigma, T, n_steps, N)
        error += abs(mc_price - bs_price)
    mean_error = error/M
    mean_errors.append(mean_error)
plt.loglog(path_counts, mean_errors, marker='o')
plt.xlabel("Number of Monte Carlo Paths")
plt.ylabel("Absolute pricing error")
plt.show()