import matplotlib.pyplot as plt

git_hashes = {'abc': 123, 'def': 10, 'ghi': 40}

fig, ax = plt.subplots()
hashes = git_hashes.keys()
times = git_hashes.values()
ax.plot(hashes, times)
ax.set_ylabel('Execution time')

plt.show()
