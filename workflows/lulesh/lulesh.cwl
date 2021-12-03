class: Workflow
cwlVersion: v1.0

inputs:
  lulesh_args: string

outputs:
  lulesh_stdout:
    type: File
    outputSource: lulesh/lulesh_stdout

steps:
  lulesh:
    run:
      class: CommandLineTool
      baseCommand: [/lulesh2.0]
      stdout: lulesh_stdout.txt
      inputs:
        lulesh_args:
          type: string
          inputBinding:
            position: 1
      outputs:
        lulesh_stdout:
          type: stdout
    in:
      lulesh_args: lulesh_args
    out: [lulesh_stdout]
    hints:
      DockerRequirement:
        dockerPull: "{{ container }}"
