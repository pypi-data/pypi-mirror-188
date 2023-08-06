import os
import yaml
import re
import subprocess
import os
from collections.abc import Iterable
import sys


def get_dbt_project_status():
    result = subprocess.run(['dbt', 'debug'], capture_output=True, text=True)
    output = result.stdout
    if 'ERROR not found' in output:
        return ('failed', None)
    elif 'All checks passed' in output:
        lines = output.split("\n")
        for line in lines:
            if "Using dbt_project.yml file at" in line:
                path = line.split("dbt_project.yml file at")[1].strip()
                path = os.path.dirname(path)
                if os.path.exists(path):
                    return ('passed', path)
        return ('passed', None)
    else:
        return ('unknown', None)

def find_file_path(model_name,path):
    models_dir = os.path.join(path, "models")
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file == f"{model_name}.sql" or file == model_name:
                return root
    return None



def check_sql_config(file_path):
    with open(file_path, 'r') as sql_file:
        file_content = sql_file.read()
        match = re.search(r"config\s*\((.*)\)", file_content)
        if match:
            config_args = match.group(1)
            match = re.search(r"materialized\s*=\s*'(.*?)'", config_args)
            if match:
                materialized_arg = match.group(1)
                if materialized_arg == "ephemeral":
                    return True
    return False


def check_file_exists(model_name,path):
    models_dir = os.path.join(path, "models")
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file == f"{model_name}.sql" or file == model_name:
                return True
    return False

def find_file(model_name,path):
    models_dir = os.path.join(path, "models")
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file == f"{model_name}.sql" or file == model_name:
                return os.path.join(root, file)
    return None



def yamlgen(model_name,path, version=2):
    model_name = model_name.split('.', 1)[0]
    if check_file_exists(model_name,path):
        model_path = find_file(model_name,path)
        file_path = find_file_path(model_name,path)
        mod_name = {"model_names": [model_name]}
        if not check_sql_config(model_path):
            cmd = "dbt run-operation generate_model_yaml --args '{}'".format(mod_name)
            output = subprocess.check_output(cmd, cwd='.', shell=True)
            output = output.decode("utf-8")
            ver_details = 'version: {}\n'.format(version)
            mod_details = output.split('version: 2')[1]
            file_path = '{}/{}.yml'.format(file_path, model_name)
            with open(file_path, "w") as text_file:
                text_file.write(ver_details + mod_details)
            print("{}.yml has been created in {}".format(model_name, file_path))
        else:
            print("{} is ephemeral, skipping...".format(model_name))
            pass


def generate_yaml_for_models(model_names,path, version=2):
    for model_name in model_names:
        yamlgen(model_name,path, version)

def get_sql_list(folder):
    list_sql = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".sql"):
                list_sql.append(file)
                
    return list_sql


                                  