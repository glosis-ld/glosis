# Generates WiDoco documentation for the GloSIS ontology modules. It transforms
# meta-data triples into a WiDoco config file and runs the WiDoco jar file.
# Check the README file for full details.
#
# This programme takes as sole argument the ontology module name:
#
# python3 generateDoc.py glosis_main
#
# SPDX-License-Identifier: CC-BY-NC-SA-3.0-IGO 

import os 
import sys
import json
import configparser
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, FOAF, RDFS, OWL

DCT = Namespace("http://purl.org/dc/terms/")
SCHEMA = Namespace("http://schema.org/")

mapPreds = {
    "thisVersionURI": OWL.versionIRI,
    "ontologyRevisionNumber": OWL.versionInfo,
    "ontologyTitle": DCT.title,
    "abstract": DCT.abstract
}

widoco_jar = "/opt/widoco/widoco-1.4.15-jar-with-dependencies.jar"
ont_file = "glosis_main"
templ_file = "template.json"

creators = []
contributors = []

def addCreators(g, config):

    global creators
    
    for s, dc_creator, creator in g.triples((None, DCT.creator, None)):
        for s2, p2, name in g.triples((creator, FOAF.name, None)):
            if (name in creators):
                continue
            else:
                creators.append(name)
                config["authors"] += name + ";"
                auth_uri = ""
                for s3, p3, uri in g.triples((creator, RDFS.seeAlso, None)):
                    auth_uri = uri
                config["authorsURI"] += auth_uri + ";"
                i_name = ""
                i_uri = ""
                for s4, p4, institute in g.triples((creator, SCHEMA.affiliation, None)):
                    for s5, p5, inst_name in g.triples((institute, FOAF.name, None)):
                        i_name = inst_name
                    for s6, p6, inst_uri in g.triples((institute, RDFS.seeAlso, None)):
                        i_uri = inst_uri
                    config["authorsInstitution"] += i_name + ";"
                    config["authorsInstitutionURI"] += i_uri + ";"

    return(config)


def addContributors(g, config):

    global contributors

    for s, dc_contributor, contributor in g.triples((None, DCT.contributor, None)):
        for s2, p2, name in g.triples((contributor, FOAF.name, None)):
            if not (name in contributors):
                contributors.append(name)
                config["contributors"] += name + ";"
                for s3, p3, uri in g.triples((contributor, RDFS.seeAlso, None)):
                    config["contributorsURI"] += uri
                config["contributorsURI"] += ";"
                for s4, p4, institute in g.triples((contributor, SCHEMA.affiliation, None)):
                    for s5, p5, inst_name in g.triples((institute, FOAF.name, None)):
                        config["contributorsInstitution"] += inst_name
                    for s6, p6, inst_uri in g.triples((institute, RDFS.seeAlso, None)):
                        config["contributorsInstitutionURI"] += inst_uri
                config["contributorsInstitution"] += ";"
                config["contributorsInstitutionURI"] += ";"

    return(config)


if __name__ == "__main__":

    if (len(sys.argv) > 1):
        ont_file = sys.argv[1]
    
    config = configparser.ConfigParser()
    config.read('config')
    widoco_jar = config['WiDoco']['jar_path']
    templ_file = config['Template']['dict']

    # Read in template
    file = open(templ_file)
    config = json.load(file)
    file.close()
    
    # Parse ontology file
    g = Graph()
    g.parse("../%s.ttl" % ont_file)
    
    # Ontology namespace
    for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
        config["ontologyNamespaceURI"] = s
    
    # Simple predicates: Title, abstract and similar
    for item in mapPreds.items():
        for s, p, o in g.triples((None, item[1], None)):
            config[item[0]] = o
    
    # Creators
    config = addCreators(g, config)    

    # Contributors
    config = addContributors(g, config)

    # Imported ontologies
    for s, p, ontology in g.triples((None, OWL.imports, None)):
        config["importedOntologyNames"] += ontology + ";"
        config["importedOntologyURIs"] += ontology + ";"
        g_ext = Graph()
        try:
            g_ext.parse(ontology, format="turtle")
            config = addCreators(g_ext, config)    
            config = addContributors(g_ext, config)
        except:
            print("Faild to parse ontology: %s" % ontology)

    # Dump WiDoco config file
    config_file = "%s.config" % ont_file
    textfile = open(config_file, "w")
    
    for key in config:
        a = textfile.write("%s=%s\n" % (key, config[key]))
        print("Outputed key: %s", key)
    
    textfile.close()

    # Execute WiDoco
    os.system("mkdir %s" % ont_file)
    os.system(
        """java -jar %s \
            -ontFile ../%s.ttl \
            -outFolder %s \
            -confFile %s \
            -uniteSections \
            -webVowl \
            -rewriteAll""" % (widoco_jar, ont_file, ont_file, config_file))
    
