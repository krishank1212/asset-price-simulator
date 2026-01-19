# About the project
As my interest in quantitative finance begins to develop, I wanted to implement some of the maths that's important in the role of finance. One of the pivotal equations is the Black-Scholes equation. This program compares Monte Carlo simulations of a European call option price under Geometric Brownian Motion (GBM), and compares the asset price with the theoretical price that is produced from the Black-Scholes equation. It also demonstrates how the Monte Carlo method converges to the theoretical value as the number of paths increases.

# How it's made
The project is made entirely in Python, and is my first experience using the modules `numpy` and `scipy`. I also used `matplotlib` to plot the results to visually compare how the Monte Carlo simulations converge to the theoretical value. The maths works as follows:

- I produced small time increments by dividing the time horizon by the number of time steps.
- Using the Z distribution, I generated random sized increments, and multiplied these by the square root of the small time increments.
- Since we assume that the increments have a lognormal distribution, I applied the GBM formula to calculate the increments.
- I then summed these to find the logarithm of the cumulative sum.
- This is then exponentiated and multiplied by the initial stock price to find the final value.
- This completed over all the desired number of paths.
- The Monte Carlo simulator uses this GBM simulation to calculate the payoff of each path at maturity.
- The average payoff is discounted back to the present value.
- The Black-Scholes equation then uses the same parameters to find the theoretical value of the stock.
- Using varying number of paths, I observed how the absolute error between the Monte Carlo values and Black-Scholes value changed, and plotted this.

# Optimisations
The key factor that drives the error between the Monte Carlo and Black-Scholes prices, for any number of paths, is the variance of the Monte Carlo method. I employed different strategies to reduce the variance.
## Antithetic Variates
Antithetic variates use the symmetry in the normal distribution to reduce the variance. For every value Z I drew, I also drew -Z, and thus, only have to draw half the number of increments. By pairing samples, I introduce negative correlation into the sample and reduce the variance.
## Control Variates
Control variates reduce the variance in the Monte Carlo simulation by subtracting a correlated random variable whose true average is already known. I implemented a random variable Y whose PDF is complex but has a known expectation and is strongly correlated with the option payoff. This means that if my option pay off is unusually high, so is Y, and same logic if the option payoff is unusually low.  This makes the difference between the option payoff and Y more stable, which can be exploited to more easily calculate the expected payoff. A multiplicative constant, beta, is introduced to ensure that the payoff and Y fluctuate by the same amount.

# Lessons I learnt
This project has given me a much deeper insight into not just the mathematics by which the stock market operates, but also an understanding of how computational power can be used to simulate and predict such conclusions. I've also greatly improved my `numpy` skills as a result, and look forward to learning other important mathematical modules in Python and other languages.
