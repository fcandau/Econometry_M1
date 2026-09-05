# M1 Econometrics — UPPA

Lecture slides (Beamer PDF) and [Quarto](https://quarto.org) source for the first-year
Master (M1) Econometrics course, **F. Candau** (E2S-UPPA / UPPA-TREE).

The course runs in sequence: **OLS → Panel → Instrumental Variables / Shift-Share →
Difference-in-Differences (canonical design, staggered adoption, then doses and on/off
treatments).**

## Lectures

| # | Lecture | Slides | Source |
|---|---------|--------|--------|
| 1 | The Linear Model — OLS, inference, diagnostics | [PDF](Basic/Lecture/basics.pdf) | [.qmd](Basic/Lecture/basics.qmd) |
| 2 | Panel Data | [PDF](Panel/Lecture/panel.pdf) | [.qmd](Panel/Lecture/panel.qmd) |
| 3 | Instrumental Variables & Shift-Share | [PDF](IV_Shift_Share/Lecture/IV_ShiftShare.pdf) | [.qmd](IV_Shift_Share/Lecture/IV_ShiftShare.qmd) |
| 4 | Difference-in-Differences (I) — the canonical design | [PDF](DiD/Lecture/did.pdf) | [.qmd](DiD/Lecture/did.qmd) |
| 5 | Difference-in-Differences (II) — staggered adoption | [PDF](DiD_staggered/Lecture/did_staggered.pdf) | [.qmd](DiD_staggered/Lecture/did_staggered.qmd) |
| 6 | Difference-in-Differences (III) — beyond the switch: doses, on/off treatments | [PDF](DiD_advanced/Lecture/did_advanced.pdf) | [.qmd](DiD_advanced/Lecture/did_advanced.qmd) |

## Reproducing the slides

Each deck is rendered to a Beamer PDF from its `Lecture/` folder:

```bash
quarto render Basic/Lecture/basics.qmd --to beamer
```

## Textbook

Békés & Kézdi (2021), *Data Analysis for Business, Economics, and Policy*, Cambridge
University Press — replication code (R / Python / Stata):
<https://github.com/gabors-data-analysis/da_case_studies>.
