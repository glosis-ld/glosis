# Table of contents

- [Table of contents](#table-of-contents)
- [Info](#info)
- [Documentation](#documentation)
- [Tools](#tools)
  - [Transformer-tool](#transformer-tool)
    - [Installation](#installation)
    - [Usage](#usage)
  - [Version Updater](#version-updater)
    - [Requirements](#requirements)
    - [Usage](#usage-1)
- [Citing](#citing)


# Info
This repository contains the Global Soil Information System (GloSIS) v1.0 ontology network, derived from the source UML data model,
and modelled in line with best practices and methodologies, reusing existing standard models and ontologies.

# Documentation

All modules in this web ontology are documented individually with HTML pages
generated with the [WiDoco](https://github.com/dgarijo/Widoco) tool. These pages can be accessed at [https://rapw3k.github.io/glosis/docs/](https://rapw3k.github.io/glosis/docs/).

Configuration files for WiDoco are generated automatically with a [bespoke
tool](https://github.com/rapw3k/glosis/blob/glosis_doc/doc/README.md).
Documentation pages are maintained in the [glosis_doc branch](https://github.com/rapw3k/glosis/tree/glosis_doc/doc).

The documentation for each module can be accessed via the [documentation entry page](https://rapw3k.github.io/glosis/docs)

# Tools

## Transformer-tool

[Transformer-tool](https://github.com/rapw3k/glosis/tree/master/utils/transformer_tool) is a bi-directional tool that allows generating RDF representation using SPARQL query and list of codelist items in CSV file or another way around by generating a CSV list of items out of RDF representation.

### Installation

One should perform the following steps before running the script:

1. ``pip install - r requirements.txt``
2. ``git clone https://github.com/Montanaz0r/pytarql.git``
3. cd into cloned repository and run ``pip install .`` to activate setup.py

### Usage

Script can transform in two ways:
1) from csv -> rdf, ``python transform_to_rdf.py [path to input csv] [path to SPARQL query file] [output filename] [version]``
2) from rdf -> csv  ``python transform_to_csv.py [path to rdf file]``

*examples:*    
```python transform_to_rdf.py data/test.csv data/myquery.rq output.ttl 1.1.1```

```python transform_to_csv.py input.ttl```
(this creates a csv file with corresponding filename in the location of TURTLE file)

## Version Updater

[Version updater](https://github.com/rapw3k/glosis/tree/master/utils/version_updater) is a simple convenience script that updates and harmonizes versions across all ontology modules.

### Requirements

python3

### Usage

*example:*    
```python utils/version_updater/version_updater.py 3.0.1```

# Citing

Cite as:

> Palma R., Janiak B., Reznik T., Schleidt K., Kozel, J., De Sousa L., Egmond F., Mouazen A. M., Moshou, D. (2020) Global Soil Information System (GloSIS) Ontology. SIEUSOIL project. http://w3id.org/glosis/model 


Shield: [![CC BY NC SA 3.0 IGO][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO][cc-by].

[![CC BY NC SA 3.0 IGO][cc-by-image]][cc-by]

[cc-by]: https://creativecommons.org/licenses/by-nc-sa/3.0/igo/
[cc-by-image]: https://licensebuttons.net/l/by/3.0/igo/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%20NC%20SA%203.0%20IGO-lightgrey.svg
