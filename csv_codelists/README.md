This folder contains the latest version of CSV files with codelists for the following modules:

- [glosis_cl](../glosis_cl.ttl), sources: [glosis_cl](./glosis_cl.csv), [glosis_result](./glosis_result.csv), [glosis_property_descriptive](./glosis_property_descriptive.csv), [glosis_property_physchem](.\glosis_property_physchem.csv)
- [glosis_procedure](../glosis_procedure.ttl), source [glosis_procedure](./glosis_procedure.csv)

A [the transformer_tool](../utils/transformer_tool) can be used to convert vocabularies from csv to .ttl or vice versa. More details can be found in the [transformer_tool_README](../utils/transformer_tool/README.md).

As it stands today, the files are being updated on demand, but in the future we plan to have a CI/CD cycle that will guarantee that the folder contains the latests data. 