# yamdgen(Alpha Version)
A Yaml and Markdown file wrapper for dbt codegen for dbt a.k.a yamdgen. Simple library written for automatically generating the yaml and md files needed for dbt models.

## Usage for list of models

```
# run the command below in your cli 

yamlgen "['model_a','model_b','model_c']"

```


## Usage for a directory

```
# run the command below in your cli 

yamlgen fullpath/model_folder

```

# Requirements

The requirements for this package to work as inteneded is to ensure you are in your dbt project folder, as you would when you want to run any dbt command.

# **Important information !!!!**

1. **As this is work in progress it is advisebale to use this when you dont have a yaml and md file yet as this will  overwrite your yaml and md files in your folder.**



