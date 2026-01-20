# About the project
This project implements and analyses Monte Carlo pricing of a European call option under the Black–Scholes framework, with the underlying asset modelled as a Geometric Brownian Motion (GBM). The primary aim was not just to obtain an option price, but to study convergence behaviour and variance reduction techniques, and to compare empirical Monte Carlo estimates with the closed-form Black–Scholes solution.

In particular, I investigate how the Monte Carlo estimator converges to the analytical price as the number of simulated paths increases, and how variance reduction techniques improve efficiency for a fixed computational budget.
# How it's made
## Mathematical Model

Under the Black–Scholes assumptions, the asset price $S_t$ follows the stochastic differential equation

$dS_t = \mu S_t \ dt + \sigma S_t \, dW_t$,

where $\mu$ is the drift, $\sigma$ the volatility, and $W_t$ a standard Brownian motion.

Discretising this SDE over small time steps $\Delta t$, the terminal asset price is simulated using

$S_T = S_0 \exp\left( \left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma \sqrt{T} Z \right),
\quad Z \sim \mathcal{N}(0,1)$.

For each simulated path, the payoff of a European call option is computed as

$\max(S_T - K, 0)$,

and the Monte Carlo price is obtained by discounting the average payoff under the risk-neutral measure.

The analytical Black–Scholes price is computed using the same parameters, allowing a direct comparison between simulated and theoretical values.

## Implementation
The project is implemented in Python, using:
- `NumPy` for vectorised simulation of paths,
- `SciPy` for evaluating the Black–Scholes formula,
- `Matplotlib` for visualising convergence and error behaviour.

To study convergence, I varied the number of Monte Carlo paths and plotted the absolute pricing error against the theoretical Black–Scholes value, observing the expected $O(N^{-1/2})$ convergence rate for the naïve estimator.

# Optimisations
A key limitation of standard Monte Carlo pricing is its high variance. I implemented two classical variance reduction methods to improve estimator efficiency.
## Antithetic Variates
Antithetic variates use the symmetry in the normal distribution to reduce the variance. For every value $\quad Z \sim \mathcal{N}(0,1)$ I drew, I also drew $-Z$, and thus, only have to draw half the number of increments. By pairing samples, I introduce negative correlation into the sample and reduce the variance.
## Control Variates
I also implemented a control variate based on a strongly correlated random variable with known expectation. Specifically, I used the terminal asset price $S_T$, whose expected value under the risk-neutral measure is known analytically.

The adjusted estimator takes the form

$\hat{V}_{CV} = \hat{V} - \beta(\hat{Y} - \mathbb{E}[Y]),$

where $\beta$ is chosen to minimise variance. The optimal control variate was empirically estimated using sample moments. Empirically, this significantly reduced estimator variance compared to both the naïve and antithetic estimators.
# Experimental Setup
All simulations were performed with the following baseline parameters:
- Initial price $S_0 = 100$
- Strike $K = 100$
- Risk-free rate $r = 0.03$
- Volatility $\sigma  = 0.2$
- Time to maturity $T = 1$
- Number of time steps $n\textunderscore steps = 252$
The Monte Carlo estimates were computed using paths of: $500, 1000, 2000, 5000, 10000, 20000, 50000, 100000$.

# Quantitatve Results
Variance reduction was assessed by comparing the empirical absolute error of each estimator across repeated simulations. Relative to the naïve Monte Carlo simulator:
- Antithetic variates reduced the absolute error by approximately 28%
- Control variates reduced the absolute error by approximately 38%

This translated into substantially faster convergence for a fixed number of paths

# Visual evidence

## Absolute error vs variance reduction methods

|No. of paths|Naïve Monte Carlo|Antithetic|Control|
|---|---|---|---|
|500|0.5267|0.3900|0.3277|
|1000|0.2828|0.2768|0.2135|
|2000|0.2632|0.1598|0.1278|
|5000|0.1615|0.1128|0.0849|
|10000|0.1006|0.0752|0.0582|
|20000|0.0792|0.0454|0.0565|
|50000|0.0520|0.0360|0.0321|
|100000|0.0415|0.0285|0.0263|

## Absolute error vs number of paths

<img width="613" height="473" alt="image" src="https://github.com/user-attachments/assets/caee5f2b-316f-4ae7-9a6d-36596d28862c" />

# Results and limitations
The variance reduction techniques substantially improved convergence speed, allowing accurate pricing with far fewer simulated paths. However, the model relies on strong assumptions — constant volatility, lognormal returns, frictionless markets — which are violated in real financial data.

# Lessons I learnt
This project deepened my understanding of:
- stochastic modelling of asset prices,
- Monte Carlo convergence and variance reduction,
- the relationship between analytical finance models and numerical methods.

It also highlighted the importance of validating simulations against known results, and of understanding model assumptions rather than treating formulas as black boxes.
