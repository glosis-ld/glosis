import os
import re
import logging
import datetime

import rdflib
import pandas as pd

base_uri_mapping = {
    "results": rdflib.term.URIRef(f'http://w3id.org/glosis/model/codelists/results/'),
    "properties": rdflib.term.URIRef(f'http://w3id.org/glosis/model/codelists/properties/'),
    "desc_prop": rdflib.term.URIRef(f'http://w3id.org/glosis/model/codelists/descriptive/'),
    "desc_pch": rdflib.term.URIRef(f'http://w3id.org/glosis/model/codelists/physiochemical/'),
    "procedure": rdflib.term.URIRef(f'http://w3id.org/glosis/model/procedure/')
}


class Transformer(object):
    def __init__(self, file, file_type, output_filename=None):
        self.filename = file
        self.graph = self._parse_into_graph()
        self.file_type = file_type
        self.collections = []
        self.results = {}
        self.base_uri = base_uri_mapping.get(self.file_type)
        self.output = output_filename if output_filename else os.path.splitext(file)[0]

        # setting up logger
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.DEBUG)
        # self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        # current_date = datetime.datetime.now()
        # self.log_path = os.path.join('logs',
        #                              f'rdf_to_csv_{current_date.year}-{current_date.month}-{current_date.day}.log')
        # self.file_handler = logging.FileHandler(self.log_path)
        # self.file_handler.setFormatter(self.formatter)
        # self.logger.addHandler(self.file_handler)

    def _parse_into_graph(self):
        g = rdflib.Graph()
        try:
            g.parse(self.filename, format="ttl")
            return g
        except FileNotFoundError:
            print("File not found, please double-check the path that you provided!")
            return

    def _get_coll_name(self, collection):
        coll_name = re.findall(rf"(?<={self.base_uri}).*(?=ValueCollection|PropertyCollection|ProcedureCollection)", collection)[-1]
        postfix = re.findall(r"ValueCollection|PropertyCollection|Procedure", collection)[-1]
        postfixes = {"Procedure": "Procedure", "ValueCollection": "ValueCode", "PropertyCollection": "PropertyCode"}
        postfix_adjusted = postfixes.get(postfix)
        return coll_name, postfix_adjusted

    def _get_instance_name(self, instance):
        return re.findall(r"(?:(?<=ValueCode\-)|(?<=PropertyCode\-)|(?<=Procedure\-)).*(?=>)", instance)[-1]

    def _select_collections(self):
        collection = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#Collection')
        for s, p, o in self.graph:
            if o == collection:
                self.collections.append(self._get_coll_name(collection=s.n3()))

    def _select_instances(self):
        concept = rdflib.term.URIRef('http://www.w3.org/2004/02/skos/core#Concept')
        ns_type = rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        for collection in self.collections:
            #self.logger.debug(f"{collection=}")
            current_instances = []
            for s, p, o in self.graph:
                if o == concept and p == ns_type:
                    #self.logger.debug(f"{s=}")
                    collection_name = collection[0]
                    camel = collection_name[0].lower() + collection_name[1:]
                    #self.logger.debug(f"{camel=}")
                    patterns = [
                        f"{camel}ValueCode",
                        f"{camel}PropertyCode",
                        f"{camel}Procedure"
                    ]
                    if any(pattern in str(s) for pattern in patterns):
                        #self.logger.debug(f"MATCH: {s.n3()}")
                        instance_value = self._get_instance_name(instance=s.n3())
                        current_instances.append(instance_value)
            #self.logger.debug("-----------=========--------------")
            self.results.update({collection: dict.fromkeys(current_instances, {})})

    @staticmethod
    def _map_foi(foi_val):
        if "GL_Profile" in foi_val:
            return "Profile"
        elif "GL_Horizon" in foi_val:
            return "Layer-Horizon"
        elif "GL_Plot" in foi_val:
            return "Plot-Site"
        elif "GL_Surface" in foi_val:
            return "Surface"
        else:
            return None

    def _get_instance_details(self):
        for collection, values in self.results.items():
            collection_definition = None
            if not self.file_type == "procedure":
                coll_uri = self.base_uri + collection[0] + collection[1]
                for s, p, o in self.graph:
                    if s == coll_uri and p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#definition"):
                        collection_definition = o.n3().strip('"')
            if not values:
                # no instances case
                collection_dict = {}
                collection_dict["collection_definition"] = collection_definition
                self.results[collection] = collection_dict
            else:
                #self.logger.debug(f"{self.results[collection]=}")
                for instance in values:
                    #self.logger.debug(f"{instance=}")
                    property_dict = {}
                    property_dict["collection_definition"] = collection_definition
                    camel = collection[0][0].lower() + collection[0][1:]
                    instance_phrase = f"{camel}{collection[1]}-{instance}"
                    # self.logger.debug(f"{collection[0]=}")
                    # self.logger.debug(f"{collection[1]=}")
                    #self.logger.debug(f"{instance_phrase=}")
                    instance_uri = self.base_uri + instance_phrase
                    #self.logger.debug(f"{instance_uri=}")
                    for s, p, o in self.graph:
                        # self.logger.debug(f"{s=}")
                        # self.logger.debug(f"{instance_uri=}")
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
                            elif p == rdflib.URIRef("http://www.w3.org/ns/ssn/isPropertyOf"):
                                mapped_value = self._map_foi(o.n3())
                                #self.logger.debug(f"{mapped_value=}")
                                if mapped_value:
                                    property_dict.setdefault("foi", []).append(mapped_value)
                            elif "scopeNote" in p:
                                if isinstance(o, rdflib.term.Literal):
                                    property_dict["citation"] = o.n3().strip('"')
                                elif isinstance(o, rdflib.term.URIRef):
                                    property_dict["reference"] = o.n3().strip("<>")
                            elif "core#broader" in p:
                                property_dict["parent_concept"] = self._get_instance_name(o.n3())
                    # self.logger.debug(f"{property_dict=}")
                    self.results[collection][instance] = property_dict

    def transform_to_csv(self):
        self._select_collections()
        self._select_instances()
        # self.logger.debug(f"{self.results=}")
        self._get_instance_details()
        frames = []
        # commented out, used only locally for debugging purposes
        # self.logger.debug(f"{self.results=}")
        for k in self.results.keys():
            if self.results[k].keys():
                for k2 in self.results[k].keys():
                    # check if there are existing instances with corresponding details
                    if isinstance(self.results[k][k2], dict):
                        instance_data = self.results[k][k2]
                        normalized_instance_data = pd.json_normalize(instance_data)
                        normalized_instance_data["concept"] = k2
                        normalized_instance_data["collection"] = k[0]
                        frames.append(normalized_instance_data)
                    # if there are no instances save only basic information related to collection
                    else:
                        attribute_data = self.results[k]
                        normalized_attribute_data = pd.json_normalize(attribute_data)
                        normalized_attribute_data["collection"] = k[0]
                        frames.append(normalized_attribute_data)
        #self.logger.debug(frames)
        df = pd.concat(frames)
        #self.logger.debug(f"{df=}")
        if self.file_type == "properties":
            df = df.explode('foi')
            df = df.reindex(columns=["foi", "collection", "concept", "parent_concept", "notation", "label", "definition",
                                     "reference", "citation", "collection_definition", "pub_chem",
                                     "inchi_key", "inchi"])
        else:
            df = df.reindex(columns=["collection", "concept", "parent_concept", "notation", "label", "definition",
                                     "reference", "citation", "collection_definition", "pub_chem",
                                     "inchi_key", "inchi"])
        df.drop_duplicates(inplace=True)
        df["collection"] = df["collection"].apply(
            lambda x: x[0].lower() + x[1:] if x else x
        )
        df.to_csv(f"{self.output}", index=False)
