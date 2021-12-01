class: Workflow
cwlVersion: v1.0

inputs:
  build_script:
    type: string
  scale_script:
    type: string
  scale_args: # Arguments to the scaling script
    type: string
  collect_script:
    type: string

outputs:
  build_out:
    type: string
    outputSource: build/out
  scale_test_out:
    type: string
    outputSource: scale_test/out
  collect_out:
    type: string
    outputSource: collect/out

# TODO: Need to use input parameters as arguments
steps:
  build:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: [ls, /]
      inputs:
        build_script:
          type: string
          inputBinding:
            position: 1
      outputs:
        out:
          type: string
    in:
      build_script: build_script
    out: [out]
  scale_test:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: [/opt/run.sh]
      inputs:
        scale_script:
          type: string
          inputBinding:
            position: 1
        scale_args:
          type: string
          inputBinding:
            position: 2
        build_input:
          type: string
          default: ""
          inputBinding:
            position: 3
      outputs:
        out:
          type: File
    in:
      build_input: build/out
      scale_args: scale_args
      scale_script: scale_script
    out: [out]
  collect:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: [ls, /]
      inputs:
        collect_script:
          type: string
          inputBinding:
            position: 1
        scale_test_input:
          type: string
          default: ""
          inputBinding:
            position: 2
      outputs:
        out:
          type: File
    in:
      scale_test_input: scale_test/out
      collect_script: collect_script
    out: [out]
