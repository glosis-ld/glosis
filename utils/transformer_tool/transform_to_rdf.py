import sys
import os

from src.postprocessors.csv_to_rdf import oneOf_postprocess
from src.postprocessors.csv_to_rdf import header_appender
from src.postprocessors.csv_to_rdf import order_triples
from src.transformers.csv_to_rdf import csv_to_rdf

if __name__ == "__main__":
    # input data
    input_csv = sys.argv[1]
    query = sys.argv[2]
    output_ttl = sys.argv[3]
    version = sys.argv[4]
    # actions
    transformer = csv_to_rdf.Transformer(input_csv=input_csv, query=query)
    temp = transformer.run()
    postprocessor = oneOf_postprocess.PostProcessor(input_csv=input_csv, temp=temp)
    graph = postprocessor.run()
    header_appender = header_appender.HeaderAppender(input_csv=input_csv, graph=graph, version=version)
    graph = header_appender.run()
    sequencer = order_triples.Sequencer(output_ttl=output_ttl, input_csv=input_csv, graph=graph)
    sequencer.run()
    os.remove(temp)
