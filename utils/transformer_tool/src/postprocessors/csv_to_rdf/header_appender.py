import sys

import rdflib
from rdflib.term import Literal, URIRef


class HeaderAppender(object):
    def __init__(self, input_csv, graph, version):
        self.graph = graph
        self.input_csv = input_csv
        self.header = self._extract_type()
        self.version = version

    def _extract_type(self):
        if "glosis_result" in self.input_csv:
            return "static/results_header.ttl"
        elif "glosis_property_descriptive" in self.input_csv:
            return "static/prop_desc_header.ttl"
        elif "glosis_property_physchem" in self.input_csv:
            return "static/prop_pch_header.ttl"
        elif "glosis_procedure" in self.input_csv:
            return "static/procedure_header.ttl"
        else:
            sys.exit("Input file not recognized.")

    def run(self):
        g2 = rdflib.Graph()
        g3 = rdflib.Graph()
        g2.parse(self.header, format="turtle")
        for ns in g2.namespaces():
            self.graph.namespace_manager.bind(ns[0], ns[1])
        for s, p, o in g2:
            if "versionIRI" in p.n3():
                o = URIRef(o.replace("x.x.x", self.version))
            if "versionInfo" in p.n3():
                o = Literal(o.replace("x.x.x", self.version))
            g3.add((s, p, o))

        self.graph += g3
        return self.graph
