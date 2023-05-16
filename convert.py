import yaml
import configparser
import os
import argparse

config = configparser.ConfigParser()
config.read('config.ini')
parser = argparse.ArgumentParser()
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
workflow_dir_path = ".github/workflows"

def read_and_update_workflow():   
    abs_read_file_path = os.path.join(script_dir, f"{workflow_dir_path}/base/base-backup-workflow.yaml")
    
    with open(abs_read_file_path, 'r') as file:
        workflow_json = yaml.safe_load(file)
        workflow_json["on"] = "workflow_dispatch"
        workflow_json["name"] = file_name

        if "env" not in workflow_json:
            workflow_json["env"] = {} 
        
        workflow_json["env"]["workflow_file_name"] = file_name
    
    for key in config["DETAILS"]:
        print(' {} = {}'.format(key,config["DETAILS"][key]))
        workflow_json["env"][key] = config["DETAILS"][key]
    
    return workflow_json



def write_new_workflow_file(workflow_json):
    abs_write_file_path = os.path.join(script_dir, f"{workflow_dir_path}/{file_name}")
    
    # write to file
    with open(abs_write_file_path, 'w') as file:
        yaml.dump(workflow_json, file, sort_keys=False)
    
    # setup github actions output
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f"workflow_file_name={file_name}", file=fh)


file_name = f"{config['DETAILS']['table_name']}.workflow.yaml"
workflow_json = read_and_update_workflow()
write_new_workflow_file(workflow_json)
