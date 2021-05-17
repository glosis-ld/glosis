import csv

output = ""
individ_list = ""
individuals = ""

def addClasses(prop, proc, procM, source):

    global output, individ_list, individuals

    output += """
    glosis_pr:%s a skos:ConceptScheme ;
            skos:prefLabel "Code list for %s analysis procedures - codelist scheme"@en;
            rdfs:label "Code list for %s analysis procedures - codelist scheme"@en;
            skos:note "This  code list provides analysis procedures for %s."@en;
            skos:definition "%s" ;
            rdfs:seeAlso glosis_pr:%s .
    """  % (proc, prop, prop, prop, source, procM)
    
    output += """
    glosis_pr:%s a sosa:Procedure;
            rdfs:subClassOf skos:Concept ;
            rdfs:label "Procedures for %s - codelist class"@en;
            rdfs:comment "This code list provides analysis procedures for %s."@en;
            rdfs:seeAlso glosis_pr:%s ;
            owl:oneOf ("""  % (procM, prop, prop, proc)

    output += individ_list + "\n\t\t\t) .\n"

    output += individuals

    individ_list = ""
    individuals = ""



def main():

    global output, individ_list, individuals

    proc_prev = ""
    csv_file = open('/home/duque004/ISRIC/ProjectsInternal/GSP/DataBaseContents/Procedures.csv')
    csv_reader = csv.reader(csv_file, delimiter=',')
    # Bypass header
    next(csv_reader)

    for row in csv_reader:

        method = row[4]
        if (method == "" or method == None):
            continue

        prop = row[1] # meta-property
        if (prop == "" or prop == None):
            prop = row[2]

        proc = prop + "Procedure"
        procM = proc[0].upper() + proc[1:]
        desc = row[5]
        reference = row[6]
        source = row[7]
    
        if (proc_prev != "" and proc != proc_prev):
            addClasses(prop, proc, procM, source)
    
        individ_list += """
                glosis_pr:%s""" % (method)
    
        individuals += """
    glosis_pr:%s a skos:Concept, glosis_pr:%s;
            skos:topConceptOf glosis_pr:%s;
            skos:prefLabel "%s"@en ;
            skos:notation "%s" ;
            skos:definition "%s" ;""" % (method, procM, proc, method, method, desc)
        if (reference != ""):
            individuals += """
            skos:scopeNote <%s> ;""" % (reference)
        individuals += """
            skos:inScheme glosis_pr:%s .
            """ % (proc)
    
        proc_prev = proc

    file = open('procedures.ttl', 'a')
    file.write(output)


if __name__ == "__main__":
    main()
