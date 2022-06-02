import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches
import numpy as np
import time

# Parameters order: [herwig, photos, born, reference]
bare_muon_pt_mass = [80.79178, 80.79318, 80.79506]
bare_muon_pt_err = [0.04481, 0.04535, 0.04358]
bare_muon_pt_chi = [0.5808974081548854, 0.571649164271761, 0.6260217355829164]

ttl_lbl, x_lbl, y_lbl = "$P_{T, Bare(Data)/Born(Model)Muon}$\n+$P_{T, Both Photons}$ W mass", "Mass (GeV)", "Case"
plot_levels_lbl = ["Reference using\nHerwig weights", "Reference using\nPhotos weights", "Reference"]
plot_fl_nam = "Bare_Born_Muon_PT_2_photons"
run_mode = "Summary"  # "Summary", "Report"

plt.rcParams["font.family"] = "Times New Roman"
ttl_fnt_size, x_lbl_fnt_size, y_lbl_fnt_size = 30, 25, 25
x_maj_tick_fnt_size, y_maj_tick_fnt_size = 12, 12
x_min_tick_fnt_size, y_min_tick_fnt_size = 5, 5
x_maj_tick_rot, y_maj_tick_rot = 0, 30
start_y_val, end_y_val, stepsize = 0, len(plot_levels_lbl), 1
if run_mode == "Summary":
    padding_arr = [0.8, 0.15, 0.25, 0.95, 0.2, 0.2]  # [top, bottom, left, right, hspace, wspace]
elif run_mode == "Report":
    padding_arr = [0.9, 0.15, 0.25, 0.95, 0.2, 0.2]  # [top, bottom, left, right, hspace, wspace]
x_lbl_shft, y_lbl_shft = 10, -10

# Calculate average mass and its uncertainty
avg_mass = np.average(bare_muon_pt_mass, weights=bare_muon_pt_err)
min_mass = np.amin(bare_muon_pt_mass)
max_mass = np.amax(bare_muon_pt_mass)
std_mass = np.std(bare_muon_pt_mass)

# Calculate maximum error
diff_min = avg_mass-min_mass
diff_max = max_mass-avg_mass

if diff_max > diff_min:
    uncert_mass = diff_max
else:
    uncert_mass = diff_min

rect_mean_left, rect_mean_bottom, rect_mean_width, rect_mean_height = (min_mass, start_y_val-1, max_mass-min_mass, end_y_val+1) # Mean mass range
rect_uncert_left, rect_uncert_bottom, rect_uncert_width, rect_uncert_height = (avg_mass-uncert_mass, start_y_val-1, 2*uncert_mass, end_y_val+1)  # Uncertainty range
range_rect_alpha, range_rect_color, range_rect_lbl = 0.1, '#00FFFF', 'Mean mass range'
range_uncert_rect_alpha, range_uncert_rect_color, range_uncert_rect_lbl = 0.1, '#FF0000', 'Mass Uncertainty'

black_color = (0/255, 0/255, 0/255)
major_x_tick_step_1 = 0.02
major_y_tick_step_2 = 1
minor_x_tick_step_2 = major_x_tick_step_1/2
minor_y_tick_step_2 = major_y_tick_step_2/2

spine_lines_width = 2
tick_width = spine_lines_width
maj_tick_lngth = 8
min_tick_lngth = maj_tick_lngth*0.5

print("Starting parameters")
# time.sleep(5)
# Final Plots
fig, ax = plt.subplots()
w_masses = plt.errorbar(bare_muon_pt_mass, range(len(bare_muon_pt_mass)), xerr=bare_muon_pt_err, c='blue', label="W mass", fmt='o')
print("Starting part with parameters")
# time.sleep(5)
# plt.margins(x=0, y=10)
# plt.xlabel("X-axis", labelpad=7)
labels = [item.get_text() for item in ax.get_yticklabels()]
for nth_tick in range(len(plot_levels_lbl)):
    labels[nth_tick+1] = plot_levels_lbl[nth_tick]
# ax.yaxis.set_ticks(np.arange(start_y_val, end_y_val, stepsize))
loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax.yaxis.set_major_locator(loc)
ax.set_yticklabels(labels)

print("Starting spine")
# time.sleep(5)
# Spine properties
ax.spines['top'].set_color(black_color)
ax.spines['right'].set_color(black_color)
ax.spines['bottom'].set_color(black_color)
ax.spines['left'].set_color(black_color)

# Set spine thickness
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(spine_lines_width)

print("Starting MultipleLocator")
# time.sleep(5)
# Ticks per spine properties
ax.tick_params(top="on", bottom="on", right="on", left="on")
ax.yaxis.set_ticks_position('both')  # Show both top and bottom ticks
ax.xaxis.set_ticks_position('both')  # Show both right and left ticks
ax.yaxis.set_major_locator(MultipleLocator(major_y_tick_step_2))  # Set y_major size step
ax.xaxis.set_major_locator(MultipleLocator(major_x_tick_step_1))  # Set x_major size step
ax.yaxis.set_minor_locator(MultipleLocator(minor_y_tick_step_2))  # Set y_minor size step
ax.xaxis.set_minor_locator(MultipleLocator(minor_x_tick_step_2))  # Set x_minor size step

ax.tick_params(axis='x', which='major', labelsize=x_maj_tick_fnt_size, rotation=x_maj_tick_rot)
ax.tick_params(axis='y', which='major', labelsize=y_maj_tick_fnt_size, rotation=y_maj_tick_rot)

# Colour, length and thickness of major ticks
ax.tick_params(axis="x", direction="in", length=maj_tick_lngth, width=tick_width, color=black_color, labelsize=x_maj_tick_fnt_size, rotation=x_maj_tick_rot)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax.tick_params(axis="y", direction="in", length=maj_tick_lngth, width=tick_width, color=black_color, labelsize=y_maj_tick_fnt_size, rotation=y_maj_tick_rot)  # direction=... w.r.t. spine of plot area

# Colour, length and thickness of minor ticks
ax.tick_params(axis="x", which="minor", direction="in", length=min_tick_lngth, width=tick_width, labelsize=x_min_tick_fnt_size)  # For RGB colour: [(255, 0, 255)] -> [(1, 0, 1)]
ax.tick_params(axis="y", which="minor", direction="in", length=min_tick_lngth, width=tick_width, labelsize=y_min_tick_fnt_size)  # direction=... w.r.t. spine of plot area

# ax.xaxis.set_ticklabels([])  # Hide label of x axis
ax.xaxis.labelpad = x_lbl_shft
ax.yaxis.labelpad = y_lbl_shft

ax.set_ylim([start_y_val-0.5, end_y_val-0.5])
# ax.set_xlim([80, 81])  # Doing
fig.subplots_adjust(top=padding_arr[0], bottom=padding_arr[1], left=padding_arr[2], right=padding_arr[3], hspace=padding_arr[4], wspace=padding_arr[5])

# Draw rectangle to account for error and vertical line to account for mean of all values
# uncert_mean_rect=mpatches.Rectangle((rect_uncert_left,rect_uncert_bottom), rect_uncert_width, rect_uncert_height, alpha=range_uncert_rect_alpha, color=range_uncert_rect_color, label=range_uncert_rect_lbl)
# plt.gca().add_patch(uncert_mean_rect)

# Draw rectangle of uncertainty of W mass
uncert_rect=mpatches.Rectangle((rect_mean_left,rect_mean_bottom), rect_mean_width, rect_mean_height, alpha=range_rect_alpha, color=range_rect_color, label=range_rect_lbl)
plt.gca().add_patch(uncert_rect)

# Vertical mean line
mean_handle = plt.vlines(x=[avg_mass], ymin=[rect_mean_bottom], ymax=[rect_mean_height], colors='teal', ls='--', lw=2, label='Mean W mass')

plt.xlabel(x_lbl, fontsize=x_lbl_fnt_size)
plt.ylabel(y_lbl, fontsize=y_lbl_fnt_size)

if run_mode == "Summary":
    plt.title(ttl_lbl, fontsize=ttl_fnt_size)
    plt.legend(handles=[w_masses, mean_handle, uncert_rect])  # , uncert_mean_rect])
    out_chi_img_fl_nm = f'{plot_fl_nam}_summary.png'
elif run_mode == "Report":
    plt.title(" ", fontsize=ttl_fnt_size)
    out_chi_img_fl_nm = f'{plot_fl_nam}_report.png'
print("Starting to save")
# time.sleep(5)
plt.savefig(out_chi_img_fl_nm, dpi=300)
print("Done fitting chi-square values and saving plot")

# Save metadata as extra file to use for report
with(open(f"{plot_fl_nam}_metadata.txt", "w")) as fl:
    fl.write(f"{plot_fl_nam}_report.png and {plot_fl_nam}_summary.png\n")
    fl.write("Mean [GeV], uncertainty [GeV]\n")
    fl.write(f"{avg_mass}, {uncert_mass}\n")
