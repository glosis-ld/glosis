import sys

from src.transformers.rdf_to_csv import rdf_to_csv

if __name__ == "__main__":
    rdf_file = sys.argv[1]
    output_filename = sys.argv[2] if sys.argv[2] else None
    if "glosis_cl" in rdf_file:
        transformer = rdf_to_csv.Transformer(file=rdf_file, file_type="codelist", output_filename=output_filename)
    elif "glosis_procedure" in rdf_file:
        transformer = rdf_to_csv.Transformer(file=rdf_file, file_type="procedure", output_filename=output_filename)
    else:
        sys.exit("Input file not recognized.")
    transformer.transform_to_csv()
