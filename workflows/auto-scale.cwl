cwlVersion: v1.0
class: Workflow

requirements:
  InlineJavascriptRequirement: {}
inputs:
  version:
    type: string
  build_script:
    type: File
    default:
      class: File
      location: ../scripts/build_script.py

# outputs: []
outputs:
  code_tarball:
    type: File
    outputSource: build/code_tarball

steps:
  # TODO: This could be better done with the builder code
  # Build a small container to launch
  build:
    run:
      class: CommandLineTool
      requirements:
        InitialWorkDirRequirement:
          listing:
            - entryname: build_script.py
              entry: $(inputs.build_script)
      inputs:
        version:
          type: string
        build_script:
          type: File
      baseCommand: [./build_script.py]
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
