cwlVersion: v1.0
class: Workflow

requirements: {}
inputs:
  # Version indicating the version of the code to run
  version:
    type: string
#  build_script:
#    type: File
#    default:
#      class: File
#      location: ../scripts/build_script.py
#  scale_script:
#    type: File
#    default:
#      class: File
#      location: ../scripts/scale_test.py
#  # Arguments to the binary to run
#  bin_args:
#    type: string

# outputs: []
outputs:
  code_tarball:
    type: File
    outputSource: build/code_tarball
  scale_results:
    type: File
    outputSource: build/scale_results

steps:
  # TODO: This could be better done with the builder code
  # Build a small container to launch
  build:
    run:
      class: CommandLineTool
      requirements:
        #InitialWorkDirRequirement:
        #  listing:
        #    - entryname: build_script.py
        #      entry: $(inputs.build_script)
        DockerRequirement:
          dockerImageId: beeswarm
      inputs:
        version:
          type: string
        build_script:
          type: File
      baseCommand: [/scripts/build_script.py]
      arguments:
        - valueFrom: $(inputs.version)
          prefix: --version
      outputs:
        code_tarball:
          type: File
          streamable: true
          outputBinding:
            glob: "code.tar.bz2"
    in:
      version: version
      build_script: build_script
    out: [code_tarball]
  scale_test:
    run:
      class: CommandLineTool
      requirements:
        #InitialWorkDirRequirement:
        #  listing:
        #    - entryname: scale_test.py
        #      entry: $(inputs.scale_script)
        DockerRequirement:
          dockerImageId: beeswarm
      inputs:
        code_tarball:
          type: File
        #scale_script:
        #  type: File
      baseCommand: [/scripts/scale_test.py]
      arguments:
        - valueFrom: $(inputs.code_tarball.path)
          prefix: --tarball
        #- valueFrom: $(inputs.bin_args)
        #  prefix: --bin
      outputs:
        results:
          type: File
          streamable: true
          outputBinding:
            glob: "scale_result.json"
    in:
      code_tarball: build/code_tarball
      #bin_args: bin_args
      scale_script: scale_script
    out: [results]
