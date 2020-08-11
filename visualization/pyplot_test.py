import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()

data_x = [1, 2, 3, 4, 5, 6]
data_y = [14, 11, 18, 21, 32, 49]

ax1.plot(data_x, data_y, color='tab:blue')
ax2 = ax1.twinx()

data_y2 = [0.1, 0.3, 0.5, 0.12, 0.50, 0.29]
ax2.set_ylabel('ratio')
ax2.set_ylim([0.0, 1.0])
ax2.plot(data_x, data_y2, color='tab:red')

#fig.tight_layout()
plt.show()

