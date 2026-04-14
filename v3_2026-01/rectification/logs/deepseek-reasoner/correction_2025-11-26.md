**Benchmark Summary**
* **Total Clauses:** 886
* **Truly Void:** 130
* **Truly Valid:** 756

---
**1. Classification Metrics (The "Funnel")**

| Metric | Score |
| :--- | :--- |
| Accuracy | 74.72% |
| Precision | 36.09% |
| Recall | 93.85% |
| F1-Score | 0.52 |

| | **Predicted: Void** | **Predicted: Valid** |
| :--- | :--- | :--- |
| **Actual: Void** | 122 (TP) | 8 (FN) |
| **Actual: Valid** | 216 (FP) | 540 (TN) |

---
**2. Linguistic Quality of Corrections**
*(n = 338 attempted corrections)*

| Linguistic Metric | Avg. Delta |
| :--- | :--- |
| Readability (Flesch-Kincaid Grade) | +0.02 grades |
| Verbosity (Word Count) | +6.75 words |

---
**3. Overall Correction Quality (All Clauses)**
*(n = 886 clauses)*

| Metric | Total | Avg. per Clause |
| :--- | :--- | :--- |
| **Total Problems Missed** | 23 | 0.03 |
| **Total Unnecessary Changes** | 527 | 0.59 |

---
**4. Correction Quality Analysis: True Positives (TPs)**
*(n = 122 clauses)*

| Correction Quality | Count | % of TPs |
| :--- | :--- | :--- |
| **Perfect** (Fixed all, 0 junk) | 51 | 41.80%
| **Good, but Sloppy** (Fixed all, >0 junk) | 58 | 47.54%
| **Partial, but Clean** (Missed some, 0 junk) | 4 | 3.28%
| **Partial & Sloppy** (Missed some, >0 junk) | 9 | 7.38%

| TP Error Averages | Total | Avg. per TP |
| :--- | :--- | :--- |
| Missed Problems | 14 | 0.11 |
| Unnecessary Changes | 102 | 0.84 |

---
**5. Correction Quality Analysis: False Positives (FPs)**
*(n = 216 clauses)*

| FP Error Averages | Total | Avg. per FP |
| :--- | :--- | :--- |
| Missed Problems | 0 | 0.00 |
| Unnecessary Changes | 425 | 1.97 |

---
**6. Correction Quality Analysis: False Negatives (FNs)**
*(n = 8 clauses)*

| FN Error Averages | Total | Avg. per FN |
| :--- | :--- | :--- |
| Missed Problems | 9 | 1.12 |
| Unnecessary Changes | 0 | 0.00 |

---
**7. Rule-Specific Performance**

| Rule ID | Title | Total Violations | Hits | Misses | Hallucinations | Rule Recall | Rule Precision | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 678bd828d87a6f8049fddf7a | Pausenregelung | 1 | 1 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678a5d77780e9d4cb9184b91 | Generelles Pfändungsverbot | 12 | 12 | 0 | 1 | 100.00% | 92.31% | 96.00% |
| 678a6002780e9d4cb9184c05 | Abwesenheitsgrund | 11 | 11 | 0 | 3 | 100.00% | 78.57% | 88.00% |
| 678a62a4780e9d4cb9184c42 | Verschwiegenheit Gehalt | 7 | 7 | 0 | 2 | 100.00% | 77.78% | 87.50% |
| 678a5dfc780e9d4cb9184bfe | Kostenpauschale | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 678a63c2780e9d4cb9184c65 | Vergütung Schulungen | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 678a625a780e9d4cb9184c3b | Ausschlussfrist Limitierungen | 20 | 16 | 4 | 5 | 80.00% | 76.19% | 78.05% |
| 678a6376780e9d4cb9184c57 | Abgeltung Überstunden Transparenz | 25 | 24 | 1 | 15 | 96.00% | 61.54% | 75.00% |
| 678a620e780e9d4cb9184c34 | Anspruchgeltendmachung Form | 16 | 15 | 1 | 10 | 93.75% | 60.00% | 73.17% |
| 678bcbc7d87a6f8049fddf57 | Vertragsänderung Form | 13 | 13 | 0 | 13 | 100.00% | 50.00% | 66.67% |
| 67942f34d87a6f8049fde684 | Mindesturlaub | 2 | 2 | 0 | 2 | 100.00% | 50.00% | 66.67% |
| 678bd561d87a6f8049fddf73 | Einarbeitungsstunden Schaden | 2 | 2 | 0 | 2 | 100.00% | 50.00% | 66.67% |
| 678bcb3dd87a6f8049fddf50 | Kündigungsfrist Probezeit | 6 | 5 | 1 | 5 | 83.33% | 50.00% | 62.50% |
| 678a618c780e9d4cb9184c21 | Zweistufige Ausschlussfristen | 11 | 10 | 1 | 18 | 90.91% | 35.71% | 51.28% |
| 691334b64d8b5fd53971f21f | Günstigkeitsprinzip | 1 | 1 | 0 | 2 | 100.00% | 33.33% | 50.00% |
| 678a6392780e9d4cb9184c5e | Mindestlohn | 7 | 3 | 4 | 3 | 42.86% | 50.00% | 46.15% |
| 678a6054780e9d4cb9184c0c | Nebenbeschäftigung Einschränkung | 9 | 9 | 0 | 23 | 100.00% | 28.12% | 43.90% |
| 691335a84d8b5fd53971f234 | Vertragsstrafe in Probezeit | 4 | 3 | 1 | 10 | 75.00% | 23.08% | 35.29% |
| 678a6320780e9d4cb9184c50 | Abgegoltene Überstunden | 2 | 1 | 1 | 3 | 50.00% | 25.00% | 33.33% |
| 678a62d7780e9d4cb9184c49 | Verschwiegenheit Kenntnisse | 6 | 5 | 1 | 29 | 83.33% | 14.71% | 25.00% |
| 6794200fd87a6f8049fde668 | Kündigungsfrist Arbeitgeber | 1 | 1 | 0 | 8 | 100.00% | 11.11% | 20.00% |
| 691335754d8b5fd53971f22d | Postzugang 4-Tages-Fiktion | 1 | 1 | 0 | 10 | 100.00% | 9.09% | 16.67% |
| 691334ea4d8b5fd53971f226 | Urlaub Übertragbarkeit | 1 | 1 | 0 | 18 | 100.00% | 5.26% | 10.00% |
| 678bcc5ad87a6f8049fddf65 | Kündigungsfrist Max. Dauer | 0 | 0 | 0 | 2 | 0.00% | 0.00% | 0.00% |
| 678a63eb780e9d4cb9184c6c | Wettbewerbsverbot Minderheitsbeteilig... | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |
| 678a6447780e9d4cb9184c73 | Wettbewerbsverbot Karenzentschädigung | 0 | 0 | 0 | 2 | 0.00% | 0.00% | 0.00% |
| 691335cf4d8b5fd53971f23b | Transparenzgebot | 1 | 0 | 1 | 62 | 0.00% | 0.00% | 0.00% |
| 691334564d8b5fd53971f1f5 | Kündigungsfrist nach Probezeit | 2 | 0 | 2 | 5 | 0.00% | 0.00% | 0.00% |
| 678a607e780e9d4cb9184c13 | Einseitige Ausschlussfrist | 0 | 0 | 0 | 6 | 0.00% | 0.00% | 0.00% |