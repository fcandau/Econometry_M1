# M1 Econometrics — UPPA

Lecture slides (Beamer PDF) and [Quarto](https://quarto.org) source for the first-year
Master (M1) Econometrics course, **F. Candau** (E2S-UPPA / UPPA-TREE).

The course runs in sequence: **OLS → Time Series → Panel → Instrumental Variables /
Shift-Share.**

## Lectures

| # | Lecture | Slides | Source |
|---|---------|--------|--------|
| 1 | The Linear Model — OLS, inference, diagnostics | [PDF](Basic/Lecture/basics.pdf) | [.qmd](Basic/Lecture/basics.qmd) |
| 2 | Time Series — persistence, trends, spurious regression | [PDF](time_series/Lecture/timeseries.pdf) | [.qmd](time_series/Lecture/timeseries.qmd) |
| 3 | Panel Data | [PDF](Panel/Lecture/panel.pdf) | [.qmd](Panel/Lecture/panel.qmd) |
| 4 | Instrumental Variables & Shift-Share | [PDF](IV_Shift_Share/Lecture/IV_ShiftShare.pdf) | [.qmd](IV_Shift_Share/Lecture/IV_ShiftShare.qmd) |

## Reproducing the slides

Each deck is rendered to a Beamer PDF from its `Lecture/` folder:

```bash
quarto render Basic/Lecture/basics.qmd --to beamer
```

## Textbook

Békés & Kézdi (2021), *Data Analysis for Business, Economics, and Policy*, Cambridge
University Press — replication code (R / Python / Stata):
<https://github.com/gabors-data-analysis/da_case_studies>.
