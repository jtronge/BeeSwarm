class: Workflow
cwlVersion: v1.0

inputs:
  build_in:
    type: File

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
      baseCommand: [/opt/build.sh]
      inputs:
        build_in:
          type: string
          default: ""
          inputBinding:
            position: 1
      outputs:
        out:
          type: File
    in:
      build_in: build_in
    out: [out]
  scale_test:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: [/opt/run.sh]
      inputs:
        build_input:
          type: string
          default: ""
          inputBinding:
            position: 1
      outputs:
        out:
          type: File
    in:
      build_input: build/out
    out: [out]
  collect:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: [/opt/collect.sh]
      inputs:
        scale_test_input:
          type: string
          default: ""
          inputBinding:
            position: 1
      outputs:
        out:
          type: File
    in:
      scale_test_input: scale_test/out
    out: [out]
