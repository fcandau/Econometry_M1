"""Generate figures for the staggered-DiD lecture (deterministic, simulated data)."""
import os, re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pyfixest as pf

BORDEAUX = (0.68, 0.0, 0.13)
BLUE = "steelblue"
GREEN = "#5b7f6b"
GREY = "#4a4a55"
os.makedirs("fig", exist_ok=True)
rng = np.random.default_rng(7)

# ---------------------------------------------------------------------------
# A simulated staggered panel: three cohorts (early g=4, late g=7, never), T=10
#   effect of cohort g at event time k>=0 :  tau(g,k) = a_g * (1 + k)   (grows with time)
# ---------------------------------------------------------------------------
N, T = 300, 10
units = np.arange(N)
g = np.repeat([4, 7, 99], N // 3)                     # 99 = never treated
a = np.where(g == 4, 1.0, np.where(g == 7, 0.6, 0.0))
fe_i = rng.normal(0, 1, N)
fe_t = np.linspace(0, 2, T)                           # common upward trend
rows = []
for i in units:
    for t in range(1, T + 1):
        k = t - g[i]
        tau = a[i] * (1 + k) if k >= 0 else 0.0
        y = fe_i[i] + fe_t[t - 1] + tau + rng.normal(0, 0.5)
        rows.append((i, t, int(g[i]), k if g[i] != 99 else -99, int(t >= g[i]), y, tau))
df = pd.DataFrame(rows, columns=["id", "t", "g", "k", "d", "y", "tau"])

# ---- Fig 1: the three groups over time -------------------------------------
means = df.groupby(["g", "t"])["y"].mean().unstack(0)
fig, ax = plt.subplots(figsize=(7.4, 3.9))
ax.plot(means.index, means[99], "-o", color=GREY, lw=2, ms=4, label="Never treated")
ax.plot(means.index, means[7], "-s", color=BLUE, lw=2, ms=4, label="Late cohort ($g=7$)")
ax.plot(means.index, means[4], "-^", color=BORDEAUX, lw=2, ms=4, label="Early cohort ($g=4$)")
ax.axvline(3.5, color=BORDEAUX, lw=1, ls="--"); ax.axvline(6.5, color=BLUE, lw=1, ls="--")
ax.axvspan(3.5, 6.5, color=BORDEAUX, alpha=0.06)
ax.text(5, ax.get_ylim()[1] * 0.97, "early treated,\nlate not yet", ha="center", va="top", fontsize=8, color=GREY)
ax.axvspan(6.5, 10.5, color=BLUE, alpha=0.06)
ax.text(8.5, ax.get_ylim()[1] * 0.97, "both treated", ha="center", va="top", fontsize=8, color=GREY)
ax.set_xlabel("Period $t$"); ax.set_ylabel("Mean outcome")
ax.legend(loc="lower right", fontsize=8.5, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("fig/three_groups.png", dpi=150); plt.close(fig)

print("done")
