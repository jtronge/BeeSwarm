class: Workflow
cwlVersion: v1.0

inputs:
  nw_file: string

outputs:
  nw_stdout:
    type: File
    outputSource: nwchem/nw_stdout

steps:
  nwchem:
    run:
      class: CommandLineTool
      # baseCommand: [./bin/LINUX64/nwchem, examples/tcepolar/ccsd_polar_small.nw]
      baseCommand: [/opt/nwchem/bin/nwchem]
      stdout: nwchem_stdout.txt
      inputs:
        nw_file:
          type: string
          inputBinding:
            position: 0
      outputs:
        nw_stdout:
          type: stdout
    in:
      nw_file: nw_file
    out: [nwchem_stdout]
    hints:
      DockerRequirement:
        dockerPull: "{{ container }}"
      beeflow:MPIRequirement:
        nodes: {{ nodes }}
        ntasks: {{ ntasks }}
