import os
import yaml
import re
import subprocess
import os
from collections.abc import Iterable
import sys
from yamdgen.yaml_helpers_function import *


def create_md_file(model_name):
    model_name  = model_name.split('.', 1)[0]
    if check_file_exists(model_name):
        path = find_file_path(model_name)
        lines = ['{{% docs {} %}}'.format(model_name),
                '## Overview', '###### Resources:',
                '### Unique Key:', '### Partitioned by:',
                '### Contains PII:', '### Sources:',
                '### Granularity:', '### Update Frequency:',
                '### Example Queries:', '{% enddocs %}']
        with open('{}/{}.md'.format(path,model_name), 'w') as file:
            for line in lines:
                file.write(line)
                file.write('\n')
                file.write('\n')
            print("File created: {}.md has been created in {}".format(model_name, path))

def generate_md_for_models(model_names):
    for model_name in model_names:
        create_md_file(model_name)


    
    
    
