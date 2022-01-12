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
    run: nwchem_bin.cwl
    in:
      nw_file: nw_file
    out: [nw_stdout]
    hints:
      DockerRequirement:
        # dockerPull: "{{ container }}"
        dockerPull: "jtronge/nwchem"
      #beeflow:MPIRequirement:
        #  nodes: {{ nodes }}
        #  ntasks: {{ ntasks }}
