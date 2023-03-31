import subprocess
import os
import rdflib


class Transformer(object):
    def __init__(self, input_csv, query):
        self.input = input_csv
        self.query = query
        self.temp = "temp.ttl"

    def run(self):
        command = f"pytarql {self.query} {self.input} --quotechar=doublequote --dedup=99000"
        with open(self.temp, 'w', encoding="utf-8", errors="ignore") as f:
            p = subprocess.Popen(command, shell=True, stdout=f)
            p.communicate()

        g = rdflib.Graph()
        g.parse(self.temp, format="turtle")
        g.serialize(destination=self.temp, format="turtle")
        return os.path.abspath(self.temp)
