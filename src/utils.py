import yaml
import os

def load_credentials(path: str) -> list:

    with open(path, 'r') as file:
        credentials = yaml.safe_load(file)

    for key, value in credentials.items():
        os.environ[key] = value

    return list(credentials.keys())