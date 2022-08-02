from otsrdflib import OrderedTurtleSerializer
from rdflib.namespace import Namespace, SKOS, OWL


class Sequencer(object):
    def __init__(self, output_ttl, input_csv, graph):
        self.output = output_ttl
        self.input_csv = input_csv
        self.graph = graph

    def run(self):
        if "glosis_cl" in self.input_csv:
            main_class = OWL.Class
        else:
            main_class = Namespace('http://www.w3.org/ns/sosa/').Procedure
        serializer = OrderedTurtleSerializer(self.graph)
        serializer.class_order = [OWL.Ontology, SKOS.ConceptScheme, main_class, SKOS.Concept]
        with open(self.output, 'wb') as fp:
            serializer.serialize(fp)
