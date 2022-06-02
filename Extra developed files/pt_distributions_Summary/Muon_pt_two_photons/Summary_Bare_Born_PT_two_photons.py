import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches
import numpy as np
import time

def read_summary_file_lines(abs_fl_path):
    """Function that reads initial file with some metadata on plot parameters"""
    print(f"Gotten line_ {abs_fl_path}")
    lbl_arr, case_lbl_arr, mean_arr, err_arr, chi_arr = [], [], [], [], []
    with(open(abs_fl_path, "r")) as fl:
        lines = fl.readlines()
        for ith, line in enumerate(lines):
            if ith == 4:
                axs_lbl_arr = line.strip().replace("\\n", "\n").split("|||||")
            elif ith > 5:  # Omit metadata of file
                arr_line = line.strip().replace('Â±', ', ').split(": ")
                nth_lbl_arr = arr_line[0].split(";;")
                case_lbl_arr.append(nth_lbl_arr[0])
                lbl_arr.append(nth_lbl_arr[1])
                vals_arr = arr_line[1].split(", ")
                mean_arr.append(float(vals_arr[0]))
                err_arr.append(float(vals_arr[1]))
                chi_arr.append(float(vals_arr[2]))
    return axs_lbl_arr, case_lbl_arr, lbl_arr, mean_arr, err_arr, chi_arr
# Initial string from summary text file:

def weighted_avg_std_min_and_max(data_vals, data_weights):
    dat_avg = np.average(data_vals, weights=data_weights)
    dat_var = np.average((data_vals-dat_avg)**2, weights=data_weights)
    dat_min = np.amin(data_vals)
    dat_max = np.amax(data_vals)
    return dat_avg, np.sqrt(dat_var), dat_min, dat_max

def norm_res_arr_avg_min_and_max(norm_res_vals):
    norm_res_avg = np.average(norm_res_vals)
    norm_res_var = np.std(norm_res_vals-norm_res_avg)
    norm_res_min = np.amin(norm_res_vals)
    norm_res_max = np.amax(norm_res_vals)
    return norm_res_avg, norm_res_var, norm_res_min, norm_res_max

sum_fl_abs_dir_pth = r"C:\Users\gusta\Desktop\T2W8\backend\w8-w9_new_plots\Muon_pt_two_photons\InitialData"
sum_fl_nam = r"pt_and_both_photons_all.txt"
sum_fl_abs_pth = sum_fl_abs_dir_pth+"\\"+sum_fl_nam
axs_lbls_arr, nth_cases_lbl_arr, lbls_arr, means_arr, errs_arr, chis_arr = read_summary_file_lines(sum_fl_abs_pth)
print(f"nth_cases_lbl_arr: {nth_cases_lbl_arr}")
print(f"lbls_arr: {lbls_arr}")
print(f"axs_lbls_arr: {axs_lbls_arr}")
print(f"lbls_arr: {lbls_arr}")
print(f"means_arr: {means_arr}")
print(f"errs_arr: {errs_arr}")
print(f"chis_arr: {chis_arr}")

# Invert order of labels and data points, apparently needed
nth_cases_lbl_arr = nth_cases_lbl_arr[::-1]
lbls_arr = lbls_arr[::-1]
means_arr = means_arr[::-1]
errs_arr = errs_arr[::-1]
chis_arr = chis_arr[::-1]

# Parameters order: [herwig, photos, born, reference]
# muon_pt_mass = [80.50583, 80.50734, 80.51036]
# muon_pt_err = [0.02229, 0.02229, 0.02173]
# muon_pt_chi = [8.858657814354698, 8.915012030742584, 10.953005993531724]

ttl_lbl, x_lbl, y_lbl = axs_lbls_arr[0], axs_lbls_arr[1], axs_lbls_arr[2]  # "$P_{T, Bare Muon}+P_{T, Highest Photon}$\nW mass", "Mass (GeV)", "Case"
# plot_levels_lbl = ["Reference using\nHerwig weights", "Reference using\nPhotos weights", "Reference"]
plot_fl_nam = "FinalFigures/Bare_Born_Muon_2_photon_PT"
run_mode = "Report"  # "Summary", "Report"

plt.rcParams["font.family"] = "Times New Roman"
ttl_fnt_size, x_lbl_fnt_size, y_lbl_fnt_size = 30, 25, 25
x_maj_tick_fnt_size, y_maj_tick_fnt_size = 20, 20
x_min_tick_fnt_size, y_min_tick_fnt_size = 15, 15
x_maj_tick_rot, y_maj_tick_rot, x_norm_maj_tick_rot = 0, 30, 60
start_y_val, end_y_val, stepsize = 0, len(lbls_arr), 1
if run_mode == "Summary":
    padding_arr = [0.8, 0.20, 0.20, 0.95, 0, 0]  # [top, bottom, left, right, hspace, wspace]
elif run_mode == "Report":
    padding_arr = [0.9, 0.20, 0.20, 0.95, 0, 0]  # [top, bottom, left, right, hspace, wspace]
x_lbl_shft, y_lbl_shft, x_norm_lbl_shft = 10, 10, 0

# Calculate average mass and its uncertainty
avg_mass, uncert_mass, min_mass, max_mass = weighted_avg_std_min_and_max(means_arr, errs_arr)

# Calculate normalised residuals
norm_res = []
for ith, (nth_mean_mass, nth_mass_err) in enumerate(zip(means_arr, errs_arr)):
    nth_norm_res = (nth_mean_mass-avg_mass)/nth_mass_err
    norm_res.append(nth_norm_res)

avg_norm_res, uncert_norm_res, min_norm_res, max_norm_res = norm_res_arr_avg_min_and_max(norm_res)

"""# Calculate maximum error
diff_min = avg_mass-min_mass
diff_max = max_mass-avg_mass

if diff_max > diff_min:
    uncert_mass = diff_max
else:
    uncert_mass = diff_min"""

rect_mean_left, rect_mean_bottom, rect_mean_width, rect_mean_height = (min_mass, start_y_val-1, max_mass-min_mass, end_y_val+1) # Mean mass range
rect_uncert_left, rect_uncert_bottom, rect_uncert_width, rect_uncert_height = (avg_mass-uncert_mass, start_y_val-1, 2*uncert_mass, end_y_val+1)  # Uncertainty range
range_rect_alpha, range_rect_color, range_rect_lbl = 0.1, '#00FFFF', 'Mean mass range'
range_uncert_rect_alpha, range_uncert_rect_color, range_uncert_rect_lbl = 0.1, '#FF0000', 'Mass Uncertainty'

fig_shape = (10, 8)
pad_between_axis = -3.0
black_color = (0/255, 0/255, 0/255)
major_x_tick_step_1 = 0.03
major_y_tick_step_2 = 1
minor_x_tick_step_2 = major_x_tick_step_1/2
minor_y_tick_step_2 = major_y_tick_step_2

spine_lines_width = 2
tick_width = spine_lines_width
maj_tick_lngth = 8
min_tick_lngth = maj_tick_lngth*0.5

major_norm_res_tick_step = 0.5
minor_norm_res_tick_step = major_norm_res_tick_step/2

print("Starting parameters")
# Final Plots
# fig, axes = plt.subplots(2, 2, figsize=fig_shape, gridspec_kw={'width_ratios': [3, 1], 'height_ratios': [10, 1]})

fig, axes = plt.subplots(1, 2, figsize=fig_shape, gridspec_kw={'width_ratios': [3, 1], 'height_ratios': [1]})
fig.tight_layout(pad=pad_between_axis)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                   Main masses plot                                                  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ax.yaxis.set_ticks(np.arange(start_y_val, end_y_val, stepsize))
# ax1 = axes[0, 0]
ax1 = axes[0]
w_masses = ax1.errorbar(means_arr, range(len(means_arr)), xerr=errs_arr, c='blue', label="W mass", fmt='o')
print("Starting part with parameters")
# time.sleep(5)
# plt.margins(x=0, y=10)
# plt.xlabel("X-axis", labelpad=7)
# labels = [item.get_text() for item in ax1.get_yticklabels()]
labels = [""]
for nth_tick in range(len(lbls_arr)):
    # labels[nth_tick+1] = lbls_arr[nth_tick]"""
    labels.append(lbls_arr[nth_tick])

loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax1.yaxis.set_major_locator(loc)
ax1.set_yticklabels(labels)

print("Starting spine")
# time.sleep(5)
# Spine properties
ax1.spines['top'].set_color(black_color)
ax1.spines['right'].set_color(black_color)
ax1.spines['bottom'].set_color(black_color)
ax1.spines['left'].set_color(black_color)

# Set spine thickness
for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(spine_lines_width)

print("Starting MultipleLocator")
# time.sleep(5)
# Ticks per spine properties
ax1.tick_params(top="on", bottom="on", right="on", left="on")
ax1.yaxis.set_ticks_position('both')  # Show both top and bottom ticks
ax1.xaxis.set_ticks_position('both')  # Show both right and left ticks
ax1.yaxis.set_major_locator(MultipleLocator(major_y_tick_step_2))  # Set y_major size step
ax1.xaxis.set_major_locator(MultipleLocator(major_x_tick_step_1))  # Set x_major size step
ax1.yaxis.set_minor_locator(MultipleLocator(minor_y_tick_step_2))  # Set y_minor size step
ax1.xaxis.set_minor_locator(MultipleLocator(minor_x_tick_step_2))  # Set x_minor size step

ax1.tick_params(axis='x', which='major', labelsize=x_maj_tick_fnt_size, rotation=x_maj_tick_rot)
ax1.tick_params(axis='y', which='major', labelsize=y_maj_tick_fnt_size, rotation=y_maj_tick_rot)

# Colour, length and thickness of major ticks
ax1.tick_params(axis="x", direction="in", length=maj_tick_lngth, width=tick_width, color=black_color, labelsize=x_maj_tick_fnt_size, rotation=x_maj_tick_rot)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax1.tick_params(axis="y", direction="in", length=maj_tick_lngth, width=tick_width, color=black_color, labelsize=y_maj_tick_fnt_size, rotation=y_maj_tick_rot)  # direction=... w.r.t. spine of plot area

# Colour, length and thickness of minor ticks
ax1.tick_params(axis="x", which="minor", direction="in", length=min_tick_lngth, width=tick_width, labelsize=x_min_tick_fnt_size)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax1.tick_params(axis="y", which="minor", direction="in", length=min_tick_lngth, width=tick_width, labelsize=y_min_tick_fnt_size)  # direction=... w.r.t. spine of plot area

# ax.xaxis.set_ticklabels([])  # Hide label of x axis
ax1.xaxis.labelpad = x_lbl_shft
ax1.yaxis.labelpad = y_lbl_shft

ax1.set_ylim([start_y_val-0.5, end_y_val-0.5])
# ax.set_xlim([80, 81])  # Doing
fig.subplots_adjust(top=padding_arr[0], bottom=padding_arr[1], left=padding_arr[2], right=padding_arr[3], hspace=padding_arr[4], wspace=padding_arr[5])

# Draw rectangle to account for error and vertical line to account for mean of all values
# uncert_mean_rect=mpatches.Rectangle((rect_uncert_left,rect_uncert_bottom), rect_uncert_width, rect_uncert_height, alpha=range_uncert_rect_alpha, color=range_uncert_rect_color, label=range_uncert_rect_lbl)
# plt.gca().add_patch(uncert_mean_rect)

# Draw rectangle of uncertainty of W mass
uncert_rect=mpatches.Rectangle((rect_mean_left,rect_mean_bottom), rect_mean_width, rect_mean_height, alpha=range_rect_alpha, color=range_rect_color, label=range_rect_lbl)
# ax1.add_patch(uncert_rect)
ax1.add_patch(uncert_rect)

# Vertical mean line
mean_handle = ax1.vlines(x=[avg_mass], ymin=[rect_mean_bottom], ymax=[rect_mean_height], colors='teal', ls='--', lw=2, label='Mean W mass')

ax1.set_xlabel(x_lbl, fontsize=x_lbl_fnt_size)
ax1.set_ylabel(y_lbl, fontsize=y_lbl_fnt_size)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                  Normalised Residuals                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# ax2 = axes[0, 1]
ax2 = axes[1]
norm_res_diff = ax2.scatter(norm_res, range(len(means_arr)), c='blue', label="Norm res", marker='o')

loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax2.yaxis.set_major_locator(loc)
ax2.set_yticklabels(labels)

loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax2.yaxis.set_major_locator(loc)
ax2.set_yticklabels([])

print("Starting spine")
# time.sleep(5)
# Spine properties
ax2.spines['top'].set_color(black_color)
ax2.spines['right'].set_color(black_color)
ax2.spines['bottom'].set_color(black_color)
ax2.spines['left'].set_color(black_color)

# Set spine thickness
for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(spine_lines_width)

print("Starting MultipleLocator")
# time.sleep(5)
# Ticks per spine properties
ax2.tick_params(top="on", bottom="on", right="on", left="on")
ax2.yaxis.set_ticks_position('both')  # Show both top and bottom ticks
ax2.xaxis.set_ticks_position('both')  # Show both right and left ticks
ax2.yaxis.set_major_locator(MultipleLocator(major_y_tick_step_2))  # Set y_major size step
ax2.xaxis.set_major_locator(MultipleLocator(major_norm_res_tick_step))  # Set x_major size step
ax2.yaxis.set_minor_locator(MultipleLocator(minor_y_tick_step_2))  # Set y_minor size step
ax2.xaxis.set_minor_locator(MultipleLocator(minor_norm_res_tick_step))  # Set x_minor size step

ax2.tick_params(axis='x', which='major', labelsize=x_maj_tick_fnt_size, rotation=x_norm_maj_tick_rot)
ax2.tick_params(axis='y', which='major', labelsize=y_maj_tick_fnt_size, rotation=y_maj_tick_rot)

# Colour, length and thickness of major ticks
ax2.tick_params(axis="x", direction="in", length=maj_tick_lngth, width=tick_width, color=black_color, labelsize=x_maj_tick_fnt_size, rotation=x_norm_maj_tick_rot)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax2.tick_params(axis="y", direction="in", length=maj_tick_lngth, width=tick_width, color=black_color, labelsize=y_maj_tick_fnt_size, rotation=y_maj_tick_rot)  # direction=... w.r.t. spine of plot area

# Colour, length and thickness of minor ticks
ax2.tick_params(axis="x", which="minor", direction="in", length=min_tick_lngth, width=tick_width, labelsize=x_min_tick_fnt_size)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax2.tick_params(axis="y", which="minor", direction="in", length=min_tick_lngth, width=tick_width, labelsize=y_min_tick_fnt_size)  # direction=... w.r.t. spine of plot area

# ax.xaxis.set_ticklabels([])  # Hide label of x axis
ax2.xaxis.labelpad = x_norm_lbl_shft
# ax2.yaxis.labelpad = y_lbl_shft

ax2.set_xlim([min_norm_res-0.3, max_norm_res+0.3])
ax2.set_ylim([start_y_val-0.5, end_y_val-0.5])

ax2.vlines(x=-1, ymin=[rect_mean_bottom], ymax=[rect_mean_height], colors='black', ls='--', lw=2)
ax2.vlines(x=0, ymin=[rect_mean_bottom], ymax=[rect_mean_height], colors='black', ls='--', lw=2)
ax2.vlines(x=1, ymin=[rect_mean_bottom], ymax=[rect_mean_height], colors='black', ls='--', lw=2)

ax2.set_xlabel("Normalised\nResiduals", fontsize=x_lbl_fnt_size)

if run_mode == "Summary":
    # plt.title(ttl_lbl, fontsize=ttl_fnt_size)
    fig.suptitle(ttl_lbl, fontsize=ttl_fnt_size)
    ax1.legend(handles=[w_masses, mean_handle, uncert_rect])  # , uncert_mean_rect])
    out_chi_img_fl_nm = f'{plot_fl_nam}_summary.png'
elif run_mode == "Report":
    # plt.title(" ", fontsize=ttl_fnt_size)
    # fig.suptitle(" ", fontsize=ttl_fnt_size)
    out_chi_img_fl_nm = f'{plot_fl_nam}_report.png'
print("Starting to save")
# time.sleep(5)
plt.savefig(out_chi_img_fl_nm, dpi=300)
print("Done fitting chi-square values and saving plot")

# Save metadata as extra file to use for report
with(open(f"{plot_fl_nam}_metadata.txt", "w")) as fl:
    fl.write(f"{plot_fl_nam}_report.png and {plot_fl_nam}_summary.png\n")
    fl.write("Mean [GeV], uncertainty [GeV], Min mass [GeV], Max mass [GeV]\n")
    fl.write(f"{avg_mass}, {uncert_mass}, {min_mass}, {max_mass}\n")
    fl.write("Average normalised residual, Uncertainty of norm res, minimum normalised residual, maximum normalised residual\n")
    fl.write(f"{avg_norm_res}, {uncert_norm_res}, {min_norm_res}, {max_norm_res}\n")
    for ith, (nth_case_lttr, nth_case_lbl, nth_mean, nth_err, nth_chi, nth_norm_res) in enumerate(zip(nth_cases_lbl_arr, lbls_arr, means_arr, errs_arr, chis_arr, norm_res)):
        nth_str = f"{ith}: '{nth_case_lttr}' as '{nth_case_lbl}', with {nth_mean}\pm{nth_err}, norm residual of '{nth_norm_res}' and chi squared fit of {nth_chi}\n"
        fl.write(nth_str)
