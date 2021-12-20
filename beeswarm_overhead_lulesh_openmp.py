
fname = 'results/lulesh-openmp/time-log-lulesh-openmp.log'
with open(fname) as fp:
    lines = [line.strip() for line in fp]
lines = [tuple(line.split(':')) for line in lines if line]
print(lines)
print('Total time:', float(lines[-1][0]) - float(lines[0][0]))
