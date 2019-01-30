import json
import yaml
import os
import sys
import subprocess
import tempfile
from datetime import datetime

def run_command(full_command):
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc.communicate()
    return proc.returncode


def create_repository(repository, git_context):
    
    print('Updating Repository: {} GIT Context: {}'.format(str(repository), git_context))
    run_command('codefresh add repository {} -c {}'.format(str(repository), git_context))


def create_pipeline(repository, pipeline_file):

    fd, path = tempfile.mkstemp(suffix='.yaml')
    
    try:
        with open(pipeline_file) as f, open(path, 'w') as tmp:
            pipeline = yaml.load(f)

            full_name = '/'.join([str(repository), pipeline['metadata']['name']])

            pipeline['metadata']['project'] = str(repository)
            pipeline['metadata']['name'] = full_name

            yaml.dump(pipeline, tmp)

        # Start Debugging

        # with open(path) as f:
        #     print f.read()

        # End Debugging
 
        with open(path) as f:
            print('Attempting to update Pipeline for Repository: {} Using file: {}'.format(str(repository), pipeline_file))
            if run_command('codefresh get pipeline {}'.format(pipeline['metadata']['name'])) == 1:
                print('Pipeline {} Not Found for Repository: {}'.format(pipeline['metadata']['name'], str(repository)))
                print('Creating...')                
                run_command('codefresh create -f {}'.format(path))
            else:
                print('Pipeline {} Found for Repository: {}'.format(pipeline['metadata']['name'], str(repository)))
                print('Updating...')
                run_command('codefresh replace -f {}'.format(path))

    finally:
        os.remove(path)

def main():

    creator_file_path = os.getenv('CREATOR_FILE_PATH', './codefresh_creator.yaml')

    with open(creator_file_path) as f:
        creator_json = json.dumps(yaml.load(f))
    
    for repository_data in json.loads(creator_json):

        repository = repository_data['repository']
        
        if 'git_context' not in repository_data:
            git_context = 'github'
        else:
            git_context = repository_data['git_context']

        create_repository(repository, git_context)
        
        pipelines = repository_data['pipelines']
        for pipeline_file in pipelines:
            create_pipeline(repository, pipeline_file)


if __name__ == "__main__":
    main()
