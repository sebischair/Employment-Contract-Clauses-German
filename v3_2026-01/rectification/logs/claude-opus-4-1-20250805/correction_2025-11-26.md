**Benchmark Summary**
* **Total Clauses:** 886
* **Truly Void:** 130
* **Truly Valid:** 756

---
**1. Classification Metrics (The "Funnel")**

| Metric | Score |
| :--- | :--- |
| Accuracy | 72.23% |
| Precision | 34.32% |
| Recall | 97.69% |
| F1-Score | 0.51 |

| | **Predicted: Void** | **Predicted: Valid** |
| :--- | :--- | :--- |
| **Actual: Void** | 127 (TP) | 3 (FN) |
| **Actual: Valid** | 243 (FP) | 513 (TN) |

---
**2. Linguistic Quality of Corrections**
*(n = 370 attempted corrections)*

| Linguistic Metric | Avg. Delta |
| :--- | :--- |
| Readability (Flesch-Kincaid Grade) | +0.58 grades |
| Verbosity (Word Count) | +8.64 words |

---
**3. Overall Correction Quality (All Clauses)**
*(n = 886 clauses)*

| Metric | Total | Avg. per Clause |
| :--- | :--- | :--- |
| **Total Problems Missed** | 16 | 0.02 |
| **Total Unnecessary Changes** | 689 | 0.78 |

---
**4. Correction Quality Analysis: True Positives (TPs)**
*(n = 127 clauses)*

| Correction Quality | Count | % of TPs |
| :--- | :--- | :--- |
| **Perfect** (Fixed all, 0 junk) | 47 | 37.01%
| **Good, but Sloppy** (Fixed all, >0 junk) | 69 | 54.33%
| **Partial, but Clean** (Missed some, 0 junk) | 4 | 3.15%
| **Partial & Sloppy** (Missed some, >0 junk) | 7 | 5.51%

| TP Error Averages | Total | Avg. per TP |
| :--- | :--- | :--- |
| Missed Problems | 12 | 0.09 |
| Unnecessary Changes | 121 | 0.95 |

---
**5. Correction Quality Analysis: False Positives (FPs)**
*(n = 243 clauses)*

| FP Error Averages | Total | Avg. per FP |
| :--- | :--- | :--- |
| Missed Problems | 0 | 0.00 |
| Unnecessary Changes | 568 | 2.34 |

---
**6. Correction Quality Analysis: False Negatives (FNs)**
*(n = 3 clauses)*

| FN Error Averages | Total | Avg. per FN |
| :--- | :--- | :--- |
| Missed Problems | 4 | 1.33 |
| Unnecessary Changes | 0 | 0.00 |

---
**7. Rule-Specific Performance**

| Rule ID | Title | Total Violations | Hits | Misses | Hallucinations | Rule Recall | Rule Precision | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 678bd561d87a6f8049fddf73 | Einarbeitungsstunden Schaden | 2 | 2 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678bd828d87a6f8049fddf7a | Pausenregelung | 1 | 1 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678a62a4780e9d4cb9184c42 | Verschwiegenheit Gehalt | 7 | 7 | 0 | 1 | 100.00% | 87.50% | 93.33% |
| 678a6002780e9d4cb9184c05 | Abwesenheitsgrund | 11 | 11 | 0 | 3 | 100.00% | 78.57% | 88.00% |
| 678a6392780e9d4cb9184c5e | Mindestlohn | 7 | 6 | 1 | 1 | 85.71% | 85.71% | 85.71% |
| 678a625a780e9d4cb9184c3b | Ausschlussfrist Limitierungen | 20 | 19 | 1 | 6 | 95.00% | 76.00% | 84.44% |
| 678a5d77780e9d4cb9184b91 | Generelles Pfändungsverbot | 12 | 11 | 1 | 4 | 91.67% | 73.33% | 81.48% |
| 678a5dfc780e9d4cb9184bfe | Kostenpauschale | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 678a63c2780e9d4cb9184c65 | Vergütung Schulungen | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 67942f34d87a6f8049fde684 | Mindesturlaub | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 678a6376780e9d4cb9184c57 | Abgeltung Überstunden Transparenz | 25 | 23 | 2 | 11 | 92.00% | 67.65% | 77.97% |
| 678a618c780e9d4cb9184c21 | Zweistufige Ausschlussfristen | 11 | 10 | 1 | 9 | 90.91% | 52.63% | 66.67% |
| 678a6320780e9d4cb9184c50 | Abgegoltene Überstunden | 2 | 1 | 1 | 0 | 50.00% | 100.00% | 66.67% |
| 678bcbc7d87a6f8049fddf57 | Vertragsänderung Form | 13 | 13 | 0 | 14 | 100.00% | 48.15% | 65.00% |
| 678bcb3dd87a6f8049fddf50 | Kündigungsfrist Probezeit | 6 | 6 | 0 | 8 | 100.00% | 42.86% | 60.00% |
| 678a620e780e9d4cb9184c34 | Anspruchgeltendmachung Form | 16 | 16 | 0 | 23 | 100.00% | 41.03% | 58.18% |
| 678a6054780e9d4cb9184c0c | Nebenbeschäftigung Einschränkung | 9 | 9 | 0 | 25 | 100.00% | 26.47% | 41.86% |
| 691334564d8b5fd53971f1f5 | Kündigungsfrist nach Probezeit | 2 | 2 | 0 | 8 | 100.00% | 20.00% | 33.33% |
| 691335a84d8b5fd53971f234 | Vertragsstrafe in Probezeit | 4 | 4 | 0 | 18 | 100.00% | 18.18% | 30.77% |
| 678a62d7780e9d4cb9184c49 | Verschwiegenheit Kenntnisse | 6 | 6 | 0 | 27 | 100.00% | 18.18% | 30.77% |
| 691335754d8b5fd53971f22d | Postzugang 4-Tages-Fiktion | 1 | 1 | 0 | 5 | 100.00% | 16.67% | 28.57% |
| 691334b64d8b5fd53971f21f | Günstigkeitsprinzip | 1 | 1 | 0 | 7 | 100.00% | 12.50% | 22.22% |
| 6794200fd87a6f8049fde668 | Kündigungsfrist Arbeitgeber | 1 | 1 | 0 | 7 | 100.00% | 12.50% | 22.22% |
| 691334ea4d8b5fd53971f226 | Urlaub Übertragbarkeit | 1 | 1 | 0 | 19 | 100.00% | 5.00% | 9.52% |
| 678a6447780e9d4cb9184c73 | Wettbewerbsverbot Karenzentschädigung | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |
| 678bcc5ad87a6f8049fddf65 | Kündigungsfrist Max. Dauer | 0 | 0 | 0 | 17 | 0.00% | 0.00% | 0.00% |
| 678a63eb780e9d4cb9184c6c | Wettbewerbsverbot Minderheitsbeteilig... | 0 | 0 | 0 | 5 | 0.00% | 0.00% | 0.00% |
| 691335cf4d8b5fd53971f23b | Transparenzgebot | 1 | 0 | 1 | 112 | 0.00% | 0.00% | 0.00% |
| 678a607e780e9d4cb9184c13 | Einseitige Ausschlussfrist | 0 | 0 | 0 | 6 | 0.00% | 0.00% | 0.00% |