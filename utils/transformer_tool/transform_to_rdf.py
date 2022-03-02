import sys

from src.transformers.csv_to_rdf import csv_to_rdf

if __name__ == "__main__":
    transformer = csv_to_rdf.Transformer(input_csv=sys.argv[1], query=sys.argv[2], output_ttl=sys.argv[3])
    transformer.run()
