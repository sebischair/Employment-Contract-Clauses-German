# German Employment Contract Clauses - Dataset

## Citation

If you use this dataset in your research, please cite our work as follows:

```bibtex
@inproceedings{wardas2025subsumption,
  title={LLMs for Legal Subsumption in German Employment Contracts},
  author={Wardas, Oliver and Matthes, Florian},
  booktitle={Proceedings of the Twentieth International Conference on Artificial Intelligence and Law},
  pages={169--176},
  year={2025},
  note={Dataset available at https://github.com/sebischair/Employment-Contract-Clauses-German}
}
```

## Overview

This dataset contains **886 samples** of clauses extracted from German employment contracts with exhaustive legal error annotations. The reduction in samples from the previous version is due to the merge of one erroneously fragmented clause.

### Contained Data:
- **Clauses (886)**
   1. **content**: Clause text
   2. **heading**: Title of the section
   3. **topic**: Reference to one topic
   4. **true_label**: Classification as 'valid', 'unfair', or 'void'
   5. **true_explanation** (only for void): Short explanation for ALL legal defects
   6. **true_hurt-rules** (only for void): Array of ALL ids of rules under which void was subsumed
- **Topics (14)**
   1. **_id**: Id
   2. **title**: Title of the topic
- **Rules (30)**
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

| **Category** | **Valid** | **Unfair** | **Void** | **Sum**|
|---------------------------------------|------------------|------------------|------------------|--------|
| Durchführung                          | 97 (89.8%)       | 9 (8.3%)         | 2 (1.9%)         | 108    |
| Krankheit                             | 57 (81.4%)       | 2 (2.9%)         | 11 (15.7%)       | 70     |
| Vertragsstrafe/Wettbewerbsverbot      | 90 (76.9%)       | 6 (5.1%)         | 21 (17.9%)       | 117    |
| Kündigung/Beendigung                  | 80 (87.9%)       | 3 (3.3%)         | 8 (8.8%)         | 91     |
| Verjährung                            | 15 (53.6%)       | 0 (0.0%)         | 13 (46.4%)       | 28     |
| Sonstiges                             | 127 (93.4%)      | 6 (4.4%)         | 3 (2.2%)         | 136    |
| Leistungen                            | 82 (94.3%)       | 3 (3.4%)         | 2 (2.3%)         | 87     |
| Vergütung                             | 86 (68.3%)       | 6 (4.8%)         | 34 (27.0%)       | 126    |
| Urlaub                                | 47 (81.0%)       | 8 (13.8%)        | 3 (5.2%)         | 58     |
| Form                                  | 11 (45.8%)       | 1 (4.2%)         | 12 (50.0%)       | 24     |
| Überstunden                           | 6 (75.0%)        | 1 (12.5%)        | 1 (12.5%)        | 8      |
| Pfändung/Abtretung                    | 9 (45.0%)        | 0 (0.0%)         | 11 (55.0%)       | 20     |
| Erfindungen                           | 4 (100.0%)       | 0 (0.0%)         | 0 (0.0%)         | 4      |
| Ausschlussfristen                     | 0 (0.0%)         | 0 (0.0%)         | 9 (100.0%)       | 9      |
| **SUM**                               | 711 (80.2%)      | 45 (5.1%)        | 130 (14.7%)      | 886    |
