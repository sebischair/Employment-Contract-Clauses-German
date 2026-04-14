**Benchmark Summary**
* **Total Clauses:** 886
* **Truly Void:** 130
* **Truly Valid:** 756

---
**1. Classification Metrics (The "Funnel")**

| Metric | Score |
| :--- | :--- |
| Accuracy | 72.91% |
| Precision | 34.55% |
| Recall | 94.62% |
| F1-Score | 0.51 |

| | **Predicted: Void** | **Predicted: Valid** |
| :--- | :--- | :--- |
| **Actual: Void** | 123 (TP) | 7 (FN) |
| **Actual: Valid** | 233 (FP) | 523 (TN) |

---
**2. Linguistic Quality of Corrections**
*(n = 356 attempted corrections)*

| Linguistic Metric | Avg. Delta |
| :--- | :--- |
| Readability (Flesch-Kincaid Grade) | +1.41 grades |
| Verbosity (Word Count) | +32.33 words |

---
**3. Overall Correction Quality (All Clauses)**
*(n = 886 clauses)*

| Metric | Total | Avg. per Clause |
| :--- | :--- | :--- |
| **Total Problems Missed** | 18 | 0.02 |
| **Total Unnecessary Changes** | 899 | 1.01 |

---
**4. Correction Quality Analysis: True Positives (TPs)**
*(n = 123 clauses)*

| Correction Quality | Count | % of TPs |
| :--- | :--- | :--- |
| **Perfect** (Fixed all, 0 junk) | 15 | 12.20%
| **Good, but Sloppy** (Fixed all, >0 junk) | 98 | 79.67%
| **Partial, but Clean** (Missed some, 0 junk) | 3 | 2.44%
| **Partial & Sloppy** (Missed some, >0 junk) | 7 | 5.69%

| TP Error Averages | Total | Avg. per TP |
| :--- | :--- | :--- |
| Missed Problems | 10 | 0.08 |
| Unnecessary Changes | 195 | 1.59 |

---
**5. Correction Quality Analysis: False Positives (FPs)**
*(n = 233 clauses)*

| FP Error Averages | Total | Avg. per FP |
| :--- | :--- | :--- |
| Missed Problems | 0 | 0.00 |
| Unnecessary Changes | 704 | 3.02 |

---
**6. Correction Quality Analysis: False Negatives (FNs)**
*(n = 7 clauses)*

| FN Error Averages | Total | Avg. per FN |
| :--- | :--- | :--- |
| Missed Problems | 8 | 1.14 |
| Unnecessary Changes | 0 | 0.00 |

---
**7. Rule-Specific Performance**

| Rule ID | Title | Total Violations | Hits | Misses | Hallucinations | Rule Recall | Rule Precision | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 678a5d77780e9d4cb9184b91 | Generelles Pfändungsverbot | 12 | 12 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678a5dfc780e9d4cb9184bfe | Kostenpauschale | 2 | 2 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678bd828d87a6f8049fddf7a | Pausenregelung | 1 | 1 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678bd561d87a6f8049fddf73 | Einarbeitungsstunden Schaden | 2 | 2 | 0 | 0 | 100.00% | 100.00% | 100.00% |
| 678a6002780e9d4cb9184c05 | Abwesenheitsgrund | 11 | 11 | 0 | 2 | 100.00% | 84.62% | 91.67% |
| 678a620e780e9d4cb9184c34 | Anspruchgeltendmachung Form | 16 | 16 | 0 | 4 | 100.00% | 80.00% | 88.89% |
| 678a6376780e9d4cb9184c57 | Abgeltung Überstunden Transparenz | 25 | 22 | 3 | 6 | 88.00% | 78.57% | 83.02% |
| 678a625a780e9d4cb9184c3b | Ausschlussfrist Limitierungen | 20 | 19 | 1 | 7 | 95.00% | 73.08% | 82.61% |
| 678a63c2780e9d4cb9184c65 | Vergütung Schulungen | 2 | 2 | 0 | 1 | 100.00% | 66.67% | 80.00% |
| 678a62a4780e9d4cb9184c42 | Verschwiegenheit Gehalt | 7 | 7 | 0 | 5 | 100.00% | 58.33% | 73.68% |
| 678bcbc7d87a6f8049fddf57 | Vertragsänderung Form | 13 | 13 | 0 | 12 | 100.00% | 52.00% | 68.42% |
| 67942f34d87a6f8049fde684 | Mindesturlaub | 2 | 2 | 0 | 2 | 100.00% | 50.00% | 66.67% |
| 691334b64d8b5fd53971f21f | Günstigkeitsprinzip | 1 | 1 | 0 | 1 | 100.00% | 50.00% | 66.67% |
| 678bcb3dd87a6f8049fddf50 | Kündigungsfrist Probezeit | 6 | 4 | 2 | 4 | 66.67% | 50.00% | 57.14% |
| 678a6054780e9d4cb9184c0c | Nebenbeschäftigung Einschränkung | 9 | 9 | 0 | 17 | 100.00% | 34.62% | 51.43% |
| 678a618c780e9d4cb9184c21 | Zweistufige Ausschlussfristen | 11 | 10 | 1 | 19 | 90.91% | 34.48% | 50.00% |
| 678a6392780e9d4cb9184c5e | Mindestlohn | 7 | 2 | 5 | 0 | 28.57% | 100.00% | 44.44% |
| 691335a84d8b5fd53971f234 | Vertragsstrafe in Probezeit | 4 | 4 | 0 | 11 | 100.00% | 26.67% | 42.11% |
| 691334564d8b5fd53971f1f5 | Kündigungsfrist nach Probezeit | 2 | 1 | 1 | 2 | 50.00% | 33.33% | 40.00% |
| 678a62d7780e9d4cb9184c49 | Verschwiegenheit Kenntnisse | 6 | 5 | 1 | 21 | 83.33% | 19.23% | 31.25% |
| 678a6320780e9d4cb9184c50 | Abgegoltene Überstunden | 2 | 2 | 0 | 11 | 100.00% | 15.38% | 26.67% |
| 691335754d8b5fd53971f22d | Postzugang 4-Tages-Fiktion | 1 | 1 | 0 | 8 | 100.00% | 11.11% | 20.00% |
| 6794200fd87a6f8049fde668 | Kündigungsfrist Arbeitgeber | 1 | 1 | 0 | 10 | 100.00% | 9.09% | 16.67% |
| 691334ea4d8b5fd53971f226 | Urlaub Übertragbarkeit | 1 | 1 | 0 | 19 | 100.00% | 5.00% | 9.52% |
| 678a63eb780e9d4cb9184c6c | Wettbewerbsverbot Minderheitsbeteilig... | 0 | 0 | 0 | 2 | 0.00% | 0.00% | 0.00% |
| 691335cf4d8b5fd53971f23b | Transparenzgebot | 1 | 0 | 1 | 160 | 0.00% | 0.00% | 0.00% |
| 678a607e780e9d4cb9184c13 | Einseitige Ausschlussfrist | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |
| 678a6477780e9d4cb9184c7a | Wettbewerbsverbot Max. Dauer | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |
| 678a6447780e9d4cb9184c73 | Wettbewerbsverbot Karenzentschädigung | 0 | 0 | 0 | 2 | 0.00% | 0.00% | 0.00% |
| 678bcc5ad87a6f8049fddf65 | Kündigungsfrist Max. Dauer | 0 | 0 | 0 | 1 | 0.00% | 0.00% | 0.00% |