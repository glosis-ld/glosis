WiDoco auto-config
==================

This folder contains the assets necessary to generate the documentation of the
various ontology modules. Ultimatelly, the documentation is created by WiDoco,
but some pre-processing is necessary to transform the ontology meta-data into
WiDoco input config files.

This auto-config programme is necessary since WiDoco is not yet able to deal
with meta-data vocabularies (VCard, Doublin Core, Schema.org). [An issue](https://github.com/dgarijo/Widoco/issues/285) 
is currently open on this matter. Once that issue is closed this programme might no
longer be necessary. 

config
------

The auto-config programme needs to be awere of the location of the WiDoco `.jar`
file. This information is set up in the `config`, an input to the programme.
This file also stores the location of the WiDoco template, stored in a separate
file for convinience (`template.json`, see below). 

Before running the programme edit this file inserting the right path to the
WiDoco `.jar` in your system. 


template.json
-------------

Contains a dictionary with various WiDoco options that compose the input config
file. All the values in this dictionary are replaced with meta-data obtained from the
ontology file itself, except the following:
- status
- licenseURI
- licenseName
- licenseIconURL

Updated these items directly in the `template.json` file if you wish to modify them.

requirements.txt
----------------

The auto-config programme depends on a few Python libraries enumerated in the
`requirements.txt` file. A virtual environment is a simple and convinient method
to set up these libraries:

```
python3 -m venv env

source ~/env/bin/activate

pip3 install -p requirements.txt
```

generateDoc.py
--------------

Creates a config file for an ontology module and runs WiDoco. The HTML outputs
are stored in a folder with the same name of the ontology module.

The programme takes as single input the name of a module, e.g. `glosis_main`. It
then opens the corresponding Turtle file in the parent folder As an example to
create the documentation for the `glosis_common` module:

```
python3 createConfig.py glosis_common
```

