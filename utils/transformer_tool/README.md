# Python Script for transforming CSV files into ttl against SPARQL query

## Prerequisites

1. pytarql command line tool (https://github.com/semanticarts/pytarql)
2. rdflib python library (https://rdflib.readthedocs.io/en/stable/)
3. pandas (https://pandas.pydata.org/)

## Usage

Script can transform in two ways:
1) from csv -> rdf, ``python transform_to_rdf.py [path to input csv] [path to SPARQL query file] [output filename]``
2) from rdf -> csv  ``python transform_to_csv.py [path to rdf file]``

*example:*    
```python transform_to_rdf.py data/test.csv data/myquery.rq output.ttl```