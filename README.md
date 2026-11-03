# German Employment Contract Clauses - Dataset

## Overview

This dataset contains clauses, extracted from German employment contracts, which have been annotated by lawyers, specialized in economic law.
It offers a unique resource for researchers, providing insights into common legal issues and supporting the development of AI tools for contract legality analysis.

## Versions

The dataset is periodically updated according to changes in regulation and new court rulings. New versions might also contain additional annotations and supporting data. Available versions:

- V1: The initial dataset (August 2023, IRIS25)
- V2: Several new annotations and supporting data added (January 2025, ICAIL25)
- V3: Exhaustive error annotations added (January 2026, ICAIL26)


## Errata

The following corrections were made to `data/rules.json` in V2 and V3 in November 2026. The logs of the published experiments were not changed and still contain the original wording.

- **Rule "Mindestlohn":** The statutory minimum wage was updated from 12,41 € (in force in 2024) to 12,82 € (in force since 1 January 2025). No clause label is affected, as no hourly wage in the dataset lies between the two values.
- **Reference "BAG, Urteil vom 24.01.1966 – 2 AZR 264/6"** was corrected to "BAG, Urteil vom 21.04.1966 – 2 AZR 264/65". The corresponding V2 source file was renamed accordingly.
- **Reference "BMF, Schreiben vom 19.05.2015, BStBI 2015 I S. 468"** was corrected to "BStBl". The corresponding V2 source file was renamed accordingly.

## Citation

If you use this dataset in your research, please cite our work as described in each version. Citation templates are available in each version subfolder.

## License

This dataset is provided under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://github.com/sebischair/Employment-Contract-Clauses-German/blob/master/LICENSE) license. Please ensure proper attribution when using this dataset.

## Acknowledgements

Special thanks to SYLVENSTEIN Rechtsanwälte for their collaboration and support in annotating and validating the dataset.

