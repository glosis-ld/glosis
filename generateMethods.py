import csv

csv_file = open('pH_Methods.csv')
csv_reader = csv.reader(csv_file, delimiter=',')

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
            owl:oneOf ( 
    """  % (procM, prop, prop, proc)

    output += individ_list + ") ."

    output += individuals

    individ_list = ""
    individuals = ""


proc_prev = ""

for row in csv_reader:

    prop = row[1]
    proc = prop + "Procedure"
    procM = proc[0].upper() + proc[1:]
    method = row[2]
    desc = row[3]
    source = row[4]

    if (proc != proc_prev):
        addClasses(prop, proc, procM, source)

    individ_list += "\t\tglosis_pr:" + method + "\n"

    individuals += """
    glosis_pr:%s a skos:Concept, glosis_pr:%s;
            skos:topConceptOf glosis_pr:%s;
            skos:prefLabel "%s"@en ;
            skos:notation "%s" ;
            skos:definition "%s" ;
            skos:inScheme glosis_pr:%s .
    """  % (method, procM, proc, method, method, desc, proc)

    proc_prev = proc


addClasses(prop, proc, procM, source)

print(output)
