import csv
import os
import re
import logging
import datetime

import rdflib
import pandas as pd


class Transformer(object):
    def __init__(self, file, file_type, output_filename=None):
        self.filename = file
        self.graph = self._parse_into_graph()
        self.file_type = file_type
        self.postfix = self._set_postfix_based_on_type()
        self.attributes = []
        self.results = {}
        self.base_uri = self._get_base_uri() if self.file_type == "procedure" else \
            rdflib.term.URIRef(f'http://w3id.org/glosis/model/codelists/')
        self.output = output_filename if output_filename else os.path.splitext(file)[0]

        # setting up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        current_date = datetime.datetime.now()
        self.log_path = os.path.join('logs',
                                     f'rdf_to_csv_{current_date.year}-{current_date.month}-{current_date.day}.log')
        self.file_handler = logging.FileHandler(self.log_path)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def _parse_into_graph(self):
        g = rdflib.Graph()
        try:
            g.parse(self.filename, format="ttl")
            return g
        except FileNotFoundError:
            print("File not found, please double-check the path that you provided!")
            return

    def _get_base_uri(self):
        return rdflib.term.URIRef(f'http://w3id.org/glosis/model/{self.postfix.lower()}/')

    def _set_postfix_based_on_type(self):
        if self.file_type == "procedure":
            return "Procedure"
        elif self.file_type == "codelist":
            return "ValueCode"
        else:
            print("Unrecognized file_type! Has to be one of: procedure, codelist")

    def _get_attr_name(self, attribute):
        attr_name = re.findall(rf"(?<={self.base_uri}).*(?=ValueCode|PropertyCode|Procedure)", attribute)[-1]
        postfix = re.findall(r"ValueCode|PropertyCode|Procedure", attribute)[-1]
        return attr_name, postfix

    def _get_instance_name(self, instance):
        return re.findall(r"(?:(?<=ValueCode\-)|(?<=PropertyCode\-)|(?<=Procedure\-)).*(?=>)", instance)[-1]

    def _select_attributes(self):
        concept_scheme = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#ConceptScheme')
        for s, p, o in self.graph:
            if o == concept_scheme:
                self.attributes.append(self._get_attr_name(attribute=s.n3()))

    def _select_instances(self):
        concept = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#Concept')
        ns_type = rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        for attribute in self.attributes:
            current_instances = []
            for s, p, o in self.graph:
                if o == concept and p == ns_type:
                    if any(word in s for word in [f"{attribute[0]}ValueCode", f"{attribute[0]}PropertyCode",
                                                  f"{attribute[0]}Procedure"]):
                        instance_value = self._get_instance_name(instance=s.n3())
                        current_instances.append(instance_value)
            self.results.update({attribute: dict.fromkeys(current_instances, {})})

    @staticmethod
    def _is_property(phrase):
        return True if "PropertyCode" in phrase else False

    def _get_instance_details(self):
        for attribute in self.results.keys():
            concept_definition = None
            if self.file_type == "codelist":
                attr_uri = self.base_uri + attribute[0] + attribute[1]
                for s, p, o in self.graph:
                    if s == attr_uri and p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#definition"):
                        concept_definition = o.n3().strip('"')
            if self.results[attribute]:
                for instance in self.results[attribute].keys():
                    property_dict = {}
                    property_dict["concept_definition"] = concept_definition
                    property_dict["isproperty"] = self._is_property(attribute[1])
                    instance_phrase = f"{attribute[0]}{attribute[1]}-{instance}"
                    instance_uri = self.base_uri + instance_phrase
                    for s, p, o in self.graph:
                        if s == instance_uri:
                            if p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#definition"):
                                property_dict["definition"] = o.n3().strip('"')
                            elif p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#notation"):
                                property_dict["notation"] = o.n3().strip('"')
                            elif p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"):
                                property_dict["label"] = o.n3().strip('"').removesuffix('"@en')
                            elif p == rdflib.URIRef("http://dbpedia.org/property/inchikey"):
                                property_dict["inchi_key"] = o.n3().strip('"').removesuffix('"@en')
                            elif p == rdflib.URIRef("http://dbpedia.org/ontology/inchi"):
                                property_dict["inchi"] = o.n3().strip('"').removesuffix('"@en')
                            elif p == rdflib.URIRef("http://dbpedia.org/ontology/pubchem"):
                                property_dict["pub_chem"] = o.n3().strip('"').removesuffix('"@en')
                            elif "scopeNote" in p:
                                if isinstance(o, rdflib.term.Literal):
                                    property_dict["citation"] = o.n3().strip('"')
                                elif isinstance(o, rdflib.term.URIRef):
                                    property_dict["reference"] = o.n3().strip("<>")
                            elif "core#broader" in p:
                                property_dict["parent_instance"] = self._get_instance_name(o.n3())
                    self.results[attribute][instance] = property_dict
            else:
                attribute_dict = {}
                attribute_dict["concept_definition"] = concept_definition
                attribute_dict["isproperty"] = self._is_property(attribute[1])
                self.results[attribute] = attribute_dict

    def transform_to_csv(self):
        self._select_attributes()
        self._select_instances()
        self._get_instance_details()
        frames = []
        self.logger.debug(f"{self.results=}")
        for k in self.results.keys():
            if self.results[k].keys():
                for k2 in self.results[k].keys():
                    # check if there are existing instances with corresponding details
                    if isinstance(self.results[k][k2], dict):
                        instance_data = self.results[k][k2]
                        normalized_instance_data = pd.json_normalize(instance_data)
                        normalized_instance_data["instance"] = k2
                        normalized_instance_data["attribute"] = k[0]
                        frames.append(normalized_instance_data)
                    # if there are no instances save only basic informations related to attribute
                    else:
                        attribute_data = self.results[k]
                        normalized_attribute_data = pd.json_normalize(attribute_data)
                        normalized_attribute_data["attribute"] = k[0]
                        frames.append(normalized_attribute_data)
        df = pd.concat(frames)
        df = df.reindex(columns=["attribute", "instance", "parent_instance", "notation", "label", "definition",
                                 "reference", "citation", "isproperty", "concept_definition", "pub_chem", 
                                 "inchi_key", "inchi"])
        df.drop_duplicates(inplace=True)
        df.to_csv(f"{self.output}", index=False)
