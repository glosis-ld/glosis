import os
import rdflib
import sys


def update_version(file_path, new_version):
    g = rdflib.Graph()
    g2 = rdflib.Graph()
    g.parse(file_path)
    for ns in g.namespaces():
        g2.namespace_manager.bind(ns[0], ns[1])
    for s, p, o in g:
        if "versionInfo" in p:
            version = o.split("/")[-1]
            o = rdflib.term.Literal(o.replace(version, new_version))
        elif "versionIRI" in p:
            version = o.split("/")[-1]
            o = rdflib.term.URIRef(o.replace(version, new_version))
        g2.add((s, p, o))
    return g2


def replace_file(file_path, graph):
    filename = os.path.basename(file_path)
    os.remove(file_path)
    with open(filename, 'w') as f:
        f.write(graph.serialize(format="ttl"))


if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    new_version = sys.argv[1]
    for file in os.listdir(target_dir):
        if file.endswith(".ttl"):
            file_path = os.path.join(target_dir, file)
            graph = update_version(file_path=file_path, new_version=new_version)
            replace_file(file_path=file_path, graph=graph)






