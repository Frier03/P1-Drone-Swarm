import matplotlib.pyplot as plt


x = [1., 1., 1., 1., 2., 2., 3., 4., 5., 6., 6., 6., 6., 6., 5., 5., 4., 3., 2., 1.]
y = [5., 5., 5., 4., 4., 4., 4., 4., 3., 3., 3., 3., 3., 2., 1., 1., 1., 1., 1., 1.]

plt.plot(x, y, 'bo', label="X")
plt.legend()
plt.show()