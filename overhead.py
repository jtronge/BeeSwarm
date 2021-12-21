"""Calculate overhead times for the BeeSwarm log file."""

fnames = [
    'results/lulesh-openmp/time-log-lulesh-openmp.log',
    'results/comd-2021-12-21/time-log-comd-run-2.log',
]

for fname in fnames:
    with open(fname) as fp:
        lines = [line.strip() for line in fp]
    lines = [tuple(line.split(':')) for line in lines if line]
    lines = [(float(line[0]), line[1]) for line in lines]
    # print(lines)
    # Determin major timing data
    bee_init_start = None
    bee_init_end = None
    bee_shutdown_start = None
    bee_shutdown_end = None
    for line in lines:
        if line[1] == 'bee_init_start':
            bee_init_start = line[0]
        if line[1] == 'bee_init_end':
            bee_init_end = line[0]
        if line[1] == 'bee_shutdown_start':
            bee_shutdown_start = line[0]
        if line[1] == 'bee_shutdown_end':
            bee_shutdown_end = line[0]
    # Find all the scale test data
    scale_data = [line[1].split('|') for line in lines]
    scale_tests = set(d[1] for d in scale_data if len(d) == 2)
    test_data = {}
    for line in lines:
        line_data = line[1].split('|')
        if len(line_data) != 2:
            continue
        test = line_data[1]
        keys = [
            'scale_test_start',
            'scale_test_end',
            'scale_test_container_build_start',
            'scale_test_container_build_end',
        ]
        if test not in test_data:
            test_data[test] = {k: None for k in keys}
        for k in keys:
            if line_data[0] == k:
                test_data[test][k] = line[0]
    scale_test_times = [
        (test, test_data[test]['scale_test_end']
               - test_data[test]['scale_test_start'])
        for test in test_data
    ]
    container_test_times = [
        (test, test_data[test]['scale_test_container_build_end']
               - test_data[test]['scale_test_container_build_start'])
        for test in test_data
    ]
    print('------------------------------------------------------------------')
    print(fname)
    print('Average scale test time:', sum(test[1] for test in scale_test_times)
                                      / len(scale_test_times))
    print('Average container build time:', sum(test[1] for test in container_test_times)
                                           / len(container_test_times))
    print('BEE init time:', float(bee_init_end) - float(bee_init_start))
    print('BEE shutdown time:', float(bee_shutdown_end) - float(bee_shutdown_start))
    print('Total time:', float(lines[-1][0]) - float(lines[0][0]))
