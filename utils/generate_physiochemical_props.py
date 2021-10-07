import rdflib
import pandas as pd


filename = "glosis_cl.ttl"   # input ontology filename
g = rdflib.Graph()
g.parse(filename, format="ttl")


def _parse_property_name(uri):
    """
    Semi-private helper function for extracting value from URI.
    :param uri: URI object -> input URI.
    :return: str -> value.
    """
    uri = uri.strip("<>")
    value = uri.split('#')[-1]
    return value


def generate_list_of_properties(object_prefix, graph):
    """
    Function that generate list of all properties based on the object prefix.
    :param object_prefix: str -> prefix in order to recognize the object.
    :param graph: Graph instance -> graph.
    :return: list -> list with properties.
    """
    properties = []
    for s, p, o in graph:
        if object_prefix in o and "http://www.w3.org/1999/02/22-rdf-syntax-ns#first" in p:
            properties.append(o.n3())
    return properties


def generate_labels_and_notations(properties, graph):
    """
    Function that generates labels and notations list for each property.
    :param properties: list -> list of input properties.
    :param graph: Graph object -> input graph.
    :return: list, list -> two lists containing respectively: notations and labels.
    """
    notations = []
    labels = []
    for prop in properties:
        for s, p, o in graph:
            if prop == s.n3() and "http://www.w3.org/2004/02/skos/core#notation" in p:
                notations.append(o.n3())
            elif prop == s.n3() and "http://www.w3.org/2004/02/skos/core#prefLabel" in p:
                labels.append(o.n3())
    return notations, labels


def create_csv(properties, labels, notation, file_name):
    """
    Function that creates csv based on the input data.
    :param properties: list -> list of properties.
    :param labels: list -> list of labels.
    :param notation: list -> list of notations.
    :param file_name: str -> name for the output csv.
    """
    properties = list(map(_parse_property_name, properties))
    input_data = {'entity': properties,
                  'label': labels,
                  'notation': notation}
    df = pd.DataFrame(data=input_data)
    df.to_csv(file_name, index=True)


if __name__ == '__main__':
    props = generate_list_of_properties(object_prefix="physioChemicalPropertyCode-", graph=g)
    nots, labs = generate_labels_and_notations(properties=props, graph=g)
    create_csv(properties=props, labels=labs, notation=nots, file_name="PhysioChemical_properties.csv")
