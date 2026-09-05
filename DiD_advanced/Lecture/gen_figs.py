"""Figures for the 'DiD beyond the switch' lecture (deterministic, simulated data)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BORDEAUX = (0.68, 0.0, 0.13)
BLUE = "steelblue"
GREEN = "#5b7f6b"
GREY = "#4a4a55"
os.makedirs("fig", exist_ok=True)
rng = np.random.default_rng(3)

# ---------------------------------------------------------------------------
# Fig 1 — Dose: the ATT(d|d) curve and the two causal responses
#   Units self-select into doses: those with the steepest response choose the highest dose.
#   ATE(d) (population response, dashed) is concave; ATT(d|d) (solid) rises faster because
#   high-dose units have high responses. The slope of ATT(d|d) mixes the causal response and
#   selection.
# ---------------------------------------------------------------------------
d = np.linspace(0, 1, 200)
ate = 1.6 * np.sqrt(d)                       # population dose-response, concave
sel = 1.0 * d ** 2                           # selection term: high-dose units respond more
att = ate + sel
fig, ax = plt.subplots(figsize=(7.2, 3.7))
ax.plot(d, att, color=BORDEAUX, lw=2.2, label=r"$\mathrm{ATT}(d\mid d)$: effect of dose $d$ on units that chose $d$")
ax.plot(d, ate, color=BLUE, lw=2, ls="--", label=r"$\mathrm{ATE}(d)$: effect of dose $d$ on a random unit")
d0 = 0.6
ax.plot([d0], [1.6 * np.sqrt(d0) + d0 ** 2], "o", color=BORDEAUX, ms=5)
h = 0.25
s_att = (1.6 * np.sqrt(d0 + h) + (d0 + h) ** 2 - (1.6 * np.sqrt(d0) + d0 ** 2)) / h
s_ate = (1.6 * np.sqrt(d0 + h) - 1.6 * np.sqrt(d0)) / h
ax.plot([d0, d0 + h], [1.6 * np.sqrt(d0) + d0 ** 2, 1.6 * np.sqrt(d0) + d0 ** 2 + s_att * h], color=BORDEAUX, lw=1, ls=":")
ax.plot([d0, d0 + h], [1.6 * np.sqrt(d0) + d0 ** 2, 1.6 * np.sqrt(d0) + d0 ** 2 + s_ate * h], color=BLUE, lw=1, ls=":")
ax.annotate("slope of the ATT curve:\ncausal response + selection", xy=(d0 + h, 1.6 * np.sqrt(d0) + d0 ** 2 + s_att * h),
            xytext=(0.30, 2.45), fontsize=8, color=BORDEAUX, arrowprops=dict(arrowstyle="->", color=BORDEAUX, lw=0.8))
ax.annotate("causal response (ACR)\nat $d=0.6$", xy=(d0 + h, 1.6 * np.sqrt(d0) + d0 ** 2 + s_ate * h),
            xytext=(0.62, 0.45), fontsize=8, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
ax.set_xlabel("Dose $d$ (0 = untreated)"); ax.set_ylabel("Effect on the outcome")
ax.set_ylim(0, 3.1); ax.legend(loc="lower right", fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("fig/dose_response.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------------------
# Fig 2 — On and off: treatment paths (top) and outcomes with and without carryover (bottom)
#   A ban in force in periods 5-6, lifted in 7-8, reinstated in 9-10, for the treated group.
# ---------------------------------------------------------------------------
T = 10
t = np.arange(1, T + 1)
path = np.array([0, 0, 0, 0, 1, 1, 0, 0, 1, 1])
never = np.zeros(T)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 4.3), sharex=True, gridspec_kw=dict(height_ratios=[1, 2.2]))
a1.step(t, path, where="mid", color=BORDEAUX, lw=2, label="treated group")
a1.step(t, never, where="mid", color=GREY, lw=2, label="never treated")
a1.set_yticks([0, 1]); a1.set_ylabel("$d_{it}$"); a1.set_ylim(-0.15, 1.3)
a1.legend(loc="upper left", fontsize=8, frameon=False, ncol=2)
a1.spines[["top", "right"]].set_visible(False)
base = 0.1 * t                                  # common trend
y_never = base
y_nocarry = base - 0.8 * path                   # effect lasts one period only
carry = np.zeros(T)
for i in range(T):
    carry[i] = -0.8 * path[i] + (0.6 * carry[i - 1] if i > 0 else 0)   # effect persists, decays
y_carry = base + carry
a2.plot(t, y_never, "-o", color=GREY, lw=2, ms=4, label="never treated")
a2.plot(t, y_nocarry, "-s", color=BORDEAUX, lw=2, ms=4, label="treated, no carryover")
a2.plot(t, y_carry, "-^", color=BLUE, lw=2, ms=4, label="treated, carryover")
for lo, hi in [(4.5, 6.5), (8.5, 10.5)]:
    a1.axvspan(lo, hi, color=BORDEAUX, alpha=0.07); a2.axvspan(lo, hi, color=BORDEAUX, alpha=0.07)
a2.text(5.5, 1.15, "on", ha="center", fontsize=8, color=GREY); a2.text(7.5, 1.15, "off", ha="center", fontsize=8, color=GREY)
a2.text(9.5, 1.15, "on", ha="center", fontsize=8, color=GREY)
a2.set_xlabel("Period $t$"); a2.set_ylabel("Outcome"); a2.set_xticks(t)
a2.legend(loc="lower left", fontsize=8, frameon=False)
a2.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("fig/on_off.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------------------
# Fig 3 — Triple differences: four cells. The treated state has its own trend (DiD across states
#   fails); the eligible partition has its own trend everywhere (DiD within state fails); the
#   difference of the two DiDs isolates the effect.
# ---------------------------------------------------------------------------
t = np.arange(2010, 2020)
post = (t >= 2015).astype(float)
common = 0.2 * (t - 2010)
state_trend = 0.25 * (t - 2010)               # treated state grows faster (all residents)
elig_trend = 0.12 * (t - 2010)                # eligible partition grows faster (all states)
effect = -1.4 * post
cells = {
    "treated state, eligible":   10 + common + state_trend + elig_trend + effect,
    "treated state, ineligible": 9 + common + state_trend,
    "control state, eligible":   8.5 + common + elig_trend,
    "control state, ineligible": 7.5 + common,
}
styles = {"treated state, eligible": (BORDEAUX, "-", "o"), "treated state, ineligible": (BORDEAUX, "--", "s"),
          "control state, eligible": (GREY, "-", "o"), "control state, ineligible": (GREY, "--", "s")}
fig, ax = plt.subplots(figsize=(7.2, 3.7))
for k, y in cells.items():
    c, ls, m = styles[k]
    ax.plot(t, y, ls=ls, marker=m, color=c, lw=1.8, ms=3.5, label=k)
ax.axvline(2014.5, color=GREY, lw=1, ls=":")
ax.set_xlabel("Year"); ax.set_ylabel("Outcome")
ax.legend(loc="upper left", fontsize=8, frameon=False, ncol=2)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("fig/ddd.png", dpi=150); plt.close(fig)
print("done")
