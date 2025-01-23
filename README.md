# German Employment Contract Clauses - Dataset

## Overview

This dataset contains **1094 samples** of clauses extracted from German employment contracts. Each sample includes the clause text, the title of its section, and three types of annotations:

1. **Legality label**: Classified as 'valid' (0), 'unfair' (0.5), or 'void' (1).
2. **Category**: Assigned to one of 14 predefined categories.
3. **Explanation**: Provided for clauses labeled as 'unfair' or 'void', detailing why the clause is problematic.

### Key Facts
- **Clause Definition**: A clause is a semantically self-contained segment of a German employment contract.
- **Annotation Process**: The annotations were conducted by two lawyers specializing in Economic Law. The process included three annotation rounds:
   - **Round 1**: 100 randomly selected clauses, inter-annotator agreement of 72.6%.
   - **Round 2**: 300 clauses, with improved inter-annotator agreement of 96.4%.
   - **Round 3**: Two distinct sets of ~400 clauses each, resulting in 794 annotated clauses. Combined with Round 2, this forms the final dataset.
- **Inter-Annotator Agreement**:
   - Legality labels: 96.4%
   - Categories: 100%
- **Bias Considerations**: While the dataset is drawn from anonymized client contracts, potential bias towards problematic clauses may exist due to the nature of contracts typically submitted for legal review.

### Example Clause
| Field              | Content                                                                                  |
|--------------------|------------------------------------------------------------------------------------------|
| **Clause**         | Die teilweise oder vollständige Abtretung und Pfändung der Vergütung ist ausgeschlossen. (The partial or complete assignment and seizure of the remuneration is excluded.) |
| **Section Title**  | 5 Abtretungen/Pfändungen (5 Assignments/Garnishments)                                    |
| **Category**       | Pfändung/Abtretung (Garnishment/Assignment)                                             |
| **Classification** | Void (1)                                                                            |
| **Explanation**    | Pfändungs-/Abtretungsverbot seit 10/2021 nach § 308 Nr. 9 lit. a BGB in AGB ausgeschlossen (Prohibition of garnishment/assignment excluded in general terms and conditions since 10/2021 according to § 308 No. 9 lit. a BGB) |

This dataset offers a unique resource for researchers, providing insights into common legal issues and supporting the development of AI tools for legal document analysis.

## Citation

If you use this dataset in your research, please cite our work as follows:

```bibtex
@inproceedings{wardas2024employment,
  title={AI-assisted German Employment Contract Review: A Benchmark Dataset},
  author={Oliver, Wardas and Florian, Matthes},
  booktitle={IRIS: Internationales Rechtsinformatik Symposium},
  year={2025},
  note={Dataset available at https://github.com/sebischair/Employment-Contract-Clauses-German}
}
```

## License

This dataset is provided under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://github.com/sebischair/Employment-Contract-Clauses-German/blob/master/LICENSE) license. Please ensure proper attribution when using this dataset.

## Dataset Statistics

| Category (de)           | Translation (en)          | Valid | Unfair | Void | Sum | Void or Unfair |
|-------------------------|---------------------------|-------|--------|------|-----|----------------|
| Sonstiges              | Other                     | 161   | 11     | 6    | 178 | 9.6%          |
| Vergütung             | Compensation              | 100   | 27     | 21   | 148 | 32.4%         |
| Vertragsstrafe         | Penalty Clause            | 111   | 24     | 10   | 145 | 23.5%         |
| Durchführung           | Execution                 | 111   | 12     |      | 123 | 9.8%          |
| Kündigung/Beendigung  | Termination               | 93    | 12     | 5    | 110 | 15.5%         |
| Leistungen             | Tasks                     | 98    | 5      | 1    | 104 | 5.8%          |
| Krankheit              | Illness                   | 73    | 17     |      | 90  | 18.9%         |
| Urlaub                 | Vacation                  | 62    | 12     |      | 74  | 16.2%         |
| Verjährung             | Statute of Limitations    | 23    | 7      | 6    | 36  | 36.1%         |
| Form                   | Format                    | 21    | 12     | 1    | 34  | 38.2%         |
| Pfändung/Abtretung     | Garnishment               | 12    | 9      | 7    | 28  | 67.9%         |
| Überstunden            | Overtime                  | 9     | 1      | 1    | 11  | 18.2%         |
| Ausschlussfristen      | Cut-off Periods           |       | 2      | 7    | 9   | 100%          |
| Erfindungen            | Inventions                | 4     |        |      | 4   | 0%            |
| **SUM**                |                           | 875   | 149    | 70   | 1094| 20%           |

## Acknowledgements

Special thanks to SYLVENSTEIN Rechtsanwälte for their collaboration and support in annotating and validating the dataset.

