# Example/Template of ploting one scatter in a single figure

import matplotlib.pyplot as plt
import numpy as np

# # # # # # # # # # # # # # # # # # # # Generate random data # # # # # # # # # # # # # # # # # # # #
a = [pow(10, i) for i in range(10)]
x_dat = np.random.rand(1, 10)  # Generate 10 random values between 0 and 1
print(f"x data: {x_dat}")
y_dat = np.sin(x_dat)
print(f"y data: {y_dat}")

# # # # # # # # # # # # # # # # # # # # # Plot properties # # # # # # # # # # # # # # # # # # # # #
# Define plot properties for reports/PhysRev plot
label_font = "Times New Roman"
label_size = 26
tick_font = "Times New Roman"
tick_num_size = 24
legend_size = 22
title_size = 30
general_font_size = 22

# Define font sizes in general
plt.rc('font', size=general_font_size)          # controls default text sizes
plt.rc('axes', titlesize=label_size)     # fontsize of the axes title
plt.rc('axes', labelsize=label_size)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=tick_num_size)    # fontsize of the tick labels
plt.rc('ytick', labelsize=tick_num_size)    # fontsize of the tick labels
plt.rc('legend', fontsize=legend_size)    # legend fontsize
plt.rc('figure', titlesize=title_size)  # fontsize of the figure title

# Examples gotten from: https://towardsdatascience.com/what-are-the-plt-and-ax-in-matplotlib-exactly-d2cf4bf164a9
# plt.subplot(111)  # Layout with order: (total number of plots, number of columns, number of rows)
fig, axes = plt.subplots(1, 1, figsize=(10, 7))  # , figsize=(10,7), dpi=600)  # Define layout, numbers represent: (number of rows, number of columns?)
# ax = plt.subplot(2, 1, 1)  # Layout with order: (nth plot, number of columns, number of rows)
ax = axes  # [0][0]  # Start from 0, so first plot needs to be [0][0]

# fig.suptitle('Main title')

# Add data and labels text
line, = ax.plot(a, "o-", color='blue', linewidth=3, label="Random data")  # Can also define the shape

# ax.set_title('Subplot title')
# Examples of using superscripts, fractions and lowerscripts
# ax.set_xlabel(r'This is an expression $e^{\sin(\omega\phi)}$')
# ax.set_xlabel(r'Hertz $(\frac{1}{s})$')
# ax.set_xlabel(r'This is a lowerscript $A_{Some_{other}Index}e^{\sin(\omega\phi)}$')
ax.set_xlabel('x label, letter (units)')  # , font=label_font, fontsize=label_size)  # Can specifically define
ax.set_ylabel('y label, letter (units)')  # , font=label_font, fontsize=label_size)

# Labels and ticks position
# ax.yaxis.tick_right()  # If just want to move the y axis label to the right, set to left by default
ax.xaxis.set_label_coords(1.05, -0.025)  # Move label to particula coordinate
ax.yaxis.set_label_coords(1.05, 1.025)  # Move label to particula coordinate

# Spine properties
# making the top and right spine invisible:
ax.spines['top'].set_color((1, 0, 0))
ax.spines['right'].set_color('none')

for axis in ['top','bottom','left','right']:  # Set spine thickness
  ax.spines[axis].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(3)  # Individually

# Ticks per spine
ax.tick_params(top="on", bottom="on", right="on", left="on")  # Can also use, bottom="off" to turn off

# Setting both minor and major ticks, most info from: https://matplotlib.org/stable/gallery/ticks_and_spines/major_minor_demo.html
# For the minor ticks, use no labels; default NullFormatter.
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

ax.xaxis.set_minor_locator(MultipleLocator(0.25))  # Set minor size step and puts all minors
# ax.yaxis.set_minor_locator(AutoMinorLocator())  # Set minor size step and puts all minors, not working as using log axis

# Axis limits
x_minimum, x_maximum = 0, 7
# y_minimum, y_maximum = 0, 10**8  # Doesn't work properly with log scale, but perfectly with lineal scale

ax.set_xlim(x_minimum, x_maximum)
# ax.set_ylim(y_minimum, y_maximum)

# Ticks direction
ax.tick_params(axis="x", direction="in", labelsize=tick_num_size)  # Major and minor, inside plot area
ax.tick_params(axis="y", direction="inout", labelsize=tick_num_size)  # Major and minor, both in and out

ax.tick_params(which="minor", axis="x", direction="in", labelsize=tick_num_size)
ax.tick_params(which="minor", axis="y", direction="in", labelsize=tick_num_size)

# Custom ticks 
rgb_x_major_ticks = (0/255, 155/255, 155/255)
rgb_y_major_ticks = (255/255, 55/255, 255/255)

    # Colour, length and thickness of ticks
ax.tick_params(axis="x", direction="in", length=16, width=2, color=rgb_x_major_ticks)  # For colour, RGB -> [(255, 0, 255)] -> [(1, 0, 1)]
ax.tick_params(axis="y", direction="in", length=6, width=4, color=rgb_y_major_ticks)

    # Rotation, color and size of labels
ax.tick_params(axis="x", labelsize=18, labelrotation=-60, labelcolor="turquoise")  # Can also use RGB, just as above
ax.tick_params(axis="y", labelsize=12, labelrotation=20, labelcolor="orange")

    # Set custom major tick position
"""from matplotlib.ticker import FixedLocator, FixedFormatter
x_locator = FixedLocator([3, 7, 8.8, 12])
y_locator = FixedLocator([.85, 1.15, 1.28, 1.9])

ax.xaxis.set_major_locator(x_locator)
ax.yaxis.set_major_locator(y_locator)"""

# Add grid lines
ax.grid(axis="x", color=(0, 0, 0), alpha=.3, linewidth=2, linestyle=":")  # Can either change colour from color= or use alpha for transparency
ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)

# X properties
# ax.

# Y properties
ax.set_yscale('log')  # ,base=2)  # Can define base of log scale

# Ticks offsetting, apply offset transform to all xticklabels
from matplotlib.transforms import ScaledTranslation
dx, dy = 20, 20  # Move w.r.t. cartesian plane
offset = ScaledTranslation(dx/fig.dpi, dy/fig.dpi, scale_trans=fig.dpi_scale_trans)

for label in ax.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

# Ticks offsetting, apply offset transform to all yticklabels
from matplotlib.transforms import ScaledTranslation
dx, dy = 20, -20  # Move w.r.t. cartesian plane
offset = ScaledTranslation(dx/fig.dpi, dy/fig.dpi, scale_trans=fig.dpi_scale_trans)

for label in ax.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

# Legend properties, most info at: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
# ax.legend(bbox_to_anchor=(0.1, 0.1, 0.5, 0.5))  # Show legend, can just use: ax.legend()
ax.legend(loc="upper left")  # loc can also be: loc='best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center' 
# bbox_to_anchor paramters: (x, y, width, height)
# Can also use: ax.legend(loc="best")

# Saving and displaying
# plt.savefig(f"Figures/one_plot_alternative_example.png", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')
plt.show()
