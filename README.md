# Options Pricer with Greeks Dashboard

This project implements and analyses Monte Carlo pricing of a European call option under the Black–Scholes framework, extended with a full analytical and numerical Greeks module and an interactive Streamlit dashboard.

The primary aim was not to obtain option prices mechanically, but to study convergence behaviour, variance reduction techniques, and the relationship between a closed-form model and its numerical derivatives: understanding the machinery underneath rather than treating formulas as black boxes.

---

# Part I: Monte Carlo Pricing

## Mathematical Model

Under the Black–Scholes assumptions, the asset price $S_t$ follows the stochastic differential equation

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t,$$

where $\mu$ is the drift, $\sigma$ the volatility, and $W_t$ a standard Brownian motion.

Discretising this SDE over small time steps $\Delta t$, the terminal asset price is simulated using

$$S_T = S_0 \exp\!\left(\left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma\sqrt{T}\, Z\right), \quad Z \sim \mathcal{N}(0,1).$$

For each simulated path, the payoff of a European call option is

$$\max(S_T - K,\, 0),$$

and the Monte Carlo price is obtained by discounting the average payoff under the risk-neutral measure. The analytical Black–Scholes price serves as a ground truth for direct comparison.

## Implementation

The project is implemented in Python using:
- `NumPy` for vectorised simulation of paths,
- `SciPy` for evaluating the Black–Scholes formula and normal CDF,
- `Matplotlib` for visualising convergence and error behaviour.

To study convergence, the number of Monte Carlo paths was varied and absolute pricing error plotted against the analytical value, confirming the expected $O(N^{-1/2})$ convergence rate for the naïve estimator.

## Variance Reduction

A key limitation of standard Monte Carlo is high variance. Two classical variance reduction methods were implemented to improve estimator efficiency for a fixed computational budget.

### Antithetic Variates

Antithetic variates exploit the symmetry of the normal distribution. For every draw $Z \sim \mathcal{N}(0,1)$, its negative $-Z$ is also used, halving the number of independent draws required. Pairing samples in this way introduces negative correlation into the estimator, reducing variance without increasing the number of simulated paths.

### Control Variates

A control variate based on the terminal asset price $S_T$ was implemented, exploiting the fact that its risk-neutral expectation is known analytically: $\mathbb{E}[e^{-rT} S_T] = S_0$.

The adjusted estimator takes the form

$$\hat{V}_{\text{CV}} = \hat{V} - \beta \left(\hat{Y} - \mathbb{E}[Y]\right),$$

where $\beta$ is chosen to minimise variance. The optimal $\beta$ is estimated empirically from sample covariance and variance of $X$ and $Y$.

## Experimental Setup

All simulations were run with the following baseline parameters:

| Parameter | Value |
|-----------|-------|
| Initial price $S_0$ | 100 |
| Strike $K$ | 100 |
| Risk-free rate $r$ | 0.03 |
| Volatility $\sigma$ | 0.2 |
| Time to maturity $T$ | 1 year |
| Time steps | 252 |

Path counts tested: 500, 1,000, 2,000, 5,000, 10,000, 20,000, 50,000, 100,000.

## Quantitative Results

| Paths | Naïve MC | Antithetic | Control Variate |
|-------|----------|------------|-----------------|
| 500 | 0.5267 | 0.3900 | 0.3277 |
| 1,000 | 0.2828 | 0.2768 | 0.2135 |
| 2,000 | 0.2632 | 0.1598 | 0.1278 |
| 5,000 | 0.1615 | 0.1128 | 0.0849 |
| 10,000 | 0.1006 | 0.0752 | 0.0582 |
| 20,000 | 0.0792 | 0.0454 | 0.0565 |
| 50,000 | 0.0520 | 0.0360 | 0.0321 |
| 100,000 | 0.0415 | 0.0285 | 0.0263 |

Relative to the naïve estimator:
- **Antithetic variates** reduced absolute error by approximately **28%**
- **Control variates** reduced absolute error by approximately **38%**

Note: at 20,000 paths the control variate marginally underperforms antithetic, likely due to sampling variance in the empirical $\beta$ estimate. The overall convergence trend is clear.

<img width="1226" height="946" alt="image" src="https://github.com/user-attachments/assets/304ce83f-b5cc-410f-a462-fe2f0ac3cc5b" />

---

# Part II: Greeks

## What Are the Greeks?

The Greeks measure the sensitivity of an option's price to changes in its underlying parameters. They are the primary tools used by practitioners to understand and hedge option risk. Each Greek answers a specific question about how the option value $V$ moves as one input changes while the others are held fixed.

## Analytical Definitions

### Delta: $\Delta$

$$\Delta = \frac{\partial V}{\partial S} = N(d_1),$$

where $N(\cdot)$ is the standard normal CDF and

$$d_1 = \frac{\ln(S_0/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}.$$

Delta measures the rate of change of the option price with respect to the spot price. It lies in $[0,1]$ for a European call, approaching 1 deep in-the-money and 0 deep out-of-the-money. It also gives the hedge ratio: a delta-neutral portfolio holds $-\Delta$ units of the underlying per long option.

### Gamma: $\Gamma$

$$\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{N'(d_1)}{S_0 \sigma \sqrt{T}},$$

where $N'(\cdot)$ is the standard normal PDF. Gamma measures the convexity of the option price with respect to spot, or equivalently, the rate of change of delta. It is largest near-the-money and peaks as expiry approaches, capturing the non-linearity that makes delta hedging imperfect over finite rebalancing intervals.

### Vega: $\mathcal{V}$

$$\mathcal{V} = \frac{\partial V}{\partial \sigma} = S_0 \sqrt{T}\, N'(d_1).$$

Vega measures sensitivity to volatility. It is always positive for long options: higher volatility increases the probability of large moves in either direction, which benefits the call holder without increasing the downside beyond the premium paid.

### Theta: $\Theta$

$$\Theta = -\frac{\partial V}{\partial t}.$$

Theta measures time decay: the rate at which the option loses value as time to maturity decreases, all else equal. It is typically negative for long calls: as expiry approaches, there is less time for a favourable move to occur. Near-the-money options exhibit the steepest time decay close to expiry.

### Rho: $\rho$

$$\rho = \frac{\partial V}{\partial r} = KT e^{-rT} N(d_2).$$

Rho measures sensitivity to the risk-free rate. A higher rate reduces the present value of the strike payment, which increases call value. Rho is typically the least significant Greek for short-dated options but becomes more material at long maturities.

## Numerical Implementation

All Greeks except Delta are computed numerically using **central finite differences**:

$$\frac{\partial V}{\partial x} \approx \frac{V(x+h) - V(x-h)}{2h}, \qquad \frac{\partial^2 V}{\partial x^2} \approx \frac{V(x+h) - 2V(x) + V(x-h)}{h^2}.$$

Central differences achieve $O(h^2)$ accuracy compared to $O(h)$ for forward or backward differences, at the cost of two function evaluations per Greek instead of one. Step sizes are chosen to balance truncation error (large $h$) against floating-point cancellation error (small $h$):

| Greek | Differentiated w.r.t. | Step size $h$ |
|-------|----------------------|---------------|
| Delta (numerical) | Spot price $S$ | 0.01 |
| Gamma | Spot price $S$ | 0.01 |
| Vega | Volatility $\sigma$ | 0.001 |
| Theta | Time to maturity $T$ | $1/365$ |
| Rho | Risk-free rate $r$ | 0.001 |

Delta is also computed analytically via the closed-form $N(d_1)$ expression. Agreement between analytical and numerical Delta serves as a consistency check on the finite-difference implementation.

## Dashboard

An interactive Streamlit dashboard (`app.py`) allows real-time exploration of how the option price and Greeks change with each input parameter. Sliders control $S_0$, $K$, $r$, $\sigma$, and $T$; metric cards display the current Greeks; and five plots show each Greek as a continuous function of its natural variable, with a red vertical line marking the current parameter value.

<img width="728" height="782" alt="image" src="https://github.com/user-attachments/assets/8a987c56-c4b1-4fb7-a441-1165abe885ab" />

---

# Results and Limitations

The variance reduction techniques substantially improve Monte Carlo convergence speed. The Greeks module provides fast, accurate sensitivity measures that agree with the analytical values to four decimal places across all tested parameter combinations.

However, the underlying model makes strong assumptions (constant volatility, lognormal returns, frictionless markets, continuous trading) which are violated in practice. In real markets, volatility is itself stochastic (motivating models such as Heston or SABR), and the volatility surface is not flat.

---

# Lessons Learnt

This project deepened my understanding of:
- stochastic modelling of asset prices and SDE discretisation,
- Monte Carlo convergence theory and variance reduction,
- the relationship between closed-form financial models and their numerical derivatives,
- finite-difference methods and the trade-off between accuracy and numerical stability.

It also reinforced the importance of validating simulations against known results, and of understanding model assumptions rather than treating formulas as black boxes.
