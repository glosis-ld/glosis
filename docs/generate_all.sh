#!/bin/bash

source env/bin/activate

python3 generateDoc.py glosis_common
python3 generateDoc.py glosis_layer_horizon
python3 generateDoc.py glosis_main
python3 generateDoc.py glosis_observation
python3 generateDoc.py glosis_procedures
python3 generateDoc.py glosis_profile
python3 generateDoc.py glosis_properties
python3 generateDoc.py glosis_results
python3 generateDoc.py glosis_siteplot
python3 generateDoc.py glosis_surface
python3 generateDoc.py glosis_unit
python3 generateDoc.py iso28258

deactivate
