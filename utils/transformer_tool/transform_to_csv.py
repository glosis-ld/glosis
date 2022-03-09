import sys

from src.transformers.rdf_to_csv import rdf_to_csv

if __name__ == "__main__":
    rdf_file = sys.argv[1]
    if "glosis_cl" in rdf_file:
        transformer = rdf_to_csv.Transformer(file=rdf_file, file_type="codelist")
    elif "glosis_procedure" in rdf_file:
        transformer = rdf_to_csv.Transformer(file=rdf_file, file_type="procedure")
    else:
        sys.exit("Input file not recognized.")
    transformer.transform_to_csv()
