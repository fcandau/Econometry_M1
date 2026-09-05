"""Generate figures for the DiD lecture (deterministic)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BORDEAUX = (0.68, 0.0, 0.13)
BLUE = "steelblue"
os.makedirs("fig", exist_ok=True)

# ---- Fig 1: the canonical 2x2 counterfactual ----
x = [0, 1]
ctrl = [4.0, 6.0]          # control: +2 (common time shock)
treat = [6.0, 10.0]        # treated observed: +4
cf = [6.0, 8.0]            # treated counterfactual (parallel to control): +2
fig, ax = plt.subplots(figsize=(7.2, 4.0))
ax.plot(x, treat, "-o", color=BORDEAUX, lw=2.2, label="Treated (observed)")
ax.plot(x, ctrl, "-o", color=BLUE, lw=2.2, label="Control")
ax.plot(x, cf, "--", color=BORDEAUX, lw=1.6,
        label="Treated counterfactual (parallel trend)")
ax.annotate("", xy=(1, 10), xytext=(1, 8),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.4))
ax.text(1.04, 9.0, "ATT", va="center", fontsize=11)
ax.axvline(0.05, color="black", lw=0.6, ls=":")   # just after "Before"
ax.text(0.05, 2.4, "treatment", ha="left", fontsize=8, color="black")
ax.set_xticks([0, 1]); ax.set_xticklabels(["Before", "After"])
ax.set_ylabel("Outcome  $y$"); ax.set_xlim(-0.15, 1.35); ax.set_ylim(2, 12)
ax.legend(loc="upper left", fontsize=8.5)
fig.tight_layout(); fig.savefig("fig/did_canonical.png", dpi=150); plt.close(fig)

# ---- Fig 2: event study ----
rng = np.random.default_rng(2)
k = np.arange(-4, 6)
true = np.where(k < 0, 0.0, 0.45 * (k + 1))      # flat pre, rising post
est = true + rng.normal(0, 0.05, len(k))
se = np.full(len(k), 0.18)
est[k == -1] = 0.0; se[k == -1] = 0.0            # omitted baseline
fig, ax = plt.subplots(figsize=(7.4, 3.6))
ax.errorbar(k, est, yerr=1.96 * se, fmt="o", color=BORDEAUX, capsize=3, lw=1.4)
ax.axhline(0, color="black", lw=0.6)
ax.axvline(-0.5, color="gray", ls="--", lw=1.0)
ax.text(-3.8, 2.0, "pre-trends\n(should be flat)", fontsize=8, color="gray")
ax.text(2.2, 0.4, "dynamic effects", fontsize=8, color=BORDEAUX)
ax.set_xlabel(r"Event time  $k = t - $ treatment date")
ax.set_ylabel(r"$\beta_k$"); ax.set_xticks(k)
fig.tight_layout(); fig.savefig("fig/event_study.png", dpi=150); plt.close(fig)

# ---- Fig 3: forbidden comparison (clean staggered) ----
t = np.arange(1, 11)
eff = 3.0
early = 10 + 0.6 * t + np.where(t >= 4, eff, 0)   # treated at t=4
late = 6 + 0.6 * t + np.where(t >= 8, eff, 0)      # treated at t=8
fig, ax = plt.subplots(figsize=(7.6, 4.1))
ax.axvspan(8, 10.3, color="red", alpha=0.07)
ax.plot(t, early, "-^", color=BORDEAUX, lw=1.9, label="Early cohort (treated $t=4$)")
ax.plot(t, late, "-o", color=BLUE, lw=1.9, label="Late cohort (treated $t=8$)")
ax.axvline(4, color=BORDEAUX, ls=":", lw=1.1)
ax.axvline(8, color=BLUE, ls=":", lw=1.1)
ax.text(9.1, 8.2, "late cohort newly treated,\nbut early cohort is\nALREADY treated",
        fontsize=8, ha="center", color="darkred")
ax.set_xlabel("Time  $t$"); ax.set_ylabel("Outcome  $y$")
ax.set_xticks(t); ax.set_ylim(5, 24)
ax.legend(loc="upper left", fontsize=8.5)
fig.tight_layout(); fig.savefig("fig/forbidden.png", dpi=150); plt.close(fig)

print("figures written to fig/")
