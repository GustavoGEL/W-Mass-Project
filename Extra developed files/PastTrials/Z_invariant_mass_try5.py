# Calculation imports
import ROOT
import numpy as np
import os, datetime

# Plotting imports
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.transforms import ScaledTranslation

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                  Notes                                                                  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 1) Just using ROOT to read input data file
#           2) Using numpy to make calculations
#           3) Using matplotlib.pyplot to plot and save the histogram
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                               Reading data                                                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Extra details
# 1) Accounting for the range to account for, so using for histogram with Root: 
# Original: hist = ROOT.TH1F('hist', 'Z⁰ rest mass', 100, 0., 10**7)
# SInce interested in Z mass -> hist = ROOT.TH1F('hist', 'Z⁰ rest mass', 100, (70*10**7), (110*10**7))

# Get data from file
# data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/13TeV__2018__magnet_down_data__Z_candidates.root"

# Taking time to save the taken time of the entire program to run, so that it can be taken into account when calculating again
strt_tm = datetime.datetime.now()

# Get data from file
crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
data_path = crrnt_abs_pth+"/Data/13TeV__2018__magnet_down_data__Z_candidates.root"  # In my computer/local
input_file = ROOT.TFile(data_path)
input_file.ls()

tree = input_file.Get('DecayTree')

# Test gotten data
print("Checking first data point:")
tree.Show(0)
print("All data printed for first data point")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                            Data manipulation                                                            #
# Useful links used:                                                                                                                      #
# [1] Muon rest mass: https://physics.nist.gov/cgi-bin/cuu/Category?view=pdf&Atomic+and+nuclear.x=                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Define constants
m_mu = 105.6583755  # Muon rest mass [MeV/c^2] [1]
m_mu_squared = m_mu*m_mu

expected_Z_mass = 91.5  # [GeV]
e_min, e_max, use_range = 70, 110, True  # [GeV]

"""# Initialise ROOT histogram and define properties
hist = ROOT.TH1F('hist', 'Z⁰ rest mass', 100, 0.7*(10**7), 1.1*(10**7))

hist.fillstyle = 'solid'
hist.fillcolor = 'green'
hist.linecolor = 'green'
hist.linewidth = 0"""

energies_arr, all_rest_mass_arr, errors_arr = [], [], []
range_rest_mass_arr = []

# Limiter for tester and output modes to create summary data and plot files
n_vals, nth_val, testing = 100, 1, False
run_mode = "save and show"  # Modes: "save and show", "save", "show"
out_plot_type = "personal"  # Options: "phys_rev", "personal"  -> eitehr include title, floating text label, etc
tot_vals = 0

# Go through each data point
for entry in tree:
    # Count number or datapoints
    tot_vals += 1

    # # # # # # # # # # # # # # # # # # # # Sorting entry data # # # # # # # # # # # # # # # # # # # # 
    mup_PT = entry.mup_PT
    mup_ETA = entry.mup_ETA
    mup_PHI = entry.mup_PHI
    mum_PT = entry.mum_PT
    mum_ETA = entry.mum_ETA
    mum_PHI = entry.mum_PHI

    """print("First particle:")
    print(f"Transverse momentum (pt): {mup_PT}")
    print(f"Pseudorapidity (eta): {mup_ETA}")
    print(f"Azimuthal angle (phi): {mup_PHI}")

    print("Second particle:")
    print(f"Transverse momentum (pt): {mum_PT}")
    print(f"Pseudorapidity (eta): {mum_ETA}")
    print(f"Azimuthal angle (phi): {mum_PHI}")"""

    # # # # # # # # # # # # # # # # Calculating rest mass of Z_0 boson # # # # # # # # # # # # # # # #
    # Momentum components of positive and negative muons
    p_p_x = mup_PT*np.cos(mup_PHI)
    p_p_y = mup_PT*np.sin(mup_PHI)
    p_p_z = mup_PT*(np.sin(mup_PHI)/np.tan(2*np.arctan(np.exp(-mup_ETA))))

    p_m_x = mum_PT*np.cos(mum_PHI)
    p_m_y = mum_PT*np.sin(mum_PHI)
    p_m_z = mum_PT*(np.sin(mum_PHI)/np.tan(2*np.arctan(np.exp(-mum_ETA))))

    p_p_squared = ((p_p_x)**2)+((p_p_y)**2)+((p_p_z)**2)
    p_m_squared = ((p_m_x)**2)+((p_m_y)**2)+((p_m_z)**2)

    # Total energy of each particle and total energy
    E_p_tot = (p_p_squared+m_mu_squared)**(0.5)
    E_m_tot = (p_m_squared+m_mu_squared)**(0.5)

    E_tot = E_p_tot+E_m_tot  # Assuming p_Z = 0 -> E_tot = m_0_Z

    # Total initial momentum of decaying particle, i.e. conservation of momentum (From ver 3)
    p_tot_x = p_p_x+p_m_x
    p_tot_y = p_p_y+p_m_y
    p_tot_z = p_p_z+p_m_z

    p_tot_squared = (p_tot_x*p_tot_x) + (p_tot_y*p_tot_y) + (p_tot_z*p_tot_z)

    # Rest mass - From ver 3
    Z_rest_mass = ((E_tot*E_tot)-p_tot_squared)**(0.5)

    # Convert from MeV to GeV to have smaller numbers
    E_tot = E_tot/1000
    Z_rest_mass = Z_rest_mass/1000

    # Propagating errors...
    # m_mu_relative_std_uncert = 2.2*((10)**(−8))  # From reference 12

    # Total energy of decay:
    print(f"Total energy (method 4): {E_tot} [GeV]")
    print(f"Rest mass of Z boson (method 3): {Z_rest_mass} [GeV]")
    # print(f"Expecting rest mass of Z boson around: {expected_Z_mass} [MeV]")
    # print(f"Error (%): {100*(Z_rest_mass-expected_Z_mass)/(expected_Z_mass)}")

    # Add values to array
    energies_arr.append(E_tot)
    nth_val += 1

    """# Add values to ROOT histogram
    hist.Fill(E_tot)"""

    # # # # # # # # # # # # # # # # Store all output energies (if needed?) # # # # # # # # # # # # # # # #
    all_rest_mass_arr.append(Z_rest_mass)
    # errors_arr.append((Z_rest_mass-expected_Z_mass)/(expected_Z_mass))
    
    # # # # # # # # # # # # # # Reduce range of energies to improve precision # # # # # # # # # # # # # #
    if use_range:
        if e_min <= Z_rest_mass <= e_max:
            range_rest_mass_arr.append(Z_rest_mass)

    if testing:
        # Break loop or keep adding values
        if nth_val == n_vals:
            break  # Just testing the first value
        else:
            print(f"Calculated: {tot_vals}/{n_vals} -> {round(100*(tot_vals/n_vals), 3)}% done")
            nth_val += 1

# # # # # # # # # # # Convert arrays into numpy arrays to improve efficiency # # # # # # # # # # #
np.asarray(energies_arr)
np.asarray(all_rest_mass_arr)
if use_range:
    np.asarray(range_rest_mass_arr)
    print("Range rest mass:")
    print(range_rest_mass_arr)
    # np.asarray(errors_arr)

    # Calculate mean and standard deviation of energy values
    """data_mean = np.mean(energies_arr)
    data_std = np.std(energies_arr)"""
    # Calculating weighted averaged and std
    """data_mean = np.average(values, weights=weights)
    data_var = np.average((values-data_mean)**2, weights=weights)
    data_std = math.sqrt(data_var)  # Quicker than np.sqrt as this is a float, not an array"""

    data_mean = np.average(range_rest_mass_arr)
    data_std = np.std(range_rest_mass_arr)
else:
    print("All rest masses:")
    print(range_rest_mass_arr)
    data_mean = np.average(all_rest_mass_arr)
    data_std = np.std(all_rest_mass_arr)

print(f"Mean: {data_mean} [GeV]")
print(f"Std: {data_std} [GeV]")

# Plot distribution of masses vs energy 
print(f"Using {tot_vals} values in plot")
print("Setting up histogram")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                          Histogram properties                                                           #
# Useful links used:                                                                                                                      #
# [1] rc properties: https://matplotlib.org/stable/tutorials/introductory/customizing.html                                                #
# [2] Axis usage example: https://towardsdatascience.com/what-are-the-plt-and-ax-in-matplotlib-exactly-d2cf4bf164a9                       #
# [3] Histogram example from: https://matplotlib.org/stable/gallery/pyplots/pyplot_text.html#sphx-glr-gallery-pyplots-pyplot-text-py      #
# [4] Major and minor tick example: https://matplotlib.org/stable/gallery/ticks_and_spines/major_minor_demo.html                          #
# [5] Legend properties: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html                                          #
#                                                                                                                                         #
# Note: Just creating the range plot when using range
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Define histogram constants (using Physical Review Letters standard)
label_font = "Times New Roman"
label_size = 26
tick_font = "Times New Roman"
tick_label_size = 22
legend_size = 20
title_size = 30
general_font_size = 20

n_bins = 100
x_axis_lbl = 'Energy, E (GeV)'
y_axis_lbl = 'Probability'
txt_lbl_1 = f" Mean: {round(data_mean, 3)} [GeV]\nSTD: {round(data_std, 3)} [GeV]"

spine_color = (0/255, 0/255, 0/255)
rgb_x_ticks = (0/255, 0/255, 0/255)
rgb_y_ticks = (0/255, 0/255, 0/255)
minor_x_tick_step = 250
minor_y_tick_step = 0.005

spine_lines_width = 2
tick_width = spine_lines_width
maj_tick_lngth = 8
min_tick_lngth = maj_tick_lngth*0.5

if out_plot_type == "phys_rev":
    fig_all_nam = f"rest_mass_hist_{tot_vals}_all_calculated_phys_rev.png"
    fig_range_nam = f"rest_mass_hist_{tot_vals}_selected_range_phys_rev.png"
    sum_fig_nam = f"rest_mass_hist_{tot_vals}_summary_phys_rev.txt"
    sum_fig_all_dat = f"rest_mass_hist_{tot_vals}_all_calc_dat_phys_rev.txt"
    sum_fig_range_dat = f"rest_mass_hist_{tot_vals}_range_calc_dat_phys_rev.txt"
elif out_plot_type == "personal":
    fig_all_nam = f"rest_mass_hist_{tot_vals}_all_calculated_personal.png"
    fig_range_nam = f"rest_mass_hist_{tot_vals}_selected_range_personal.png"
    sum_fig_nam = f"rest_mass_hist_{tot_vals}_summary_personal.txt"
    sum_fig_all_dat = f"rest_mass_hist_{tot_vals}_all_calc_dat_personal.txt"
    sum_fig_range_dat = f"rest_mass_hist_{tot_vals}_range_calc_dat_personal.txt"
else:
    errLine = f"Check selected type of use for the plot, got: 'out_plot_type={out_plot_type}'"
    raise Exception(errLine)


# Define font sizes in general [1]
plt.rc('font', size=general_font_size)  # controls default text sizes
plt.rc('axes', titlesize=label_size)  # fontsize of the axes title
plt.rc('axes', labelsize=label_size)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=tick_label_size)  # fontsize of the tick labels
plt.rc('ytick', labelsize=tick_label_size)  # fontsize of the tick labels
plt.rc('legend', fontsize=legend_size) # legend fontsize
plt.rc('figure', titlesize=title_size)  # fontsize of the figure title

# Define axis
fig, axes = plt.subplots(1, 1, figsize=(12, 7))  # , figsize=(10,7), dpi=600)  # Define layout, numbers represent: (number of rows, number of columns?)
# ax = plt.subplot(2, 1, 1)  # Layout with order: (nth plot, number of columns, number of rows)
ax = axes  # [0][0]  # Start from 0, so first plot needs to be [0][0]

# Add data and labels text to histogram
if use_range:
    print("Generating histogram with a selected range of energies")
    n_counts, bins, _ = ax.hist(range_rest_mass_arr, bins=n_bins, density=True, facecolor=(0, 1, 1), alpha=0.75, edgecolor='black', label="Rest mass")
else:
    print("Generating histogram with entire range of energies")
    n_counts, bins, _ = ax.hist(all_rest_mass_arr, bins=n_bins, density=True, facecolor=(0, 1, 1), alpha=0.75, edgecolor='black', label="Rest mass")
print(f"Calculated n_counts: {n_counts}")
print(f"Calculated bins: {bins}")
if out_plot_type == "personal":
    ax.set_title(r'$Z^{0}$ rest mass')
ax.set_xlabel(x_axis_lbl)  # , font=label_font, fontsize=label_size)  # Can specifically define
ax.set_ylabel(y_axis_lbl)  # , font=label_font, fontsize=label_size)

# Mean and standard deviation floating label for personal use
if out_plot_type == "personal":
    ax.text(97, 0.035, txt_lbl_1)

# Shift labels and ticks position (if needed)
# ax.xaxis.set_label_coords(1.05, -0.025)  # Move label to particular coordinate
# ax.yaxis.set_label_coords(1.05, 1.025)  # Move label to particular coordinate

# Spine properties
ax.spines['top'].set_color(spine_color)
ax.spines['right'].set_color(spine_color)
ax.spines['bottom'].set_color(spine_color)
ax.spines['left'].set_color(spine_color)

for axis in ['top','bottom','left','right']:  # Set spine thickness
  ax.spines[axis].set_linewidth(spine_lines_width)

# Ticks per spine properties
ax.tick_params(top="on", bottom="on", right="on", left="on")
ax.yaxis.set_ticks_position('both')  # Show both top and bottom ticks
ax.xaxis.set_ticks_position('both')  # Show both right and left ticks
ax.yaxis.set_minor_locator(MultipleLocator(minor_y_tick_step))  # Set y_minor size step
ax.xaxis.set_minor_locator(MultipleLocator(minor_x_tick_step))  # Set x_minor size step

# Axis limits (if needed)
# x_minimum, x_maximum = 0, 7
# y_minimum, y_maximum = 0, 10**8  # Doesn't work properly with log scale, but perfectly with lineal scale

# ax.set_xlim(x_minimum, x_maximum)
# ax.set_ylim(y_minimum, y_maximum)

# Custom tick properties [4]
    # Colour, length and thickness of major ticks
ax.tick_params(axis="x", direction="in", length=maj_tick_lngth, width=tick_width, color=rgb_x_ticks, labelsize=tick_label_size)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax.tick_params(axis="y", direction="in", length=maj_tick_lngth, width=tick_width, color=rgb_y_ticks, labelsize=tick_label_size)  # direction=... w.r.t. spine of plot area

    # Colour, length and thickness of minor ticks
ax.tick_params(which="minor", axis="x", direction="in", length=min_tick_lngth, width=tick_width, labelsize=tick_label_size)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax.tick_params(which="minor", axis="y", direction="in", length=min_tick_lngth, width=tick_width, labelsize=tick_label_size)  # direction=... w.r.t. spine of plot area

    # Rotation, color and size of labels
ax.tick_params(axis="x", labelsize=tick_label_size, labelcolor=rgb_x_ticks)  # Can also use: (..., labelrotation=-60)
ax.tick_params(axis="y", labelsize=tick_label_size, labelcolor=rgb_y_ticks)  # Can also use: (..., labelrotation=20)

"""# Set custom major tick position
from matplotlib.ticker import FixedLocator, FixedFormatter
x_locator = FixedLocator([3, 7, 8.8, 12])
y_locator = FixedLocator([.85, 1.15, 1.28, 1.9])

ax.xaxis.set_major_locator(x_locator)
ax.yaxis.set_major_locator(y_locator)"""

# Add grid lines and "middle" horizontal line at a particular position (if needed)
# ax.grid(axis="x", color=(0, 0, 0), alpha=.3, linewidth=2, linestyle=":")  # Can either change colour from color= or use alpha for transparency
# ax.grid(axis="y", color=(0, 0, 0), alpha=.5, linewidth=2, linestyle=":")  # Vertical gridlines
# ax.axhline(y=10**4, xmin=0, xmax=10, color=(0, 0, 0), linewidth=2)

# Axis scales (default=linear)
# ax.set_yscale('log')  # ,base=2)  # Can define base of log scale
# ax.set_yscale('log')  # ,base=2)  # Can define base of log scale

# Ticks offsetting, apply offset transform to all xticklabels and yticklabels (if needed)
dx_x, dy_x = 0, 0  # Move w.r.t. cartesian plane
offset = ScaledTranslation(dx_x/fig.dpi, dy_x/fig.dpi, scale_trans=fig.dpi_scale_trans)

for label in ax.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

dx_y, dy_y = 0, 0  # Move w.r.t. cartesian plane
offset = ScaledTranslation(dx_y/fig.dpi, dy_y/fig.dpi, scale_trans=fig.dpi_scale_trans)

for label in ax.yaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)

# Legend properties [4]
# ax.legend(bbox_to_anchor=(0.1, 0.1, 0.5, 0.5))  # Show legend, can just use: ax.legend()
# ax.legend(loc="upper left")  # loc can also be: loc='best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center' 
# bbox_to_anchor paramters: (x, y, width, height)
# Can also use: ax.legend(loc="best")

# Save histogram as image and summary data as .txt file
if run_mode == "save and show" or run_mode == "save":
    # Calculate total time taken for program to run
    end_tm = datetime.datetime.now()
    tot_time = end_tm-strt_tm

    # Calculate average value of bins
    avg_bin_vals = []
    for nth_bin in range(len(bins)-1):
        avg_vl = (bins[nth_bin]+bins[nth_bin+1])/2
        avg_bin_vals.append(avg_vl)

    # Save summary data, individual n_bins and count values as .txt file
    if use_range:
        plt.savefig(f"FinalFigures/{fig_range_nam}", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')

        with open(f"FinalFigures/{sum_fig_range_dat}", "w") as fl:
            fl.write(f"Using {tot_vals} values in histogram\n")
            fl.write(f"Mean Z Mass: {data_mean} [GeV]\n")
            fl.write(f"Standard Deviation: {data_std} [GeV]\n")
            fl.write(f"Entire Range of Energies Figure Name: {fig_all_nam}\n")
            fl.write(f"Selected Energy Range Figure Name: {fig_range_nam}\n")
            fl.write(f"Data used/data calculated: {len(range_rest_mass_arr)}/{len(all_rest_mass_arr)} ({round(100*(len(range_rest_mass_arr)/len(all_rest_mass_arr)), 3)}%)\n")
            fl.write(f"Range selected: [{e_min}, {e_max}] [GeV]\n")
            fl.write(f"Total running time: {tot_time}\n")
            fl.write(f"Test: {str(testing)}\n")

            tot_n_counts, tot_mean_bin_vals = len(n_counts), len(avg_bin_vals)
            fl.write(f"n_counts==tot_mean_bin_vals?: {str(tot_n_counts==tot_mean_bin_vals)}\n")
            
            fl.write("Gotten n_count values:\n")
            for ith_count in range(tot_n_counts):
                if ith_count < tot_n_counts-1:
                    fl.write(str(n_counts[ith_count])+",")
                elif ith_count == tot_n_counts-1:
                    fl.write(str(n_counts[ith_count])+"\n")
            fl.write("Gotten avg_bin_vals values:\n")
            for ith_mean_bin in range(tot_mean_bin_vals):
                if ith_mean_bin < tot_mean_bin_vals-1:
                    fl.write(str(avg_bin_vals[ith_mean_bin])+",")
                elif ith_mean_bin == tot_mean_bin_vals-1:
                    fl.write(str(avg_bin_vals[ith_mean_bin])+"\n")
    else:
        plt.savefig(f"FinalFigures/{fig_all_nam}", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')

        with open(f"FinalFigures/{sum_fig_all_dat}", "w") as fl:
            fl.write(f"Using {tot_vals} values in histogram\n")
            fl.write(f"Mean Z Mass: {data_mean} [GeV]\n")
            fl.write(f"Standard Deviation: {data_std} [GeV]\n")
            fl.write(f"Entire Range of Energies Figure Name: {fig_all_nam}\n")
            fl.write(f"Total running time: {tot_time}\n")
            fl.write(f"Test: {str(testing)}\n")

            tot_n_counts, tot_mean_bin_vals = len(n_counts), len(avg_bin_vals)
            fl.write(f"n_counts==tot_mean_bin_vals?: {str(tot_n_counts==tot_mean_bin_vals)}\n")
            
            fl.write("Gotten n_count values:\n")
            for ith_count in range(tot_n_counts):
                if ith_count < tot_n_counts-1:
                    fl.write(str(n_counts[ith_count])+",")
                elif ith_count == tot_n_counts-1:
                    fl.write(str(n_counts[ith_count])+"\n")
            fl.write("Gotten avg_bin_vals values:\n")
            for ith_mean_bin in range(tot_mean_bin_vals):
                if ith_mean_bin < tot_mean_bin_vals-1:
                    fl.write(str(avg_bin_vals[ith_mean_bin])+",")
                elif ith_mean_bin == tot_mean_bin_vals-1:
                    fl.write(str(avg_bin_vals[ith_mean_bin])+"\n")
    print("Done, check output folder: FinalFigures")

# Show histogram
if run_mode == "save and show" or run_mode == "show":
    plt.show()
