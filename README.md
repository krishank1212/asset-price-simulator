# About the project
This project implements and analyses Monte Carlo pricing of a European call option under the Black–Scholes framework, with the underlying asset modelled as a Geometric Brownian Motion (GBM). The primary aim was not just to obtain an option price, but to study convergence behaviour and variance reduction techniques, and to compare empirical Monte Carlo estimates with the closed-form Black–Scholes solution.

In particular, I investigate how the Monte Carlo estimator converges to the analytical price as the number of simulated paths increases, and how variance reduction techniques improve efficiency for a fixed computational budget.
# How it's made
## Mathematical Model

Under the Black–Scholes assumptions, the asset price S_t follows the stochastic differential equation

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

where $\beta$ is chosen to minimise variance. Empirically, this significantly reduced estimator variance compared to both the naïve and antithetic estimators.
# Results and limitations
The variance reduction techniques substantially improved convergence speed, allowing accurate pricing with far fewer simulated paths. However, the model relies on strong assumptions — constant volatility, lognormal returns, frictionless markets — which are violated in real financial data.

# Lessons I learnt
This project deepened my understanding of:
- stochastic modelling of asset prices,
- Monte Carlo convergence and variance reduction,
- the relationship between analytical finance models and numerical methods.

It also highlighted the importance of validating simulations against known results, and of understanding model assumptions rather than treating formulas as black boxes.
