import yaml
import os

def open_yaml():
    with open(os.getcwd() + "\\resources\\web_elements.yaml") as stream:
        try:
            return yaml.safe_load(stream=stream)
        except yaml.YAMLError as error:
            raise Warning(error)