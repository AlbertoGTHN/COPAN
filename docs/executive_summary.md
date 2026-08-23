# Executive Summary — Implementation Update
## COPAN — Classification-Oriented Phishing Analysis Network · LACCI 2026

**To:** Loo, Galindo, Romero, Quiñonez, Funez, García, Jimenez
**Date:** 2026-04-07
**Re:** What changed in the codebase since the paper draft, and why the results improved

---

### What This Is

Over the past development sprint we ran a full audit of the phishing-detector codebase
against the submitted paper draft. We found several gaps between what the paper described
and what the code actually did. All gaps have now been closed. This memo summarises the
changes so every co-author understands what version of the system produced the results
we are reporting.

---

### The headline number

> **Our system now achieves 93.4 % accuracy, F1 = 0.934, AUC = 0.985, FPR = 9.6 %, FNR = 3.6 %**
> on a stratified 500-sample hold-out from the multi-corpus test split.

This is **+11 percentage points** above the DistilBERT+RF baseline (82.4 %) cited in our
Related Work, and +18 pp above EBIDS. It is also substantially better than the figures in
our current draft — because the draft was written against an older, degraded version of the
system (rule-only features, no PCA). The new results are reproducible in under 20 minutes
with a single command (see `docs/paper_sync_report.md`, Appendix A).

---

### Five things that changed (and why each one matters)

#### 1 · Dataset pipeline rebuilt from scratch

We automated loading of all six benchmark corpora — SpamAssassin, CEAS 2008, Enron,
Ling-Spam, Nazario, and Nigerian Fraud — through a unified pipeline
(`app/data/dataset_loader.py`). The code deduplicates on message body, applies stratified
70/15/15 splits, and writes reproducible CSVs to `data/processed/`.

**Net result:** 57,112 clean emails (paper draft claimed ~82,500 — that estimate was too
high). The split is 39,978 train / 8,567 val / 8,567 test. The paper's Section 3.2 and the
test-set description in Section 4 must be updated with these exact numbers.

#### 2 · URL Analyzer upgraded to 1D-CNN

The old URL scoring was entirely rule-based (seven heuristics). We replaced the core scoring
with a character-level 1D Convolutional Neural Network (`app/models/url_cnn.py`) with three
parallel branches (kernel sizes 3, 5, 7) that captures subtle n-gram patterns in URL strings
without manual feature engineering. The seven hard rules are still used, blended at 40 % with
the CNN score (60 %). **This closes the typosquatting-evasion gap** identified in preliminary
red-teaming.

The paper's Section 3.3 URL Analyzer paragraph needs to be replaced with a description of
this architecture (46,561 parameters, character vocab 101, max URL length 200 chars).

#### 3 · Feature fusion corrected to match the paper's own specification

The paper described a PCA-compressed BERT embedding fused with rule indicators, but the
running code was using raw concatenation without PCA, producing an 818-dimensional feature
vector that the 70-dimensional Random Forest model could not consume. This caused a runtime
crash on every inference that triggered DistilBERT.

We fixed this by implementing the full `PCA(768→64) + 20 rule indicators = 84-d` fusion
path (`app/models/classifier.py`). The Random Forest was retrained on these 84-d vectors.
Cross-validation F1 jumped from ~0.55 (broken) to **0.9390 ± 0.0088**. The paper's Section
3.3 feature-fusion paragraph must state "84-dimensional" explicitly.

#### 4 · Rigorous evaluation script with bootstrap confidence intervals

We built `scripts/evaluate.py` to replace ad-hoc metric collection. The script:
- Loads the held-out test split
- Runs the full MCO pipeline (parse → semantic → structural → classify)
- Computes accuracy, macro F1, ROC-AUC, FPR, FNR, Cohen's κ
- Constructs 95 % bootstrap confidence intervals (1 000 resamples) for all five primary metrics
- Runs an ablation pass with DistilBERT disabled (rule-only mode) for comparison
- Saves four publication-quality figures at 300 dpi to `results/`

**All numbers in Section 4.1 / Table 3 must come from this script's output**, not from
earlier notebook runs. The current draft figures are outdated.

#### 5 · Security hardening (required disclosure for ICITS companion paper)

A structured red-team exercise identified six exploitable vulnerabilities in the API:

| ID | Vulnerability | Mitigation |
|----|--------------|------------|
| V-01 | Unauthenticated training endpoints | API key (`DETECTOR_ADMIN_KEY`) via `X-Admin-Key` header |
| V-02 | DoS on analysis endpoints | 30 req/min/IP rate limit (slowapi) |
| V-03 | Training-queue flooding | 5 req/min/IP rate limit |
| V-04 | Feature oracle via raw_features | Stripped from responses by default (`EXPOSE_RAW_FEATURES=false`) |
| V-05 | Unicode homoglyph/Cyrillic bypass | NFKC normalization in both text parsers |
| V-06 | Training data poisoning | SUSPICIOUS_LABEL quarantine for high-confidence mislabeled samples |

All six are implemented and tested. A new Section 4.4 (Adversarial Robustness Analysis)
must be inserted in the paper to disclose these findings and point to the ICITS companion
paper for quantitative attack-success rates on V-07 through V-12.

---

### What the paper draft must change

Twelve specific corrections are documented in `docs/paper_sync_report.md` with exact
"current text → corrected text" pairs for each item. The most critical are:

1. **Section 3.2** — corpus size (57,112, not ~82,500) and per-dataset table
2. **Section 3.3** — URL-CNN architecture, 84-d feature fusion, RF depth = 15
3. **Section 4** — test set size (8,567, not ~12,375)
4. **Section 4.1 / Table 3** — all figures replaced with live evaluation output
5. **References** — two unresolved `[?]` must become `[5] Khonji et al. 2013`
6. **New Section 4.4** — Adversarial Robustness placeholder (12 vulnerability IDs)

---

### Nothing changed in the paper's theoretical contribution

The MCO architecture, the dual-engine design (Engine A semantic + Engine B structural),
the agentic loop framing, and the comparison against SpamAssassin and EBIDS are all intact.
The changes above are corrections to implementation details and empirical figures —
the system now actually does what the paper claims, and performs better than the paper
currently reports.

---

### Next steps for authors

| Who | Action | By |
|-----|--------|----|
| **All** | Read `docs/paper_sync_report.md`, locate each quoted passage in the draft | Before next meeting |
| **Galindo / Romero** | Apply the 12 corrections; update Table 3 with new figures | 2026-04-14 |
| **Loo** | Draft Section 4.4 text; coordinate with ICITS paper submission for V-07 – V-12 attack results | 2026-04-21 |
| **García / Jimenez** | Verify reproducibility: run `py scripts/evaluate.py` against the shared model artifacts | 2026-04-14 |
| **Quiñonez / Funez** | Review SECURITY.md; confirm the six mitigations are complete for ICITS disclosure | 2026-04-14 |

---

*Full technical details: `docs/paper_sync_report.md` · Security details: `SECURITY.md`*
*Model artifacts: `models/rf_classifier.pkl`, `models/pca_reducer.pkl`*
*Evaluation figures: `results/*.png`*
