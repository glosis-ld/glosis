import rdflib
import pandas as pd
import os


def generate_list_off_all_observations(input_files):
    """
    Function that generates list of all observation from list of input files.
    :param input_files: list -> files containing data.
    :return: list -> list with n3 observation representations.
    """
    observations = []
    for file in input_files:
        g = rdflib.Graph()
        g.parse(file, format="ttl")
        for s, p, o in g:
            if "http://www.w3.org/ns/sosa/Observation" in o:
                observations.append(s.n3())
    return observations


def create_list_of_files(folder):
    """
    Function that generates list of input files based on the folder that contains them.
    :param folder: str -> name of the folder that contains input files.
    :return: list -> list with paths to input files.
    """
    files = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        files.append(path)
    return files


def create_csv_list_with_observations(observations, file_name):
    """
    Function that creates csv file with observations.
    :param observations: list -> list with n3 observation representations.
    :param file_name: str -> name for the output csv.
    """
    observations = [x.strip("<>") for x in observations]
    names = [x.split("#")[-1] for x in observations]
    modules = [x.split("#")[0].split("/")[-1] for x in observations]
    input_data = {'observation': names,
                  'module': modules}
    df = pd.DataFrame(data=input_data)
    df.to_csv(file_name, index=True)


if __name__ == '__main__':
    list_of_files = create_list_of_files(folder="observations")
    obs = generate_list_off_all_observations(input_files=list_of_files)
    create_csv_list_with_observations(observations=obs, file_name="observations.csv")
