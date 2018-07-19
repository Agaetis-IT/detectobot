import os
import yaml

with open(os.getenv("DB_CFG_FILE"), 'r') as f:
    try:
        params = yaml.load(f)
    except yaml.YAMLError as e:
        raise e
