# German Employment Contract Clauses - Dataset

## Citation

If you use this dataset in your research, please cite our work as follows:

```bibtex
@inproceedings{wardas2024subsumption,
  title={LLMs for Legal Subsumption in German Employment Contracts},
  author={Wardas, Oliver and Matthes, Florian},
  booktitle={ICAIL: International Conference on Artificial Intelligence and Law},
  year={2025},
  note={Dataset available at https://github.com/sebischair/Employment-Contract-Clauses-German}
}
```

## Overview

This dataset contains **891 samples** of clauses extracted from German employment contracts with updated legality labels and additional annotations. The reduction in samples from the previous version is due to the removal of conflicting legality annotations for identical clauses (keeping the more critical annotation).

### Contained Data:
- **Clauses (891)**
   1. **content**: Clause text
   2. **heading**: Title of the section
   3. **topic**: Reference to one topic
   4. **true_label**: Classification as 'valid', 'unfair', or 'void'
   5. **true_explanation** (only for unfair/void): Short explanation for the classification
   6. **true_hurt-rules** (only for void): Array of ids of rules under which void was subsumed
- **Topics (14)**
   1. **_id**: Id
   2. **title**: Title of the topic
- **Rules (24)**
   1. **_id**: Id
   2. **title**: Title of the rule
   3. **text**: Content of the rule
   4. **topic**: Reference to one topic
   5. **references**: Array of references to legal sources from which the rule was derived

### Example Clause

| Field              | Content                                                                                  |
|--------------------|------------------------------------------------------------------------------------------|
| **Clause**         | Die teilweise oder vollständige Abtretung und Pfändung der Vergütung ist ausgeschlossen. (The partial or complete assignment and seizure of the remuneration is excluded.) |
| **Section Title**  | 5 Abtretungen/Pfändungen (5 Assignments/Garnishments)                                    |
| **Category**       | Pfändung/Abtretung (Garnishment/Assignment)                                             |
| **Classification** | void                                                                            |
| **True Explanation**    | Pfändungs-/Abtretungsverbot seit 10/2021 nach § 308 Nr. 9 lit. a BGB in AGB ausgeschlossen (Prohibition of garnishment/assignment excluded in general terms and conditions since 10/2021 according to § 308 No. 9 lit. a BGB) |
| **True Hurt Rules** (ref)   | \["Eine Klausel, die in den AGB ein generelles Pfändungs- oder Abtretungsverbot für die Forderungen des Arbeitnehmers festlegt, ist unwirksam."\] |

## Dataset Statistics

| **Category**                          | **Valid**        | **Unfair**       | **Void**         | **Sum**|
|---------------------------------------|------------------|------------------|------------------|--------|
| Durchführung                          | 97 (89.8%)       | 11 (10.2%)       | 0 (0.0%)         | 108    |
| Krankheit                             | 57 (81.4%)       | 5 (7.1%)         | 8 (11.4%)        | 70     |
| Vertragsstrafe/Wettbewerbsverbot      | 82 (70.1%)       | 14 (12.0%)       | 21 (17.9%)       | 117    |
| Kündigung/Beendigung                  | 80 (87.0%)       | 8 (8.7%)         | 4 (4.3%)         | 92     |
| Verjährung                            | 16 (53.3%)       | 2 (6.7%)         | 12 (40.0%)       | 30     |
| Sonstiges                             | 126 (92.0%)      | 10 (7.3%)        | 1 (0.7%)         | 137    |
| Leistungen                            | 79 (90.8%)       | 3 (3.4%)         | 5 (5.7%)         | 87     |
| Vergütung                             | 85 (66.9%)       | 8 (6.3%)         | 34 (26.8%)       | 127    |
| Urlaub                                | 46 (79.3%)       | 11 (19.0%)       | 1 (1.7%)         | 58     |
| Form                                  | 11 (45.8%)       | 7 (29.2%)        | 6 (25.0%)        | 24     |
| Überstunden                           | 6 (75.0%)        | 1 (12.5%)        | 1 (12.5%)        | 8      |
| Pfändung/Abtretung                    | 8 (40.0%)        | 1 (5.0%)         | 11 (55.0%)       | 20     |
| Erfindungen                           | 4 (100.0%)       | 0 (0.0%)         | 0 (0.0%)         | 4      |
| Ausschlussfristen                     | 0 (0.0%)         | 1 (11.1%)        | 8 (88.9%)        | 9      |
| **SUM**                               | 697 (78.2%)      | 82 (9.2%)        | 112 (12.6%)      | 891    |
