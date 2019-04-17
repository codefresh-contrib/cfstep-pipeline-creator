# cfstep-pipeline-creator

Programmatically add repositories and pipelines to Codefresh Account using YAML file.

Store your repositories and pipeline spec files in a separate repository and update them from a single location.

Example `codefresh-creator.yaml`:

``` yaml
-  repository: dustinvanbuskirk/repository-1
   git_context: github
   pipelines:
     - ./pipelines/pipeline-spec1.yaml
     - ./pipelines/pipeline-spec2.yaml
-  repository: dustinvanbuskirk/repository-2
   pipelines:
     - ./pipelines/pipeline-spec2.yaml
```

Using the file above we will create the repository if it does not exist for the Codefresh account and the pipelines for that repository.

This Fresh Step should be integrated in with the repository containing the file above.

``` yaml
version: '1.0'
steps:
  CreatePipelines:
    image: codefresh/cfstep-pipeline-creator:latest
    environment:
      - CREATOR_FILE_PATH='./example/codefresh-creator.yaml'
```

The step above will pick up the codefresh-creator.yaml in the examples folder.

In that file the pipeline's YAML files have been defined according to the repositories layout which is automatically set as the `working_directory` of the script explaining the relative paths.

This will create repositories as needed and keep all pipelines up-to-date with file using replace.
