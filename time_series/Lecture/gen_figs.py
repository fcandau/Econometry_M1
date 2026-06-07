"""Generate the three figures for the time-series lecture (deterministic)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BORDEAUX = (0.68, 0.0, 0.13)
BLUE = "steelblue"
os.makedirs("fig", exist_ok=True)
T = 200
t = np.arange(T)


def ols(y, x):
    X = np.column_stack([np.ones(len(x)), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    sigma2 = ss_res / (len(y) - 2)
    var_b1 = sigma2 * np.linalg.inv(X.T @ X)[1, 1]
    tstat = b[1] / np.sqrt(var_b1)
    return b, r2, tstat


# ---- Fig 1: persistence (white noise vs AR(1)) ----
rng = np.random.default_rng(7)
eps = rng.standard_normal(T)
wn = eps.copy()
ar = np.zeros(T)
for i in range(1, T):
    ar[i] = 0.85 * ar[i - 1] + eps[i]
fig, ax = plt.subplots(1, 2, figsize=(8.2, 2.9))
ax[0].plot(t, wn, color="gray", lw=1.0)
ax[0].set_title(r"White noise ($\rho=0$): no memory")
ax[1].plot(t, ar, color=BORDEAUX, lw=1.3)
ax[1].set_title(r"AR(1), $\rho=0.85$: long swings")
for a in ax:
    a.axhline(0, color="black", lw=0.5)
    a.set_xlabel("t")
fig.tight_layout()
fig.savefig("fig/persistence.png", dpi=150)
plt.close(fig)

# ---- Fig 2: random walks ----
rng = np.random.default_rng(3)
fig, a = plt.subplots(figsize=(7.2, 3.0))
for _ in range(5):
    rw = np.cumsum(rng.standard_normal(T))
    a.plot(t, rw, lw=1.2)
a.axhline(0, color="black", lw=0.5)
a.set_title(r"Five random walks $y_t=y_{t-1}+\varepsilon_t$: each wanders off")
a.set_xlabel("t")
fig.tight_layout()
fig.savefig("fig/randomwalk.png", dpi=150)
plt.close(fig)

# ---- Fig 3: spurious regression (search a striking independent draw) ----
chosen = None
for seed in range(1000):
    g = np.random.default_rng(seed)
    y = np.cumsum(g.standard_normal(T))
    x = np.cumsum(g.standard_normal(T))  # independent of y
    b, r2, tstat = ols(y, x)
    if r2 > 0.85 and abs(tstat) > 18:
        chosen = (seed, y, x, b, r2, tstat)
        break
seed, y, x, b, r2, tstat = chosen
fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.2))
ax[0].plot(t, y, color=BORDEAUX, lw=1.3, label="y")
ax[0].plot(t, x, color=BLUE, lw=1.3, label="x")
ax[0].set_title("Two INDEPENDENT random walks")
ax[0].set_xlabel("t")
ax[0].legend(fontsize=8, loc="best")
ax[1].scatter(x, y, s=10, color="gray")
xs = np.array([x.min(), x.max()])
ax[1].plot(xs, b[0] + b[1] * xs, color=BORDEAUX, lw=2)
ax[1].set_title(rf"OLS of $y$ on $x$:  $R^2={r2:.2f}$,  $t={tstat:.0f}$")
ax[1].set_xlabel("x")
ax[1].set_ylabel("y")
fig.tight_layout()
fig.savefig("fig/spurious.png", dpi=150)
plt.close(fig)
print(f"spurious seed={seed}  R2={r2:.3f}  t={tstat:.2f}")
