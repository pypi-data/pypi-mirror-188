#!/usr/bin/env python
# coding: utf-8


# automated version with user prompt
import os
import argparse
import yaml
import re
import subprocess
import os
from collections.abc import Iterable
import sys
from yamdgen.yaml_helpers_function import *
from yamdgen.md_helpers_function import *
                  
                            
def main_yaml():
    result,path = get_dbt_project_status()
    parser = argparse.ArgumentParser(description='Check if the argument is a path or a list \n')
    parser.add_argument('input', type=str, help='Path or list of values \n')

    args = parser.parse_args()

    if os.path.exists(args.input):
        list_sql = get_sql_list(args.input)
        if result == "passed":
            print("running yaml generator using dbt_project.yml in {}/dbt_project.yml...........\n".format(path))
            generate_yaml_for_models(list_sql,path)
        else:
            print("Error: Please go into a dbt project as a dbt_project.yml file could not be found in the current directory. \n")               
    else:
        try:
            values = eval(args.input)
            if isinstance(values, list):
                if result == "passed":
                    print("running yaml generator using dbt_project.yml in {}/dbt_project.yml........... \n".format(path))
                    generate_yaml_for_models(values,path)
                else:
                    print("Error: Please go into a dbt project as a dbt_project.yml file could not be found in the current directory. \n")                     
            else:
                print(f"The argument is neither a path nor a list \n")
        except:
            print(f"The argument is neither a path nor a list \n")

def main_md():
    result,_ = get_dbt_project_status()
    parser = argparse.ArgumentParser(description='Check if the argument is a path or a list \n')
    parser.add_argument('input', type=str, help='Path or list of values \n')

    args = parser.parse_args()

    if os.path.exists(args.input):
        list_sql = get_sql_list(args.input)
        if result == "passed":
            print("running md generator........... \n")
            generate_md_for_models(list_sql)
    else:
        try:
            values = eval(args.input)
            if isinstance(values, list):
                if result == "passed":
                    print("running md generator........... \n")
                    generate_md_for_models(values)
            else:
                print(f"The argument is neither a path nor a list \n")
        except:
            print(f"The argument is neither a path nor a list \n")

if __name__ == "__main__":
    main_yaml()
    main_md()
                