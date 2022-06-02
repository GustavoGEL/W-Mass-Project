# Example from: https://matplotlib.org/stable/gallery/pyplots/pyplot_text.html#sphx-glr-gallery-pyplots-pyplot-text-py
import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

mu, sigma = 100, 15
x_vals = mu + sigma * np.random.randn(10000)

# the histogram of the data
n_bins = 50

fig, axes = plt.subplots(1, 1, figsize=(10, 7))
ax = axes

counts, bins, patches = ax.hist(x_vals, bins=n_bins, density=True, facecolor='blue', alpha=0.75, edgecolor='black')

ax.set_xlabel('Smarts')
ax.set_ylabel('Probability')
ax.set_title('Histogram of IQ')
ax.text(0, 0, r'$\mu=100,\ \sigma=15$')
ax.set_xlim(40, 160)
ax.set_ylim(0, 0.03)
# ax.grid(color='r', linestyle='-', linewidth=2)

# Save/Display figure
plt.savefig(f"Figures/one_hist_example.png", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')
plt.show()
