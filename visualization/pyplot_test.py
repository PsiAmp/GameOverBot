import matplotlib.pyplot as plt

plt.yscale('log')

data_x = [1, 2, 3, 4, 5, 6]
data_y = [14, 11, 18, 21, 32, 49]
lines = plt.plot(data_x, data_y)
plt.draw()
for line in lines:
    line.set_alpha(0.1)
    #line.set_color('#dbdbdb')

data_y = [1, 3, 5, 12, 50, 29]
plt.plot(data_x, data_y)
plt.show()