# Example/Template of ploting one scatter in a single figure

import matplotlib.pyplot as plt
import numpy as np

# Generate random data
x_dat = np.random.rand(1, 10)  # Generate 10 random values between 0 and 1
print(f"x data: {x_dat}")
y_dat = np.sin(x_dat)
print(f"y data: {y_dat}")

# Define plot properties for personal use plot
"""plt.scatter(x_dat, y_dat)
plt.xlabel("x label [units]")
plt.ylabel("y label [units]")
plt.title("Figure title")
plt.savefig(f"Figures/one_plot_example.png", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')
plt.show()"""


# Define plot properties for reports/PhysRev plot
label_font = "Times New Roman"
label_size = 26
tick_font = "Times New Roman"
tick_num_size = 24
legend_size = 22
title_size = 30
general_font_size = 22

# Plot properties
plt.figure(figsize=(6,4))  # Proportion and size
plt.scatter(x_dat, y_dat)

# Set scale
ax.set_xscale("log")
ax.set_yscale("log")

# X axis
plt.xlabel("x label [units]", labelpad=-30,  ha="left")  # May use the commented part to shift the title label vertically, can use either ha= or horizontalalignment=
# plt.xlabel('title of the xlabel', fontweight='bold', color = 'orange', fontsize='17', horizontalalignment='center')  # Custom Axis title

# Custom X ticks
# plt.xticks(np.arange(0, 1.1, step=0.2))  # Set label locations, i.e. Using a number slightly greater than 1 to get: 0, 0.2, 0.4, 0.6, 0.8, 1.0
# plt.xticks(np.arange(4), ['Tom', 'Charlie', 'Ruhi', 'Someone'])  # Set text labels, no control of positions
plt.xticks([0, 0.5, 13], ['January', 'February', 'March'], rotation=20, ha="center")  # , alignment = ["right", "left", "center"])  # Set text labels and some properties, like the text, rotation and horizontal alignment
# plt.xticks([])  # Disable xticks.

plt.ylabel("y label [units]")

# Set axis limit
plt.xlim(0,20)

# Custom ticks
plt.tick_params(axis='x', colors='red', direction='out', length=13, width=3)

plt.title("Figure title")  # , loc='left') or , loc='right')  # Use either of the commented locations of the title to shift title
# Can also use: , pad=-14)  # This shifts the title downwards

plt.rc('font', size=general_font_size)          # controls default text sizes
plt.rc('axes', titlesize=label_size)     # fontsize of the axes title
plt.rc('axes', labelsize=label_size)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=tick_num_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=tick_num_size)    # fontsize of the tick labels
plt.rc('legend', fontsize=legend_size)    # legend fontsize
plt.rc('figure', titlesize=title_size)  # fontsize of the figure title

# Saving and displaying
# plt.savefig(f"Figures/one_plot_example.png", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')
plt.show()
