import os
import re
import sys


def update_version(file_path, new_version):
    regex_pattern = re.compile(r"\d\.\d\.*\d*")
    with open(file_path, 'r') as input:
        with open("temp.ttl", 'w') as output:
            lines = input.readlines()
            for line in lines:
                version_prompts = ("versionInfo", "versionIRI")
                if any(ver in line for ver in version_prompts):
                    target = regex_pattern.findall(line)[0]   # there is only one match
                    new_line = line.replace(target, new_version)
                    output.write(new_line)
                else:
                    output.write(line)
    os.remove(file_path)
    os.rename("temp.ttl", file_path)


if __name__ == "__main__":
    target_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    new_version = sys.argv[1]
    list_of_target_files = os.listdir(target_dir)
    for file in list_of_target_files:
        if file.endswith(".ttl"):
            file_path = os.path.join(target_dir, file)
            update_version(file_path=file_path, new_version=new_version)
