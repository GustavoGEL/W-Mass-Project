#!usr/bin/gnu python
from ROOT import gROOT
gROOT.SetBatch(True)
from ROOT.TMath import BreitWigner as RBW

import os, datetime
import ROOT as r
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


def get_Chi_squared(y_data, y_model):
    """Function that calculates the Chi squared value of expected values and input values. 
    Gotten from: Measurements and Their Uncertainties (T. Hase)"""
    chisquare_vl = 0
    for i, y_dat in enumerate(y_data):
        if (y_dat > 0) and (y_model[i] > 0): # Avoiding zero and negative values as histograms show zero counts on some bins
        # if y_dat > 0:
            temp_vl = (y_dat-y_model[i])
            chisquare_vl += (temp_vl*temp_vl)/(y_dat+y_model[i])  # Assuming data and templates are unweighted
    return chisquare_vl


def get_reduced_Chi_Squared(y_expect, y_calc, dof):
    """Function that calculates the chi squared value per degree of freedom (i.e. χ^2_ν) of the model.
    Where: 
        1) χ^2_ν:  chi squared value per degree of freedom
        2) ν: degrees of freedom of the fitted model
    
    Gotten from: Measurements and Their Uncertainties (T. Hase)
        Null hypothesis: sample distribution is well modelled by a proposed parent distribution
        1) χ^2_ν ≈ 1 -> Reasonable fit
        2) χ^2_ν << 1 -> Check uncertainties
        3) χ^2_ν > 2 and ν ≈ 10 -> Question null hypothesis
        4) χ^2_ν > 1.5 and approximately 50 ≤ ν ≤ 100 -> Question null hypothesis"""
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
data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples2/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"  # Set absolute path of data
out_img_fl_nm = 'muPT_born_distribution_1_photon_real_10'
out_meta_fl_nm = 'muPT_born_distribution_1_photon_real_10_metadata'
running_script_name = '"Born_1_photon_real_10.py"'
# Data = bare, Model = born

tree_data_fill_var = "mu_truth_born_pt"
tree_model_fill_var = "mu_truth_born_pt"
tree_lead_photon_pt = "mu_truth_leading_photon_pt*(1+0.1*gaussian_random_number)" # Just 1 photon case
tree_second_lead_photon_pt  = "mu_truth_subleading_photon_pt*(1+0.1*gaussian_random_number)"
weigth_var = "1" # Not using weights: "photos_fsr_weight", "herwig_fsr_weight"
# Define constants
"""# 1) W and Z masses: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.030001
m_W_expect = 80.379  # ± 0.012  # [GeV/c^2] [1]
m_W_width = 0.012"""

# From previous fit to simulated data (i.e. using curve_fit)
parms_fit = 2
w_mass_mev, w_boson_width_mev = 80379, 20
hyp_masses_arr = [78, 82, 49]  # Array of: [minimum mass, maximum mass, number of masses in that range], i.e. [79, 83, 5] -> [79, 80, 81, 82, 83]
# hyp_masses_arr = [80, 81, 99]
# hyp_masses_arr = [80.3, 80.5, 99]
"""condition_dat_arr = ['int((mu_truth_leading_photon_pt == 0 && mu_truth_subleading_photon_pt == 0) || (mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt <= 0) || (mu_truth_leading_photon_pt <= 0 && mu_truth_subleading_photon_pt > 0) || (mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt > 0))',
                 'int(mu_truth_leading_photon_pt == 0 && mu_truth_subleading_photon_pt == 0)',
                 'int((mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt <= 0) || (mu_truth_leading_photon_pt <= 0 && mu_truth_subleading_photon_pt > 0))',
                 'int(mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt > 0)']
n_photons = ["all events", 0, 1, 2]"""

# The following condition accounts for just leading photon pt and muon bare pt
condition_dat_arr = [f'((1.0+({tree_lead_photon_pt}/{tree_data_fill_var}))*{weigth_var}*int(mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt <= 0))+((1.0+({tree_second_lead_photon_pt}/{tree_data_fill_var}))*{weigth_var}*int(mu_truth_leading_photon_pt <= 0 && mu_truth_subleading_photon_pt > 0))']
condition_mod_arr = [f'((1.0+({tree_lead_photon_pt}/{tree_model_fill_var}))*{weigth_var}*int(mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt <= 0))+((1.0+({tree_second_lead_photon_pt}/{tree_model_fill_var}))*{weigth_var}*int(mu_truth_leading_photon_pt <= 0 && mu_truth_subleading_photon_pt > 0))']
n_photons = [1]

hist_axis = ["lin", "lin"]  # [x, y] log: logarithmic, lin: linear
data_x_lbl, data_y_lbl, data_title_lbl = "muon PT [GeV]", "Normalised counts", "Bare P_{T,#mu} + P_{T,1photon} photos distribution"
chi_square_x_lbl, chi_square_y_lbl, chi_square_title_lbl = "Hypothesis mass [GeV]", "$χ^{2}$ value", "$χ^{2}$ distribution of fits"
optim_x_lbl, optim_y_lbl, optim_title_lbl = "muon PT [GeV]", "Normalised counts", "Optimal W fit (Bare P_{T,#mu} + P_{T,1photon} photos)"

# Testing parameters
test_frst_entry = False
run_mode = "Report"
# run_mode = "Report"

# Histogram parameters
energies_arr, rest_mass_arr = [], []
# e_min, e_max, use_range = 0, 120, True  # [GeV]
e_min, e_max, use_range = 0, 120, True  # [GeV]
n_hist_bins = 100
summary_arrs = []

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                            Sort tree data and output directories                                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Check if all needed directories exist, else create them
check_if_create_dirs(dirs_arr)

# Test input data
input_file = r.TFile(data_path)
input_file.ls()

tree = input_file.Get("DecayTree")
# Alternatively...
# ch = r.TChain("MCDecayTree")
# ch.Add(data_path)
# cd.Show(0) # Test

# Test data
if test_frst_entry:
    print("Checking first data point:")
    tree.Show(0)
    print("All data printed for first data point")
    quit()

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

colors_to_omit = [3, 7]
names, masses, color, ith_color = {}, {}, {}, -1
for ith in range(hyp_masses_arr[2]):
    hyp_mass = hyp_mass_rng[ith]
    names[str(ith)] = f"M_{{hyp}}={hyp_mass}"
    masses[str(ith)] = hyp_mass
    if ith in colors_to_omit:
        ith_color += 2
    else:
        ith_color += 1
    color[str(ith)] = ith_color+2

# Initiate data histogram and hypothesis histograms
hyp_hists = {}
# hyp_hists['original'] = hist_template.Clone('original')
for name, mass in masses.items():
    hyp_hists[name] = hist_template.Clone(name)
# Split data in two as 'Model' and 'Data'
chi_square_arr = []

# Split data in two as 'Model' and 'Data'
print("Sorting data and model data...")
n_hists = len(masses)

# Sort pseudodata and hypothesis masses
# Pseudodata 
nth_photons = 0
print(f"Processing: data\r", end="")
tree.Draw(f'{tree_data_fill_var}>>data', f"{condition_dat_arr[nth_photons]}*(Entry$%2!=0)", 'goff')
# Hypothesis masses
for idx, name in masses.items():
    print(f"Processing:  {int(idx)+1}/{n_hists}\r", end="")
    mass_hypo_mev = int(hyp_mass_rng[int(idx)]*1000)  # GeV -> MeV
    condition_hist_str = f'(TMath::BreitWigner(V_TRUE_M*1000,{mass_hypo_mev}.,{w_boson_width_mev}.)/TMath::BreitWigner(V_TRUE_M*1000,{w_mass_mev}.,{w_boson_width_mev}.))'
    tree.Draw(f'{tree_model_fill_var}>>{idx}', f"{condition_hist_str}*{condition_dat_arr[nth_photons]}*(Entry$%2==0)", 'goff')
print("Done sorting data and model data")

# Getting the bin content from data histogram to use with optimal histogram
data_arr = []
for idx_energ in range(1, n_hist_bins+1):
    data_arr.append(hist_dat.GetBinContent(idx_energ))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                  Hypothesis mass histogram                                                                  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("Saving hypothesis histograms and data plot...")
# Save hypothesis histograms and data
c = r.TCanvas("c", "c", 1920, 1080)

# Define histogram properties and add histogram to main canvas
if run_mode == "Summary":
    hist_dat.SetTitle(data_title_lbl)
    hist_dat.GetYaxis().SetTitle(data_y_lbl)  # Fraction in label example: "#frac{A}{B}"
    hist_dat.GetXaxis().SetTitle(data_x_lbl)  # Fraction in label example: "#frac{A}{B}", using latex syntax
elif run_mode == "Report":
    hist_dat.SetTitle(" ")
    hist_dat.GetYaxis().SetTitle(" ")  # Fraction in label example: "#frac{A}{B}"
    hist_dat.GetXaxis().SetTitle(" ")  # Fraction in label example: "#frac{A}{B}", using latex syntax
hist_dat.SetLineWidth(2)

# hist_dat.FillStyle = 'solid'
# Color properties and indexes at: https://root.cern/root/html534/TColor.html
# hist_dat.SetFillColor(1)

hist_dat.GetYaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetYaxis().CenterTitle(1)

hist_dat.GetXaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetXaxis().CenterTitle(r.kTRUE)

# Sort energy, data values before normalisation
data_bin_cnts = []
for idx_energ in range(1, n_hist_bins+1):
    data_bin_cnts.append(hist_dat.GetBinContent(idx_energ))

dat_integ_fact = hist_dat.Integral()
if dat_integ_fact != 0:
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

    # Normalise histogram and set both integrals equal -> same number of total events
    if hist_mod_n.Integral() != 0:
        hist_mod_n.Scale(dat_integ_fact/hist_mod_n.Integral())

    # Sort energy, model values before normalisation
    model_bin_cnts = []
    for idx_energ in range(1, n_hist_bins+1):
        model_bin_cnts.append(hist_mod_n.GetBinContent(idx_energ))

    # Calculate chi square of fit and add to chi-squared values array
    fit_dofs = len(model_bin_cnts)-parms_fit
    # model_chi_square = get_reduced_Chi_Squared(data_bin_cnts, model_bin_cnts, fit_dofs)
    model_chi_square = get_Chi_squared(data_bin_cnts, model_bin_cnts)
    chi_square_arr.append(model_chi_square)

    # Normalise histogram and add to final histogram
    if hist_mod_n.Integral() != 0:
        hist_mod_n.Scale(1./hist_mod_n.Integral())
    hist_mod_n.SetLineColor(color[name])
    hist_mod_n.Draw('HIST SAME')
# hist_dat.Draw('HIST E1 SAME')  # Draw data again, so that the data points are on top of everything
if run_mode == "Summary":
    legend.Draw("same")  # Draw legend with all elements
    out_img_fl_nm = f'{dirs_arr[2]}/muPT_{w_mass_mev/1000}_{w_boson_width_mev/1000}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}_summary.png'
elif run_mode == "Report":
    # Turn off general legend of histogram
    hist_dat.SetStats(0)
    out_img_fl_nm = f'{dirs_arr[2]}/muPT_{w_mass_mev/1000}_{w_boson_width_mev/1000}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}_report.png'
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
all_quant_str_wrds = f"mean expected W mass: {w_mass_mev/1000} $[GeV/c^{{2}}]$,\\\\\nmean hypothesis masses: {hyp_mass_rng} $[GeV/c^{{2}}]$,\\\\\nmass width: {w_boson_width_mev/1000} $[GeV/c^{{2}}]$,\\\\\nchi_square value of hypothesis fit: {model_chi_square}"
sum_str = f"{all_quant_str_wrds}\\\\\n"
sum_str += f"	Absolute path to figure: {abs_plot_fl_nm}\\\\\n"
sum_str += f"	Next lines are the data of the shown histograms (if needed): \\\\\n"
all_quant_str = f"	{w_mass_mev/1000}, {hyp_mass_rng}, {w_boson_width_mev}, {model_chi_square}"
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
parbl_shft = fit_vls(real_roots)

# Define uncertainty of masses, i.e. use values at which chi_squared = 1 to calculate spread around root
chi_min_vls_rng = np.ones(len(hyp_mass_rng))*real_roots[0]
chi_max_vls_rng = np.ones(len(hyp_mass_rng))*(parbl_shft[0]+1)
chi_unit_fit_vls = fit_vls-(parbl_shft+1) # Shift parabola to calculate new roots
chi_unit_roots = np.roots(chi_unit_fit_vls)
real_chi_unit_roots = np.unique(chi_unit_roots.real)

# Calculate differences and calculate uncertainty
roots_difs = []
for ith_root in real_chi_unit_roots:
    roots_difs.append(np.absolute(ith_root-real_roots))
max_diff = np.max(roots_difs)
int_max_fidd = int(max_diff)

# Found rounding factor for mean and error
n_factors_of_ten = 0
while(int_max_fidd == 0):
    max_diff = max_diff*10 
    int_max_fidd = int(max_diff)
    n_factors_of_ten += 1
n_factors_of_ten += 3
max_diff = max_diff*1000 
int_max_fidd = int(max_diff)

# Round error and mean (Currently using 4 s.f. to account for possible missrounding)
max_diff = int_max_fidd/10**(n_factors_of_ten)
rounded_roots = []
for ith_root in real_roots:
    nth_rounded_root = int(ith_root*10**(n_factors_of_ten))/10**(n_factors_of_ten)
    rounded_roots.append(nth_rounded_root)
real_roots = rounded_roots

# Define plot properties and save it
plt.scatter(hyp_mass_rng, chi_square_arr, marker='o', c='red', label="$χ^{2}$ values", zorder=1)
plt.scatter(real_chi_unit_roots,fit_vls(real_chi_unit_roots), c='green', label="Mass range limits", zorder=1)
plt.scatter(real_roots,fit_vls(real_roots), c='blue', label="Optimum mass", zorder=1)
plt.plot(chi_x_vls,fit_vls(chi_x_vls), c='black', label="$χ^{2}$ parabola fit", zorder=0)
plt.plot(hyp_mass_rng,chi_max_vls_rng, linestyle='--', c='black', label=f"$χ^{{2}}$ = {parbl_shft[0]}+1", zorder=0)
if run_mode == "Summary":
    plt.title(chi_square_title_lbl)
    plt.xlabel(chi_square_x_lbl)
    plt.ylabel(chi_square_y_lbl)
    plt.legend()
    out_chi_img_fl_nm = f'{dirs_arr[2]}/chi_square_fits_muPT_{w_mass_mev/1000}_{w_boson_width_mev/1000}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}_summary.png'
elif run_mode == "Report":
    plt.title(" ")
    plt.xlabel(" ")
    plt.ylabel(" ")
    out_chi_img_fl_nm = f'{dirs_arr[2]}/chi_square_fits_muPT_{w_mass_mev/1000}_{w_boson_width_mev/1000}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}_report.png'
plt.savefig(out_chi_img_fl_nm, dpi=300)
print("Done fitting chi-square values and saving plot")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                              Data and optimal parameters plot                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Re-scale back histogram for optimal calculations
if dat_integ_fact != 0:
    hist_dat.Scale(dat_integ_fact)

print("Calculating optimal fit and saving plot...\r", end="")
# Creating optimal fit histogram (Assuming minimum value, so ignoring the rest of values)
for i, entry in enumerate(data_arr):
    w_nth = entry*RBW(entry, real_roots[0]*1000, w_boson_width_mev)/RBW(entry, w_mass_mev, w_boson_width_mev)
    hist_optim.Fill(mean_e_vl[i], w_nth)

# Calculate chi-squared value of optimal fit with respect to data
data_bin_cnts, model_bin_cnts = [], []
for idx_energ in range(1, n_hist_bins+1):
    data_bin_cnts.append(hist_dat.GetBinContent(idx_energ))
    model_bin_cnts.append(hist_optim.GetBinContent(idx_energ))

# Calculate chi square of fit and add to chi-squared values array
fit_dofs = len(model_bin_cnts)-parms_fit
# optim_model_chi_square = get_reduced_Chi_Squared(data_bin_cnts, model_bin_cnts, fit_dofs)
optim_model_chi_square = get_Chi_squared(data_bin_cnts, model_bin_cnts)

# Save optimal fit and data in same plot
c = r.TCanvas("c", "c", 1920, 1080)

# Optimal histogram (Using this to define title of hitogram before adding data and optimal fit on top of data)
if run_mode == "Summary":
    hist_optim.SetTitle(optim_title_lbl)
    hist_optim.GetYaxis().SetTitle(optim_y_lbl)  # Fraction in label example: "#frac{A}{B}"
    hist_optim.GetXaxis().SetTitle(optim_x_lbl)  # Fraction in label example: "#frac{A}{B}", using latex syntax
elif run_mode == "Report":
    hist_optim.SetTitle(" ")
    hist_optim.GetYaxis().SetTitle(" ")  # Fraction in label example: "#frac{A}{B}"
    hist_optim.GetXaxis().SetTitle(" ")  # Fraction in label example: "#frac{A}{B}", using latex syntax

    # Turn off general legend of histogram
    hist_dat.SetStats(0)
    hist_optim.SetStats(0)
hist_optim.GetYaxis().SetTitleOffset(1.0)  # Offset the label
hist_optim.GetYaxis().CenterTitle(1)

hist_optim.GetXaxis().SetTitleOffset(1.0)  # Offset the label
hist_optim.GetXaxis().CenterTitle(r.kTRUE)

# Define histogram properties and add histogram to main canvas
hist_dat.SetLineWidth(2)
# hist_dat.FillStyle = 'solid'
# Color properties and indexes at: https://root.cern/root/html534/TColor.html
# hist_dat.SetFillColor(1)

dat_integ_fact = hist_dat.Integral()
if dat_integ_fact != 0:
    hist_dat.Scale(1./dat_integ_fact)
hist_dat.SetLineColor(r.kBlack)
hist_dat.Draw('HIST E1')

# Optimal histogram parameters
hist_optim.SetLineWidth(2)
# hist_optim.SetLineStyle(2)

optim_integ_fact = hist_optim.Integral()
if optim_integ_fact > 0:
    hist_optim.Scale(1./optim_integ_fact)
hist_optim.SetLineColor(r.kBlue)
hist_optim.Draw('HIST SAME')

# Set axis type
if hist_axis[0] == "log":
    r.gPad.SetLogx(1)  # Set logarithmic x-axis
if hist_axis[1] == "log":
    r.gPad.SetLogy(1)  # Set logarithmic y-axis

# Check all hypothesis and add them to the corresponding leyend
if run_mode == "Summary":
    legend = r.TLegend(0.78, 0.27, 0.98, 0.44)  # Legend coords: (x_1, y_1, x_2, y_2)
    legend.AddEntry(hist_dat, "P_{T,#mu} data", "f")
    legend.AddEntry(hist_optim, f"#splitline{{Optimal fit,}}{{M' = {real_roots[0]} GeV}}", "f")
    legend.Draw("SAME")

    out_optim_img_fl_nm = f'{dirs_arr[2]}/optimum_muPT_{w_mass_mev/1000}_{w_boson_width_mev/1000}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}_summary.png'
elif run_mode == "Report":
    out_optim_img_fl_nm = f'{dirs_arr[2]}/optimum_muPT_{w_mass_mev/1000}_{w_boson_width_mev/1000}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}_report.png'
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
start_latex = r"""\documentclass[a4paper,12pt]{article}

\usepackage{graphicx}% Include figure files
\usepackage{dcolumn}% Align table columns on decimal point

% Use Arial font %
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault} 

% Default margins and paper properties %
\usepackage[portrait, margin=0.6in]{geometry}

\begin{document}
	\title{Hypothesis plots summary} % Force line breaks with \\
	\author{1666957, Gustavo Espinal Lugo}
	\date{\today} % It is always \today, today, %  but any date may be explicitly specified

	\maketitle
	%\tableofcontents
	
	\section*{Plots}
"""
end_latex = r"\end{document}"
with(open(f"{crrnt_abs_pth}/{dirs_arr[1]}/{fils_nm_arr[1]}", "w")) as fl:
    fl.write(start_latex)
    for ith in range(len(summary_arrs)):
        sum_arr = summary_arrs[ith]
        hyp_masses_caption = sum_arr[2].replace("\\\\\n", "").replace(": ", "$=$").replace(",", ", ")
        fl.write(f"""
	\\begin{{figure}}[hp]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{sum_arr[1]}}}
		\\caption{{\\small Hypothesis masses {hyp_mass_rng}. }}
		\\label{{fig: fig_{ith}}}
	\\end{{figure}}
    \\newpage

    \\begin{{figure}}[hp]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{crrnt_abs_pth}/{out_chi_img_fl_nm}}}
		\\caption{{\\small $\\chi^{2}$ of hypothesis masses. }}
		\\label{{fig: fig_chi_square}}
	\\end{{figure}}
    \\newpage

    \\begin{{figure}}[hp]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{crrnt_abs_pth}/{out_optim_img_fl_nm}}}
		\\caption{{\\small Data and optimum fit with $\\chi^{2}/DoF (n\\_hist\\_bins-parms\\_fit) = {optim_model_chi_square}/{n_hist_bins-parms_fit}$. Used the hypothesis mass of {real_roots[0]}$\pm${max_diff} $[GeV/c^{{2}}]$. }}
		\\label{{fig: fig_optim_parms}}
	\\end{{figure}}
    \\newpage
    
    \\section*{{Summary and Metadata}}
    Found optimal massses ($\\chi^{2}$ roots): {real_roots} $[GeV/c^{{2}}]$
    Uncertainty $[GeV/c^{2}]$: {max_diff}
    
    {sum_arr[0]}
""")
    fl.write(end_latex)  

# Compile LaTex file
print(f"Current abs path: {crrnt_abs_pth}")
print(f"Tex path: {crrnt_abs_pth}/{dirs_arr[1]}/{fils_nm_arr[1]}")
print(f"Sh path: {crrnt_abs_pth}/{dirs_arr[0]}/{fils_nm_arr[0]}")

sh_fl_content = f"""# Load root
source /cvmfs/lhcb.cern.ch/lib/etc/cern_profile.sh
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_100 x86_64-centos7-gcc10-opt
# Run python script
python3 ./{running_script_name}"""
with(open(f"{crrnt_abs_pth}/{dirs_arr[0]}/{fils_nm_arr[0]}", "w")) as fl:
    fl.write(sh_fl_content)
# Not using run.sh, already using commands with this script
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
