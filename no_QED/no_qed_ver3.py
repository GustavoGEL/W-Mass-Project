#!usr/bin/gnu python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# No QED investigation
# 
# Filling either templates or pseudodata with muon_pt to investigate noQED effects.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT.TMath import BreitWigner as RBW

import os, datetime
import ROOT as r  # Currently not working, getting an error from 2nd command: source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_100 x86_64-centos7-gcc10-opt
import numpy as np
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
# from scipy.stats import chisquare as chisquare

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                          Functions                                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def check_if_create_dir(abs_pth_fl):
    if not os.path.exists(abs_pth_fl):
        full_cmnd_lin = f"mkdir '{abs_pth_fl}'"
        os.system(full_cmnd_lin)
        print(f"Created: {abs_pth_fl}")
    else:
        print("Exists: "+abs_pth_fl)
    return None


def check_if_create_dirs(dirs_in_dir_arr):
    global crrnt_abs_pth
    print(f"Current directory: {crrnt_abs_pth}")
    for dir_itm in dirs_in_dir_arr:
        dir_to_check = crrnt_abs_pth+"/"+dir_itm
        check_if_create_dir(dir_to_check)
    return None


def get_Chi_squared(y_expect, y_data):
    """Function that calculates the Chi squared value of expected values and input values. 
    Gotten from: Measurements and Their Uncertainties (T. Hase)"""
    chisquare_vl = 0
    for i, y_dat in enumerate(y_data):
        if (y_dat > 0) and (y_expect[i] > 0): # Avoiding zero and negative values as histograms show zero counts on some bins
            temp_vl = (y_dat-y_expect[i])
            chisquare_vl += (temp_vl*temp_vl)/y_expect[i]
    return chisquare_vl


def get_reduced_Chi_Squared(y_expect, y_calc, dof):
    """Function that calculates the chi squared value per degree of freedom (i.e. ??^2_??) of the model.
    Where: 
        1) ??^2_??:  chi squared value per degree of freedom
        2) ??: degrees of freedom of the fitted model
    
    Gotten from: Measurements and Their Uncertainties (T. Hase)
        Null hypothesis: sample distribution is well modelled by a proposed parent distribution
        1) ??^2_?? ??? 1 -> Reasonable fit
        2) ??^2_?? << 1 -> Check uncertainties
        3) ??^2_?? > 2 and ?? ??? 10 -> Question null hypothesis
        4) ??^2_?? > 1.5 and approximately 50 ??? ?? ??? 100 -> Question null hypothesis"""
    return (get_Chi_squared(y_expect, y_calc))/dof


# Taking time to save the taken time of the entire program to run, so that it can be taken into account when calculating again
strt_tm = datetime.datetime.now()
print("Program started, taking time")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                         Parameters                                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Input and output paths and files related
crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
dirs_arr = ["scripts", "doc", "plots", "past_trials"]  # Just need the first three, but extra directories just in case
fils_nm_arr = ["run.sh", "main.tex", "metadata_optimal_vals.txt"]  # and: .../scripts/run.sh, .../doc/main.tex
data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/13TeV__W__Pythia__8.186__CT09MCS__0__LHCbDefaultSim09__evts100000__seed0.root"  # Set absolute path of data
# try_1: hyp_masses_arr = [78, 82, 5]  # Used to test program with expected values
# try_2: hyp_masses_arr = [71, 91, 15] # Used to check chi squared dispersion for a large number of hypothesis masses
# try_3: hyp_masses_arr = [31, 131, 21]  # Used to check chi square dispersion for large hypothesis mass ranges -> not parabolic behaviour at those ranges
# try_4: hyp_masses_arr = [71, 91, 11]  # Used to check medium range -> shifted minimum
# try_5: hyp_masses_arr = [75, 85, 11] # Used to check dispersion at ranges of about 10 GeV -> Parabolic, but chi values in scale of 10s
# try_6: hyp_masses_arr = [78, 92, 11] # Used to check dispersion towards higher masses -> Parabolic approximation starts to break down
# try_7: hyp_masses_arr = [78, 82, 9] # Used to check expected value and small range for every 0.5 GeV -> Parabolic holds
hyp_masses_arr = [78, 82, 9]  # Array of: [minimum mass, maximum mass, number of masses in that range], i.e. [79, 83, 5] -> [79, 80, 81, 82, 83]

# Testing parameters
n_vals, testing = 1000, False

# Histogram parameters
energies_arr, rest_mass_arr = [], []
# e_min, e_max, use_range = 0, 120, True  # [GeV]
e_min, e_max, use_range = 30, 50, True  # [GeV]
n_hist_bins = 100
summary_arrs = []

# Define constants
"""# 1) W and Z masses: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.030001
m_W_expect = 80.379  # ?? 0.012  # [GeV/c^2] [1]
m_W_width = 0.012"""

# From previous fit to simulated data (i.e. using curve_fit)
m_W_expect = 80.36010913  # ?? 2.07041274  # [GeV/c^2] [1]
m_W_width = 2.07041274
parms_fit = 2

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                            Sort tree data and output directories                                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Check if all needed directories exist, else create them
check_if_create_dirs(dirs_arr)

# Test input data
input_file = r.TFile(data_path)
input_file.ls()

tree = input_file.Get("MCDecayTree")
# Alternatively...
# ch = r.TChain("MCDecayTree")
# ch.Add(data_path)
# ch.Show(0) # Test

# Test data
print("Checking first data point:")
tree.Show(0)
print("All data printed for first data point")
# quit()

# Create range of energies and hypothesis masses
energ_bin_vls = np.linspace(e_min, e_max, n_hist_bins+1)
hyp_mass_rng = np.linspace(hyp_masses_arr[0], hyp_masses_arr[1], hyp_masses_arr[2])

# Mean energy values of histogram
mean_e_vl = []
for idx_energ in range(1, n_hist_bins+1):
        mean_e_vl.append((energ_bin_vls[idx_energ]+energ_bin_vls[idx_energ-1])*0.5)

# Generate histogram template and dictionaries with all the mean values with their respective line colors
hist_template = r.TH1F('hist_template','P_{T,#mu} distribution', n_hist_bins, e_min, e_max)
hist_dat = hist_template.Clone('data')
hist_optim = hist_template.Clone('optim_fit')

names, masses, color = {}, {}, {}
for ith in range(hyp_masses_arr[2]):
    hyp_mass = hyp_mass_rng[ith]
    names[str(ith)] = f"M_{{hyp}}={hyp_mass}"
    masses[str(ith)] = hyp_mass
    color[str(ith)] = ith+2

# Initiate data histogram and hypothesis histograms
hyp_hists = {}
# hyp_hists['original'] = hist_template.Clone('original')
for name, mass in masses.items():
    hyp_hists[name] = hist_template.Clone(name)

# Split data in two as 'Model' and 'Data'
model_arr, data_arr, chi_square_arr = [], [], []
print("Sorting data and model data...\r", end="")
for i, entry in enumerate(tree):
    # Add even and odd entries condition
    # First just use one, check chi-squared
    # Then check swtichinnnng off QED (born-mu-pt)
    # Compare both results

    # Sort data, already in GeV
    mu_born_PT = entry.born_mu_PT  
    prop_M = entry.prop_M
    mu_PT = entry.mu_PT

    # Split data
    if i%2 == 0:  # Even entry
        # mu_born_PT -> Pseudodata
        # Add values to array to plot optimal fit
        data_arr.append(mu_born_PT)

        # Add values to PT data histogram
        hist_dat.Fill(mu_born_PT)
    else: # Odd entry
        # Mu_Pt -> Model
        # Add values to array to plot optimal fit
        model_arr.append(mu_PT)

        # Calculate new weights and add values to PT model data histogram
        for name, mass in masses.items():
            # w_nth = RBW(mu_PT, masses[name], m_W_width)/RBW(mu_PT, m_W_expect, m_W_width)
            w_nth = RBW(prop_M, masses[name], m_W_width)/RBW(prop_M, m_W_expect, m_W_width)
            hyp_hists[name].Fill(mu_PT, w_nth)

    # Testing update and break
    if testing:
        # Break loop or keep adding values
        if i == n_vals:
            print(f"Calculated: {i}/{n_vals} -> {round(100*(i/n_vals), 3)}% done", )
            break  # Just testing the first value
        else:
            print(f"Calculated: {i}/{n_vals} -> {round(100*(i/n_vals), 3)}% done \r", end="")
print("Done sorting data and model data")
# Doing: Testing entire code, then optimizing to use Root functions instead of previous loop. Then, optimising next parts

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                  Hypothesis mass histogram                                                                  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("Saving hypothesis histograms and data plot...")
# Save hypothesis histograms and data
c = r.TCanvas("c", "c", 1920, 1080)

# Define histogram properties and add histogram to main canvas
hist_dat.SetTitle("P_{T,#mu} distribution")
hist_dat.SetLineWidth(2)
# hist_dat.FillStyle = 'solid'
# Color properties and indexes at: https://root.cern/root/html534/TColor.html
# hist_dat.SetFillColor(1)

hist_dat.GetYaxis().SetTitle("Normalised counts")  # Fraction in label example: "#frac{A}{B}"
hist_dat.GetYaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetYaxis().CenterTitle(1)

hist_dat.GetXaxis().SetTitle("Energy [GeV]")  # Fraction in label example: "#frac{A}{B}", using latex syntax
hist_dat.GetXaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetXaxis().CenterTitle(r.kTRUE)

# Sort energy, data values before normalisation
data_bin_cnts = []
for idx_energ in range(1, n_hist_bins+1):
    data_bin_cnts.append(hist_dat.GetBinContent(idx_energ))

dat_integ_fact = hist_dat.Integral()
hist_dat.Scale(1./dat_integ_fact)
# hist_dat.Draw('HIST' if i == 0 else 'HIST SAME')
hist_dat.SetLineColor(r.kBlack)
hist_dat.Draw('HIST E1')

# Check all hypothesis and add them to the corresponding leyend
legend = r.TLegend(0.78, 0.27, 0.98, 0.44)  # Legend coords: (x_1, y_1, x_2, y_2)
legend.AddEntry(hist_dat, "P_{T,#mu} data", "f")
for name, mass in masses.items():
    # Fill each hypothesis histogram
    print(f"Adding histogram: {name}\r", end="")
    hist_mod_n = hyp_hists[name]
    hist_mod_n.SetLineWidth(2)
    hist_mod_n.FillStyle = 'solid'

    # Add histogram label to legend
    legend.AddEntry(hist_mod_n, f"P_{{T,#mu}}, {names[name]}", "f")

    # Sort energy, model values before normalisation
    model_bin_cnts = []
    for idx_energ in range(1, n_hist_bins+1):
        model_bin_cnts.append(hist_mod_n.GetBinContent(idx_energ))

    # Calculate chi square of fit and add to chi-squared values array
    fit_dofs = len(model_bin_cnts)-parms_fit
    model_chi_square = get_reduced_Chi_Squared(data_bin_cnts, model_bin_cnts, fit_dofs)
    chi_square_arr.append(model_chi_square)

    # Normalise histogram and add to final histogram
    hist_mod_n.Scale(1./hist_mod_n.Integral())
    hist_mod_n.SetLineColor(color[name])
    hist_mod_n.Draw('HIST SAME')
hist_dat.Draw('HIST E1 SAME')  # Draw data again, so that the data points are on top of everything
legend.Draw("same")  # Draw legend with all elements

out_img_fl_nm = f'plots/muPT_{m_W_expect}_{m_W_width}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}.png'
c.Print(out_img_fl_nm)
print("Done saving hypothesis plot")

print(f"Gotten Chi squared values: {chi_square_arr}")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                    Summary data to save                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set variables to use for LaTex/PDF
print("Updating values to save in Latex document...\r", end="")
# Summary line of data used:
abs_plot_fl_nm = f"{crrnt_abs_pth}/{out_img_fl_nm}"
all_quant_str_wrds = f"Number of data points used: {i},\\\\\nmean expected W mass: {m_W_expect} $[GeV/c^{{2}}]$,\\\\\nmean hypothesis masses $[GeV/c^{{2}}]$: [{f'{nth_mass},' for nth_mass in hyp_mass_rng}],\\\\\nmass width: {m_W_width} $[GeV/c^{{2}}]$,\\\\\nchi_square value of hypothesis fit: {model_chi_square}"
sum_str = f"{all_quant_str_wrds}\\\\\n"
sum_str += f"	Absolute path to figure: {abs_plot_fl_nm}\\\\\n"
sum_str += f"	Next lines are the data of the shown histograms (if needed): \\\\\n"
all_quant_str = f"	{i}, {m_W_expect}, {hyp_mass_rng}, {m_W_width}, {model_chi_square}"
sum_str += f"	All quantities: {all_quant_str}\\\\\n"
sum_str += f"	X_energ_vls = {mean_e_vl}\\\\\n"
sum_str += f"	Y_data_bin_cnts = {data_bin_cnts}\\\\\n"
sum_str += f"	Y_model_bin_cnts = {model_bin_cnts}\\\\\n"

summary_arrs.append([sum_str.replace("_", "\\_"), abs_plot_fl_nm, all_quant_str_wrds, abs_plot_fl_nm])
print("Done updating values to save in Latex document")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                            Optimum parameters and chi-square plot                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("Fitting chi-square values and saving plot...\r", end="")
# Scale up values to improve accuracy
chi_square_arr_rng = np.asarray(chi_square_arr)

# Fit chi_squared distribution with parabola to get optimal values
chi_x_vls = np.linspace(hyp_mass_rng[0], hyp_mass_rng[-1], n_hist_bins)
fit_optim_parms = np.polyfit(hyp_mass_rng, chi_square_arr_rng, 2)
fit_vls = np.poly1d(fit_optim_parms)
roots = np.roots(fit_vls)
real_roots = np.unique(roots.real)

# Define uncertainty of masses, i.e. use values at which chi_squared = 1 to calculate spread around root
chi_max_vls_rng = np.ones(len(hyp_mass_rng))
chi_unit_fit_vls = fit_vls-1 # Shift parabola to calculate new roots
chi_unit_roots = np.roots(chi_unit_fit_vls)
real_chi_unit_roots = np.unique(chi_unit_roots.real)

# Calculate differences and calculate uncertainty
roots_difs = []
for ith_root in real_chi_unit_roots:
    roots_difs.append(np.absolute(ith_root-real_roots))
max_diff = np.max(roots_difs)

# Define plot properties and save it
plt.title("$??^{2}$ distribution of fits")
plt.scatter(hyp_mass_rng, chi_square_arr, marker='o', c='red', label="$??^{2}$ values", zorder=1)
plt.scatter(real_chi_unit_roots,fit_vls(real_chi_unit_roots), c='green', label="Mass value limits, $??^{2}$ = 1", zorder=1)
plt.scatter(real_roots,fit_vls(real_roots), c='blue', label="Optimum mass", zorder=1)
plt.plot(chi_x_vls,fit_vls(chi_x_vls), c='black', label="$??^{2}$ parabola fit", zorder=0)
plt.plot(hyp_mass_rng,chi_max_vls_rng, linestyle='--', c='black', label="$??^{2}$ = 1", zorder=0)
plt.xlabel("Hypothesis mass [GeV]")
plt.ylabel("$??^{2}$ value")
plt.legend()
out_chi_img_fl_nm = f'plots/chi_square_fits_muPT_{m_W_expect}_{m_W_width}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}.png'
plt.savefig(out_chi_img_fl_nm, dpi=300)
print("Done fitting chi-square values and saving plot")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                              Data and optimal parameters plot                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("Calculating optimal fit and saving plot...\r", end="")
# Creating optimal fit histogram (Assuming minimum value, so ignoring the rest of values)
# for i, entry in enumerate(data_arr):
for i, entry in enumerate(model_arr):
    w_nth = RBW(entry, real_roots[0], m_W_width)/RBW(entry, m_W_expect, m_W_width)
    hist_optim.Fill(entry, w_nth)

# Resize data counts as already normalised for hypothesis mass fits
hist_dat.Scale(dat_integ_fact)

# Calculate chi-squared value of optimal fit with respect to data
data_bin_cnts, model_bin_cnts = [], []
for idx_energ in range(1, n_hist_bins+1):
    data_bin_cnts.append(hist_dat.GetBinContent(idx_energ))
    model_bin_cnts.append(hist_optim.GetBinContent(idx_energ))

# Calculate chi square of fit and add to chi-squared values array
fit_dofs = len(model_bin_cnts)-parms_fit
optim_model_chi_square = get_reduced_Chi_Squared(data_bin_cnts, model_bin_cnts, fit_dofs)

# Save optimal fit and data in same plot
c = r.TCanvas("c", "c", 1920, 1080)

# Optimal histogram (Using this to define title of hitogram before adding data and optimal fit on top of data)
hist_optim.SetTitle("Optimal W fit")
hist_optim.GetYaxis().SetTitle("Normalised counts")  # Fraction in label example: "#frac{A}{B}"
hist_optim.GetYaxis().SetTitleOffset(1.0)  # Offset the label
hist_optim.GetYaxis().CenterTitle(1)

hist_optim.GetXaxis().SetTitle("Energy [GeV]")  # Fraction in label example: "#frac{A}{B}", using latex syntax
hist_optim.GetXaxis().SetTitleOffset(1.0)  # Offset the label
hist_optim.GetXaxis().CenterTitle(r.kTRUE)
hist_optim.Draw('HIST')

# Define histogram properties and add histogram to main canvas
hist_dat.SetLineWidth(2)
# hist_dat.FillStyle = 'solid'
# Color properties and indexes at: https://root.cern/root/html534/TColor.html
# hist_dat.SetFillColor(1)

hist_dat.Scale(1./dat_integ_fact)
hist_dat.SetLineColor(r.kBlack)
hist_dat.Draw('HIST E1 SAME')

# Optimal histogram parameters
hist_optim.SetLineWidth(2)
# hist_optim.SetLineStyle(2)

hist_optim.Scale(1./hist_optim.Integral())
hist_optim.SetLineColor(r.kBlue)
hist_optim.Draw('HIST SAME')

# Check all hypothesis and add them to the corresponding leyend
legend = r.TLegend(0.78, 0.27, 0.98, 0.44)  # Legend coords: (x_1, y_1, x_2, y_2)
legend.AddEntry(hist_dat, "P_{T,#mu} data", "f")
legend.AddEntry(hist_optim, f"#splitline{{Optimal fit,}}{{M' = {real_roots[0]} GeV}}", "f")
legend.Draw("same")

out_optim_img_fl_nm = f'plots/optimum_muPT_{m_W_expect}_{m_W_width}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}.png'
c.Print(out_optim_img_fl_nm)

# Create a file with all the data needed to recreate the data and optimal fit histograms if needed:
with(open(f"{crrnt_abs_pth}/{dirs_arr[1]}/{fils_nm_arr[2]}", "w")) as fl:
    fl.write("All quantities (Number of data points used, mean expected W mass [GeV/c^2], mean hypothesis masses [GeV/c^2], mass width [GeV/c^2], chi_square value of hypothesis fit):\n")
    fl.write(f"{all_quant_str}\n")
    fl.write(f"Found optimal massses (chi-square roots)[GeV/c^2]:\n{real_roots}\n")
    fl.write(f"Uncertainty [GeV/c^2]: {max_diff}\n")
    fl.write(f"X_energ_vls:\n{mean_e_vl}\n")
    fl.write(f"Y_data_bin_cnts:\n{data_bin_cnts}\n")
    fl.write(f"Y_model_bin_cnts (using the first chi-square root):\n{model_bin_cnts}\n")

# sum_str += f"	All quantities: {all_quant_str}\\\\\n"
# sum_str += f"	X_energ_vls = {mean_e_vl}\\\\\n"
# sum_str += f"	Y_data_bin_cnts = {data_bin_cnts}\\\\\n"
# sum_str += f"	Y_model_bin_cnts = {model_bin_cnts}\\\\\n"

print("Done calculating optimal fit and saving plot")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                      Latex/PDF summary                                                                      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print("Creating Latex,.sh and PDF documents...\r", end="")
# Create Latex script (need to add the new optimal plot)

print("Summary lines:")
start_latex = r"""\documentclass[12pt]{article}

\usepackage{graphicx}% Include figure files
\usepackage{dcolumn}% Align table columns on decimal point

% Use Arial font %
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault} 

% Default margins and paper properties %
\usepackage[a4, portrait, margin=0.6in]{geometry}

\begin{document}
	\title{Hypothesis plots summary} % Force line breaks with \\
	\author{1666957, Gustavo Espinal Lugo}
	\date{\today} % It is always \today, today, %  but any date may be explicitly specified

	\maketitle
	%\tableofcontents
	
	\section*{Plots and corresponding metadata}
"""
end_latex = r"\end{document}"
with(open(f"{crrnt_abs_pth}/{dirs_arr[1]}/{fils_nm_arr[1]}", "w")) as fl:
    fl.write(start_latex)
    for ith in range(len(summary_arrs)):
        sum_arr = summary_arrs[ith]
        fl.write(f"""	{sum_arr[0]}
    Found optimal massses ($\\chi^{2}$ roots): {real_roots} $[GeV/c^{{2}}]$\\\\
    Uncertainty [GeV/c^2]: {max_diff}\\\\

	\\begin{{figure}}[tb]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{sum_arr[1]}}}
		\\caption{{\\small Hypothesis masses {sum_arr[2]}. }}
		\\label{{fig: fig_{ith}}}
	\\end{{figure}}
    Notes: \\\\
    1) Using mu\_born\_PT as pseudodata and  Mu\_Pt as model/hypothesis\\\\
    2) Using {"testing mode" if testing else "full run mode"}\\\\
""")
    fl.write(f"""       \\begin{{figure}}[tb]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{crrnt_abs_pth}/{out_chi_img_fl_nm}}}
		\\caption{{\\small $\\chi^{2}$ of hypothesis masses. }}
		\\label{{fig: fig_chi_square}}
	\\end{{figure}}

    \\begin{{figure}}[tb]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{crrnt_abs_pth}/{out_optim_img_fl_nm}}}
		\\caption{{\\small Data and optimum fit with $\\chi^{2} = {optim_model_chi_square}$. Used the hypothesis mass of {real_roots[0]} $[GeV/c^{{2}}]$. }}
		\\label{{fig: fig_optim_parms}}
	\\end{{figure}}
    
""")
    fl.write(end_latex)  

# Compile LaTex file
print(f"Current abs path: {crrnt_abs_pth}")
print(f"Tex path: {crrnt_abs_pth}/{dirs_arr[1]}/{fils_nm_arr[1]}")
print(f"Sh path: {crrnt_abs_pth}/{dirs_arr[0]}/{fils_nm_arr[0]}")

sh_fl_content = """# Already using commands from .py script, else use:
mkdir -p plots
mkdir -p doc
python3 plot_templates_no_qed.py
pdflatex main.tex"""
with(open(f"{crrnt_abs_pth}/{dirs_arr[0]}/{fils_nm_arr[0]}", "w")) as fl:
    fl.write(sh_fl_content)
# Not using run.sh, already using commands within this script
print("Using command line to compile:")
full_cmnd_lin = f"cd '{crrnt_abs_pth}/{dirs_arr[1]}'; pdflatex '{fils_nm_arr[1]}'"
print(full_cmnd_lin)
os.system(full_cmnd_lin)
print("Done creating documents")

# Show running time
end_tm = datetime.datetime.now()
time_diff = str(end_tm-strt_tm)
print(f"Programm ran for: {time_diff} [s]")
print("Done")
