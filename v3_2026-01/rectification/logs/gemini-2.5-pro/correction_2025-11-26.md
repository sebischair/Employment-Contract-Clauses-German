**Benchmark Summary**
* **Total Clauses:** 886
* **Truly Void:** 130
* **Truly Valid:** 756

---
**1. Classification Metrics (The "Funnel")**

| Metric | Score |
| :--- | :--- |
| Accuracy | 73.14% |
| Precision | 34.92% |
| Recall | 96.15% |
| F1-Score | 0.51 |

| | **Predicted: Void** | **Predicted: Valid** |
| :--- | :--- | :--- |
| **Actual: Void** | 125 (TP) | 5 (FN) |
| **Actual: Valid** | 233 (FP) | 523 (TN) |

---
**2. Linguistic Quality of Corrections**
*(n = 358 attempted corrections)*

| Linguistic Metric | Avg. Delta |
| :--- | :--- |
| Readability (Flesch-Kincaid Grade) | +0.37 grades |
| Verbosity (Word Count) | +11.79 words |

---
**3. Overall Correction Quality (All Clauses)**
*(n = 886 clauses)*

| Metric | Total | Avg. per Clause |
| :--- | :--- | :--- |
| **Total Problems Missed** | 17 | 0.02 |
| **Total Unnecessary Changes** | 779 | 0.88 |

---
**4. Correction Quality Analysis: True Positives (TPs)**
*(n = 125 clauses)*

| Correction Quality | Count | % of TPs |
| :--- | :--- | :--- |
| **Perfect** (Fixed all, 0 junk) | 34 | 27.20%
| **Good, but Sloppy** (Fixed all, >0 junk) | 80 | 64.00%
| **Partial, but Clean** (Missed some, 0 junk) | 8 | 6.40%
| **Partial & Sloppy** (Missed some, >0 junk) | 3 | 2.40%

| TP Error Averages | Total | Avg. per TP |
| :--- | :--- | :--- |
| Missed Problems | 12 | 0.10 |
| Unnecessary Changes | 150 | 1.20 |

---
**5. Correction Quality Analysis: False Positives (FPs)**
*(n = 233 clauses)*

| FP Error Averages | Total | Avg. per FP |
| :--- | :--- | :--- |
| Missed Problems | 0 | 0.00 |
| Unnecessary Changes | 629 | 2.70 |

---
**6. Correction Quality Analysis: False Negatives (FNs)**
*(n = 5 clauses)*

| FN Error Averages | Total | Avg. per FN |
| :--- | :--- | :--- |
| Missed Problems | 5 | 1.00 |
| Unnecessary Changes | 0 | 0.00 |

---
**7. Rule-Specific Performance**

| Rule ID | Title | Total Violations | Hits | Misses | Hallucinations | Rule Recall | Rule Precision | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 678bd828d87a6f8049fddf7a | Pausenregelung | 1 | 1 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678bd561d87a6f8049fddf73 | Einarbeitungsstunden Schaden | 2 | 2 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678a6002780e9d4cb9184c05 | Abwesenheitsgrund | 11 | 11 | 0 | 2 | 100.00% | 84.62% | 91.67% |
| 678a5d77780e9d4cb9184b91 | Generelles Pfändungsverbot | 12 | 11 | 1 | 1 | 91.67% | 91.67% | 91.67% |
| 678a620e780e9d4cb9184c34 | Anspruchgeltendmachung Form | 16 | 16 | 0 | 7 | 100.00% | 69.57% | 82.05% |
| 678a63c2780e9d4cb9184c65 | Vergütung Schulungen | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 678a6376780e9d4cb9184c57 | Abgeltung Überstunden Transparenz | 25 | 22 | 3 | 9 | 88.00% | 70.97% | 78.57% |
| 678a625a780e9d4cb9184c3b | Ausschlussfrist Limitierungen | 20 | 20 | 0 | 11 | 100.00% | 64.52% | 78.43% |
| 678bcb3dd87a6f8049fddf50 | Kündigungsfrist Probezeit | 6 | 5 | 1 | 4 | 83.33% | 55.56% | 66.67% |
| 678a5dfc780e9d4cb9184bfe | Kostenpauschale | 2 | 2 | 0 | 2 | 100.00% | 50.00% | 66.67% |
| 678a62a4780e9d4cb9184c42 | Verschwiegenheit Gehalt | 7 | 7 | 0 | 8 | 100.00% | 46.67% | 63.64% |
| 678bcbc7d87a6f8049fddf57 | Vertragsänderung Form | 13 | 13 | 0 | 15 | 100.00% | 46.43% | 63.41% |
| 678a618c780e9d4cb9184c21 | Zweistufige Ausschlussfristen | 11 | 10 | 1 | 13 | 90.91% | 43.48% | 58.82% |
| 67942f34d87a6f8049fde684 | Mindesturlaub | 2 | 2 | 0 | 3 | 100.00% | 40.00% | 57.14% |
| 678a6392780e9d4cb9184c5e | Mindestlohn | 7 | 5 | 2 | 6 | 71.43% | 45.45% | 55.56% |
| 678a6054780e9d4cb9184c0c | Nebenbeschäftigung Einschränkung | 9 | 9 | 0 | 22 | 100.00% | 29.03% | 45.00% |
| 691335a84d8b5fd53971f234 | Vertragsstrafe in Probezeit | 4 | 4 | 0 | 11 | 100.00% | 26.67% | 42.11% |
| 691334b64d8b5fd53971f21f | Günstigkeitsprinzip | 1 | 1 | 0 | 3 | 100.00% | 25.00% | 40.00% |
| 678a62d7780e9d4cb9184c49 | Verschwiegenheit Kenntnisse | 6 | 6 | 0 | 25 | 100.00% | 19.35% | 32.43% |
| 691335754d8b5fd53971f22d | Postzugang 4-Tages-Fiktion | 1 | 1 | 0 | 5 | 100.00% | 16.67% | 28.57% |
| 678a6320780e9d4cb9184c50 | Abgegoltene Überstunden | 2 | 2 | 0 | 10 | 100.00% | 16.67% | 28.57% |
| 6794200fd87a6f8049fde668 | Kündigungsfrist Arbeitgeber | 1 | 1 | 0 | 7 | 100.00% | 12.50% | 22.22% |
| 691334ea4d8b5fd53971f226 | Urlaub Übertragbarkeit | 1 | 1 | 0 | 13 | 100.00% | 7.14% | 13.33% |
| 678a63eb780e9d4cb9184c6c | Wettbewerbsverbot Minderheitsbeteilig... | 0 | 0 | 0 | 3 | 0.00% | 0.00% | 0.00% |
| 678bcc5ad87a6f8049fddf65 | Kündigungsfrist Max. Dauer | 0 | 0 | 0 | 2 | 0.00% | 0.00% | 0.00% |
| 678a607e780e9d4cb9184c13 | Einseitige Ausschlussfrist | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |
| 678a6447780e9d4cb9184c73 | Wettbewerbsverbot Karenzentschädigung | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |
| 691334564d8b5fd53971f1f5 | Kündigungsfrist nach Probezeit | 2 | 0 | 2 | 5 | 0.00% | 0.00% | 0.00% |
| 691335cf4d8b5fd53971f23b | Transparenzgebot | 1 | 0 | 1 | 142 | 0.00% | 0.00% | 0.00% |