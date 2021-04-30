import csv
import json

unit_dict = {}
meth_dict = {}

def printObservation(prop, meth, proc_name, units):
    print("""
            glosis_lh:%s%s  a	owl:Class ;
                rdfs:subClassOf  sosa:Observation ;
                rdfs:subClassOf [ a owl:Restriction ; owl:onProperty sosa:hasFeatureOfInterest ; owl:allValuesFrom [owl:unionOf (glosis_lh:GL_Layer glosis_lh:GL_Horizon) ] ] ;
      			rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                            sosa:hasResult ; owl:allValuesFrom glosis_lh:%s%sValue ] ;
      			rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                            sosa:observedProperty ; owl:hasValue glosis_lh:%sProperty ] ;
      		    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                        sosa:usedProcedure ; owl:allValuesFrom glosis_pr:%sProcedure ] .
    """ % (prop, meth, prop, meth, prop, proc_name))
    
    print("""
            glosis_lh:%s%sValue a owl:Class ;
                rdfs:subClassOf  qudt:QuantityValue ;
                rdfs:subClassOf [ a owl:Restriction ; owl:onProperty qudt:numericValue ; owl:allValuesFrom xsd:float ] ;
                rdfs:subClassOf [ a owl:Restriction ; owl:onProperty qudt:unit ;
                owl:hasValue unit:%s ] .
            """ % (prop, meth, units))

def printProperty(prop):
    print("""
            glosis_lh:%sProperty a sosa:ObservableProperty, qudt:Quantitykind ;
                rdfs:label "%sProperty"@en .
            """ % (prop, prop))


def main():

    last = ""
    csv_file = open('/home/duque004/ISRIC/ProjectsInternal/GSP/DataBaseContents/Procedures.csv')
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    # Read first row
    for row in csv_reader:
     
        meta_meth = row[1]
        prop = row[2]
        units = row[3]
        if (prop != last and prop != "" and units != ""):
    
            method = row[4]
            props = prop.split(" ")
    
            for prp in props:
                print("New property: " + prp)
                #unit_dict["prp"].append("method")  
                if prp in unit_dict:
                    unit_dict[prp].append(units)  
                    meth_dict[prp].append(meta_meth)  
                else:
                    unit_dict[prp] = [units]
                    meth_dict[prp] = [meta_meth]
    
            last = prop
    
#    print(json.dumps(unit_dict, indent=4, sort_keys=True))
#    print(json.dumps(meth_dict, indent=4, sort_keys=True))
#    exit()
    
    for prop in unit_dict:
    
        units = unit_dict[prop][0]
        printProperty(prop)
    
        for meth in meth_dict[prop]:
            if meth == "":
                proc_name = prop.capitalize()
            else:
                proc_name = meth
            printObservation(prop, meth.capitalize(), proc_name, units)



if __name__ == "__main__":
    main()        
