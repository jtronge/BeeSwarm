cwlVersion: v1.0
class: Workflow

requirements: {}
inputs:
  build_script:
    type: string
  # Version indicating the version of the code to run
  version:
    type: string
  code_tarball:
    type: string
  out_file:
    type: string
  args:
    type: string

outputs:
  code_tarball:
    type: string
    outputSource: build/code_tarball
  scale_results:
    type: string
    outputSource: save_results/scale_output

steps:
  # TODO: This could be better done with the builder code
  # Build a small container to launch
  build:
    run:
      class: CommandLineTool
      requirements:
        DockerRequirement:
          dockerImageId: beeswarm
      inputs:
        version:
          type: string
        id:
          type: string
      baseCommand: [sh]
      arguments:
        - valueFrom: $(inputs.build_script)
        - valueFrom: $(inputs.version)
      outputs:
        code_tarball:
          type: string
          valueFrom: "code.tar.bz2"
          #streamable: true
          #outputBinding:
          #  glob: "code.tar.bz2"
    in:
      build_script: build_script
      version: version
    out: [code_tarball]
  scale_test:
    run:
      class: CommandLineTool
      requirements:
        DockerRequirement:
          dockerImageId: beeswarm
      inputs:
        code_tarball:
          type: string
        out_file:
          type: string
        args:
          type: string
      baseCommand: [/scripts/scale_test.py]
      arguments:
        - valueFrom: $(inputs.code_tarball)
        - valueFrom: $(inputs.out_file)
        - valueFrom: $(inputs.args)
      outputs:
        output:
          type: string
          default: "out.txt"
    in:
      code_tarball: build/code_tarball
      out_file: out_file
      args: args
    out: [output]
  save_results:
    run:
      class: CommandLineTool
      requirements:
        DockerRequirement:
          dockerImageId: beeswarm
      inputs:
        scale_output:
          type: string
      baseCommand: [/scripts/save_results.sh]
      arguments: []
      outputs:
        final_results:
          type: string
          default: "out.txt"
    in:
      scale_output: scale_test/output
    out: [final_results]
