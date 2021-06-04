import csv

unit_map = {
    "m3/100m3":"glosis_u:M3-PER-HundredM3",
    "%":"unit:PERCENT",
    "kg/dm3":"unit:KiloGM-PER-DeciM3",
    "cmolc/kg":"unit:CentiMOL-PER-KiloGM",
    "dS/m":"unit:DeciS-PER-M",
    "cm/h":"unit:CentiM-PER-HR",
    "g/kg":"unit:GM-PER-KiloGM",
    "pH":"unit:PH",
    "g/100g":"glosis_u:GM-PER-HectoGM",
    "cmolc/l":"glosis_u:CentiMOL-PER-L"
}

unit_dict = {}
meth_dict = {}

def printObservation(prop, meth, proc_name, units, file):
    file.write("""
            glosis_lh:%s%s  a	owl:Class ;
                rdfs:subClassOf  sosa:Observation ;
                rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                    sosa:hasFeatureOfInterest ; owl:allValuesFrom
                        [owl:unionOf (glosis_lh:GL_Layer glosis_lh:GL_Horizon) ] ] ;
      			rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                    sosa:hasResult ; owl:allValuesFrom glosis_lh:%s%sValue ] ;
      			rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                    sosa:observedProperty ; owl:hasValue glosis_lh:%sProperty ] ;
      		    rdfs:subClassOf [ a owl:Restriction ; owl:onProperty
                    sosa:usedProcedure ; owl:allValuesFrom glosis_pr:%sProcedure ] .
    """ % (prop, meth, prop, meth, prop, proc_name))
    
    file.write("""
            glosis_lh:%s%sValue a owl:Class ;
                rdfs:subClassOf  qudt:QuantityValue ;
                rdfs:subClassOf [ a owl:Restriction ; owl:onProperty qudt:numericValue ; owl:allValuesFrom xsd:float ] ;
                rdfs:subClassOf [ a owl:Restriction ; owl:onProperty qudt:unit ;
                owl:hasValue %s ] .
            """ % (prop, meth, unit_map[units]))

def printProperty(prop, file):
    file.write("""
            glosis_lh:%sProperty a sosa:ObservableProperty, qudt:Quantitykind ;
                rdfs:label "%sProperty"@en .
            """ % (prop, prop))


def main():

    last = ""
    csv_file = open('Procedures.csv')
    csv_reader = csv.reader(csv_file, delimiter=',')
    headers = next(csv_reader)

    # Read first row
    for row in csv_reader:
     
        meta_meth = row[1]
        prop = row[2]
        units = row[3]
        if (prop != last and prop != "" and units != ""):
    
#            method = row[4]
            props = prop.split(" ")
    
            for prp in props:
                if prp == "":
                    continue
                print("New property: " + prp)
                #unit_dict["prp"].append("method")  
                if prp in unit_dict:
                    unit_dict[prp].append(units)  
                    meth_dict[prp].append(meta_meth)  
                else:
                    unit_dict[prp] = [units]
                    meth_dict[prp] = [meta_meth]
    
            last = prop


    file = open('props.ttl', 'w')
    
    for prop in unit_dict:
    
        units = unit_dict[prop][0]
        printProperty(prop, file)
    
        for meth in meth_dict[prop]:
            if meth == "":
                proc_name = prop[0].upper() + prop[1:]
            else:
                meth = meth[0].upper() + meth[1:]
                proc_name = meth
            propCap = prop[0].upper() + prop[1:]
            printObservation(propCap, meth, proc_name, units, file)



if __name__ == "__main__":
    main()        
