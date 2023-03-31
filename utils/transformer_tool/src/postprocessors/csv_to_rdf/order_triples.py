from otsrdflib import OrderedTurtleSerializer
from rdflib.namespace import SKOS, OWL


class Sequencer(object):
    def __init__(self, output_ttl, input_csv, graph):
        self.output = output_ttl
        self.input_csv = input_csv
        self.graph = graph

    def run(self):
        serializer = OrderedTurtleSerializer(self.graph)
        serializer.class_order = [OWL.Ontology, SKOS.ConceptScheme, OWL.Class, SKOS.Concept]
        with open(self.output, 'wb') as fp:
            serializer.serialize(fp)
