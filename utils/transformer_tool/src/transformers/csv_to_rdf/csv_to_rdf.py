import subprocess
import sys
import os


class Transformer(object):
    def __init__(self, input_csv, query, output_ttl):
        self.input = input_csv
        self.query = query
        self.output = output_ttl
        self.temp = "temp.ttl"

    def run(self):
        command = f"pytarql {self.query} {self.input} --quotechar=doublequote --dedup=99000"
        with open(self.temp, 'w', encoding="utf-8", errors="ignore") as f:
            p = subprocess.Popen(command, shell=True, stdout=f)
            p.communicate()

        with open(self.temp, 'r', encoding="utf-8") as f:
            x = f.read()
            y = x.replace(".glo", ".\n\nglo")
            with open(self.output, 'w') as o:
                o.write(y)
        os.remove(self.temp)
