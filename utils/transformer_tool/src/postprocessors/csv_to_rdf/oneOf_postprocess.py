import sys
import pandas as pd
import re

import numpy as np
import rdflib
from rdflib.collection import Collection
from rdflib.term import BNode, URIRef


class PostProcessor(object):
    def __init__(self, input_csv, temp):
        self.input_csv = input_csv
        self.temp = temp
        self.base_uri = None
        self.the_object = None
        self.data = dict()

    def _set_base_uri(self):
        if "glosis_cl" in self.input_csv:
            self.the_object = URIRef("http://www.w3.org/2002/07/owl#" + "Class")
            self.base_uri = "http://w3id.org/glosis/model/codelists#"
        elif "glosis_procedure" in self.input_csv:
            self.the_object = URIRef("http://www.w3.org/ns/sosa/" + "Procedure")
            self.base_uri = "http://w3id.org/glosis/model/procedure#"
        else:
            sys.exit("Input file not recognized.")

    def _select_attrs_and_instances(self):
        df = pd.read_csv(self.input_csv)
        unique_attrs = list(df["attribute"].unique())   # list of unique attrs
        for attr in unique_attrs:
            instances = list(df.instance[df["attribute"] == attr])
            key_name = attr[0].upper() + attr[1:]   # capitalize first letter
            if np.nan in instances:
                instances = None
            self.data[key_name] = instances

    def _get_attr_name(self, attribute):
        attr_name = re.findall(r"(?<=#).*(?=ValueCode|PropertyCode|Procedure)", attribute)[-1]
        postfix = re.findall(r"ValueCode|PropertyCode|Procedure", attribute)[-1]
        return attr_name, postfix

    def _generate_instance_uri(self, instance, postfix, attr):
        return URIRef(self.base_uri + attr + postfix + "-" + instance)

    def run(self):
        self._set_base_uri()
        self._select_attrs_and_instances()
        g = rdflib.Graph()
        g.parse(self.temp, format="turtle")
        g.namespace_manager.bind("owl", "http://www.w3.org/2002/07/owl#")
        ns_type = rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        for s, p, o in g:
            if o == self.the_object and p == ns_type:
                if any(word in s for word in ["ValueCode", "PropertyCode", "Procedure"]):
                    attr_name, postfix = self._get_attr_name(attribute=s.n3())
                    attr = attr_name[0].lower() + attr_name[1:]
                    instances = self.data.get(attr_name)
                    if instances:
                        instance_uris = [self._generate_instance_uri(instance, postfix, attr) for instance in instances]
                        bn = BNode()
                        g.add((s, URIRef("http://www.w3.org/2002/07/owl#oneOf"), bn))
                        Collection(g, bn, instance_uris)
        return g
