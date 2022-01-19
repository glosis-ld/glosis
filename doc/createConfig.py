import json
from rdflib import Graph, URIRef
from rdflib.namespace import DC, FOAF, RDFS

file = open("template.json")
config = json.load(file)
file.close()

g = Graph()
g.parse("../glosis_main.ttl")

schema_affil = URIRef("http://schema.org/affiliation")

# Creators
for s, dc_creator, creator in g.triples((None, DC.creator, None)):
    for s2, p2, name in g.triples((creator, FOAF.name, None)):
        config["authors"] += name + ";"
    for s3, p3, uri in g.triples((creator, RDFS.seeAlso, None)):
        config["authorsURI"] += uri + ";"
    for s4, p4, institute in g.triples((creator, schema_affil, None)):
        for s5, p5, inst_name in g.triples((institute, FOAF.name, None)):
            config["authorsInstitution"] += inst_name + ";"
        for s6, p6, inst_uri in g.triples((institute, RDFS.seeAlso, None)):
            config["authorsInstitutionURI"] += inst_uri + ";"

# Contributors

# Dump WiDoco config file
textfile = open("glosis_main.config", "w")

for key in config:
    a = textfile.write("%s=%s\n" % (key, config[key]))

textfile.close()

