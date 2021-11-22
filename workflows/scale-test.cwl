class: Workflow
cwlVersion: v1.0

inputs: {}

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

steps:
  build:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: []
      inputs: {}
      outputs:
        out: stdout
    in: {}
    out: [out]
  scale_test:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: []
      inputs:
        build_input:
          type: string
      outputs:
        out: stdout
    in:
      build_input: build/out
    out: [out]
  collect:
    run:
      class: CommandLineTool
      hints:
        DockerRequirement:
          copyContainer: beeswarm.tar.gz
      baseCommand: []
      inputs:
        scale_test_input:
          type: string
      outputs:
        out: stdout
    in:
      scale_test_input: scale_test/out
    out: [out]
