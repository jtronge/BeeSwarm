class: CommandLineTool
# baseCommand: [./bin/LINUX64/nwchem, examples/tcepolar/ccsd_polar_small.nw]
baseCommand: [/opt/nwchem/bin/nwchem]
stdout: nwchem_stdout.txt
inputs:
  nw_file:
    type: string?
    inputBinding:
      position: 1
outputs:
  nw_stdout:
    type: stdout
