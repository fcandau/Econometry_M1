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

# ---- Fig 4: two violations of the design ----
# (a) Ashenfelter's dip: the treated outcome falls just before the shock, so the
#     pre-period used by the DiD is too low and the DiD overstates the effect.
# (b) Spillover: the shock also moves the control group, in the opposite direction,
#     and the DiD adds the two moves.
from matplotlib.lines import Line2D

T0, SLOPE, END = 5.0, -0.45, 10.3
def line(a, t):
    return a + SLOPE * np.asarray(t)

def arrow(ax, x, y0, y1, color, text, xtext=10.6):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.4))
    ax.text(xtext, (y0 + y1) / 2, text, color=color, fontsize=10, ha="left", va="center")

fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0))
for ax in axes:
    ax.axvline(T0, color="gray", lw=0.8, ls=":")
    ax.text(T0 + 0.15, 0.25, "shock", ha="left", va="bottom", fontsize=9, color="gray")
    ax.set_xlim(0, 13.6); ax.set_ylim(0, 10.5)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("time"); ax.set_ylabel("outcome")
    ax.spines[["top", "right"]].set_visible(False)

post = [T0, END]

# (a) Ashenfelter's dip
ax, A, DIP, EFF, T_DIP = axes[0], 6.6, -1.4, 0.9, 3.6
ax.plot([0, END], line(9.4, [0, END]), color=BLUE, lw=2.2)
ax.plot([0, T_DIP], line(A, [0, T_DIP]), color=BORDEAUX, lw=2.2)
ax.plot([T_DIP, T_DIP], [line(A, T_DIP), line(A + DIP, T_DIP)], color=BORDEAUX, lw=1.0)
ax.plot([T_DIP, T0], line(A + DIP, [T_DIP, T0]), color=BORDEAUX, lw=2.2)
ax.plot(post, line(A + EFF, post), color=BORDEAUX, lw=2.2)
ax.plot(post, line(A, post), color=BORDEAUX, lw=1.1, ls=":")
ax.plot(post, line(A + DIP, post), color=BORDEAUX, lw=1.1, ls="--")
ax.text(4.3, line(A + DIP, 4.3) - 0.45, "dip", color=BORDEAUX, fontsize=10, ha="center")
arrow(ax, 9.5, line(A, 9.5), line(A + EFF, 9.5), "black", "true effect")
arrow(ax, 10.1, line(A + DIP, 10.1), line(A + EFF, 10.1), BORDEAUX, "DiD estimate",
      xtext=10.6)
ax.set_title("(a) Ashenfelter's dip", fontsize=12)
ax.legend(handles=[Line2D([], [], color=BLUE, lw=2.2, label="Control"),
                   Line2D([], [], color=BORDEAUX, lw=2.2, label="Treated"),
                   Line2D([], [], color=BORDEAUX, lw=1.1, ls=":", label="Treated without the shock"),
                   Line2D([], [], color=BORDEAUX, lw=1.1, ls="--", label="Trend assumed from the dip")],
          loc="upper right", fontsize=8.5, frameon=False)

# (b) Spillover on the control group
ax, AT, AC, EFF_T, EFF_C = axes[1], 8.8, 6.4, 1.6, -1.1
ax.plot([0, T0], line(AT, [0, T0]), color=BORDEAUX, lw=2.2)
ax.plot([0, T0], line(AC, [0, T0]), color=BLUE, lw=2.2)
ax.plot(post, line(AT + EFF_T, post), color=BORDEAUX, lw=2.2)
ax.plot(post, line(AC + EFF_C, post), color=BLUE, lw=2.2)
ax.plot(post, line(AT, post), color=BORDEAUX, lw=1.1, ls=":")
ax.plot(post, line(AC, post), color=BLUE, lw=1.1, ls=":")
arrow(ax, 10.1, line(AT, 10.1), line(AT + EFF_T, 10.1), BORDEAUX, "effect on\nthe treated")
arrow(ax, 10.1, line(AC, 10.1), line(AC + EFF_C, 10.1), BLUE, "spillover on\nthe control")
ax.set_title("(b) Spillover on the control group", fontsize=12)
ax.legend(handles=[Line2D([], [], color=BORDEAUX, lw=2.2, label="Treated"),
                   Line2D([], [], color=BLUE, lw=2.2, label="Control"),
                   Line2D([], [], color="gray", lw=1.1, ls=":", label="Without the shock")],
          loc="upper right", fontsize=8.5, frameon=False)

fig.tight_layout(); fig.savefig("fig/violations.png", dpi=170); plt.close(fig)

# ---- Fig 5: sensitivity analysis in the spirit of Rambachan and Roth (2023) ----
# Illustrative numbers. (a) An event study whose pre-period fails the pre-trend test: the
# gap between the groups falls steadily before the policy, by at most 0.8 per year. The
# grey band is where the gap could go after the policy if it kept changing by up to 0.8
# per year (Mbar = 1). (b) The plot HonestDiD draws: the original interval, then the
# robust interval of the year-0 effect for each Mbar.
k_pre, b_pre = np.array([-5, -4, -3, -2, -1]), np.array([3.0, 2.3, 1.5, 0.7, 0.0])
k_post, b_post = np.array([0, 1, 2]), np.array([-10.0, -10.0, -9.0])
se_pre, se_post, MAXD = 0.75, 1.95, 0.8

fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.8), gridspec_kw={"width_ratios": [1.25, 1]})
ax = axes[0]
kk = np.array([-1, 0, 1, 2])
ax.fill_between(kk, -MAXD * (kk + 1), MAXD * (kk + 1), color="gray", alpha=0.25, lw=0,
                label="Change allowed after the policy ($\\bar M = 1$)")
ax.errorbar(k_pre[:-1], b_pre[:-1], yerr=1.96 * se_pre, fmt="o", color=BLUE, capsize=3,
            lw=1.3, label="Before the policy")
ax.plot([-1], [0], "o", color=BLUE)
ax.errorbar(k_post, b_post, yerr=1.96 * se_post, fmt="o", color=BORDEAUX, capsize=3,
            lw=1.3, label="After the policy")
ax.axhline(0, color="black", lw=0.6)
ax.axvline(-0.5, color="gray", ls="--", lw=0.9)
ax.set_xticks(list(k_pre) + list(k_post))
ax.set_xlabel("years relative to the policy"); ax.set_ylabel("estimated effect")
ax.set_ylim(-15.5, 7.5)
ax.set_title("(a) Event study: the pre-trend test fails", fontsize=11)
ax.legend(loc="lower left", fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)

ax = axes[1]
# Same layout as the plot HonestDiD draws: the original interval first, then the robust
# interval for each value of Mbar.
labels = ["Original", "1", "2", "3", "4", "5", "6", "7", "8"]
mbar = [np.nan, 1, 2, 3, 4, 5, 6, 7, 8]
pos = np.arange(len(labels))
for x, m in zip(pos, mbar):
    h = 1.96 * se_post + (0 if np.isnan(m) else MAXD * m)
    lo, hi = b_post[0] - h, b_post[0] + h
    col = BORDEAUX if np.isnan(m) else BLUE
    ax.plot([x, x], [lo, hi], color=col, lw=2.4)
    ax.plot([x - 0.14, x + 0.14], [lo, lo], color=col, lw=1.2)
    ax.plot([x - 0.14, x + 0.14], [hi, hi], color=col, lw=1.2)
ax.axhline(0, color="black", lw=0.6)
ax.annotate("zero enters the interval\n(breakdown value $\\approx 8$)", xy=(8, 0.4),
            xytext=(2.6, 4.5), fontsize=8.5, color="gray",
            arrowprops=dict(arrowstyle="->", color="gray", lw=0.9))
ax.set_xticks(pos); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_xlabel("$\\bar M$")
ax.set_ylabel("95 % interval, effect in year 0")
ax.set_ylim(-22, 8)
ax.set_title("(b) Sensitivity plot (HonestDiD)", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout(); fig.savefig("fig/sensitivity.png", dpi=170); plt.close(fig)

print("figures written to fig/")
