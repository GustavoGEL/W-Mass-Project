#!usr/bin/gnu python
from ROOT import gROOT
gROOT.SetBatch(True)

import os, datetime
import ROOT as r  # Currently not working, getting an error from 2nd command: source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_100 x86_64-centos7-gcc10-opt
import numpy as np
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit


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


def get_Chi_squared(y_expect, y_calc):
    """Function that calculates the Chi squared value of expected values and input values. 
    Gotten from: Measurements and Their Uncertainties (T. Hase)"""
    # Conver input data types to arrays
    y_expect = np.asarray(y_expect)
    y_calc = np.asarray(y_calc)
    err = np.sqrt(len(y_expect)-1)  # n_measurements-1 -> -1 due to mean calculation
    return np.sum((y_calc-y_expect)**2)/err
    # err = y_expect  # Approximation from Thursday meeting, not expected to affect final fit value, not using as getting inf values
    # return np.sum((y_calc-y_expect)**2/y_expect)


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


def Rel_Wreit_Breigh(energ_x, mean, sigma):  # Comes from QFT, invariant? -> so this function just depends on mass, not on PT. Can also ignore k as using this for the ratios -> k/k -> 1
    """Function that generates the relativistic Breit-Wigner distribution as s function of energy. NOTE: quantities are in natural units"""
    gamma = (mean*mean*(mean*mean+sigma*sigma))**(0.5)
    k_const = (2*(2**(0.5))*mean*sigma*gamma)/(np.pi*(((mean*mean)+gamma)**(0.5)))
    f_energ = k_const/((((energ_x*energ_x)-(mean*mean))**(2))+(mean*mean*sigma*sigma))
    return f_energ


# Taking time to save the taken time of the entire program to run, so that it can be taken into account when calculating again
strt_tm = datetime.datetime.now()
print("Program started, taking time...")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                         Parameters                                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Input and output paths and files related
crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
dirs_arr = ["scripts", "doc", "plots", "past_trials"]  # Just need the first three, but extra directories just in case
fils_nm_arr = ["run.sh", "main.tex"]  # and: .../scripts/run.sh, .../doc/main.tex
data_path = "/storage/epp2/phshgg/Public/DVTuples__v24e/13TeV_2016_28r1_Down_W_Sim09h.root"  # Set absolute path of data
nth_plot = 1  # Update according to loop iterations, but using as this for tests
hyp_masses_arr = [79, 83, 5]  # Array of: [minimum mass, maximum mass, number of masses in that range], i.e. [79, 83, 5] -> [79, 80, 81, 82, 83]

# Testing parameters
n_vals, testing = 1000, True

# Histogram parameters
energies_arr, rest_mass_arr = [], []
e_min, e_max, use_range = 0, 120, True  # [GeV]
n_hist_bins = 100
summary_arrs = []

# Define constants
"""# 1) W and Z masses: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.030001
m_W_expect = 80.379  # ± 0.012  # [GeV/c^2] [1]
m_W_width = 0.012"""

# From previous fit to simulated data (i.e. using curve_fit)
m_W_expect = 80.36010913  # ± 2.07041274  # [GeV/c^2] [1]
m_W_width = 2.07041274

# Check if all needed directories exist, else create them
check_if_create_dirs(dirs_arr)

# Test input data
input_file = r.TFile(data_path)
input_file.ls()

tree = input_file.Get("WpIso/DecayTree")

"""# Test data
print("Checking first data point:")
tree.Show(0)
print("All data printed for first data point")"""

# Create range of energies and hypothesis masses
energ_bin_vls = np.linspace(e_min, e_max, n_hist_bins+1)
hyp_mass_rng = np.linspace(hyp_masses_arr[0], hyp_masses_arr[1], hyp_masses_arr[2])

# Mean energy values of histogram
mean_e_vl = []
for idx_energ in range(1, n_hist_bins+1):
        mean_e_vl.append((energ_bin_vls[idx_energ]+energ_bin_vls[idx_energ-1])*0.5)

# Generate histogram template and dictionaries with all the mean values with their respective line colors
hist_template = r.TH1F('hist_template','mu_PT', n_hist_bins, e_min, e_max)
hist_dat = hist_template.Clone("data")
hist_optim = hist_template.Clone("optim_fit")

names, masses, color = {}, {}, {}
for ith in range(hyp_masses_arr[2]):
    hyp_mass = hyp_mass_rng[ith]
    names[str(ith)] = f"M={hyp_mass}"
    masses[str(ith)] = hyp_mass
    color[str(ith)] = ith+2

# Initiate data histogram and hypothesis histograms
hyp_hists = {}
# hyp_hists['original'] = hist_template.Clone('original')
for name, mass in masses.items():
    hyp_hists[name] = hist_template.Clone(name)

# Split data in two as 'Model' and 'Data'
data_arr, model_dat_arr, chi_square_arr = [], [], []
print("Sorting data...")

for i, entry in enumerate(tree):
    # Convert data from MeV to GeV
    mu_PT = entry.mu_PT/1000

    # Split data: 1) Add to corresponding array and histogram, 2) test, then optimize? (Tried to create a new ttree, but couldn't make it work)
    if i%2 == 0:  # Even -> Data
        data_arr.append(mu_PT)

        # Add values to PT data histogram
        hist_dat.Fill(mu_PT)
    else:  # Odd -> Model
        model_dat_arr.append(mu_PT)

        # Calculate new weights and add values to PT model data histogram
        for name, mass in masses.items():
            w_nth = Rel_Wreit_Breigh(mu_PT, masses[name], m_W_width)/Rel_Wreit_Breigh(mu_PT, m_W_expect, m_W_width)
            hyp_hists[name].Fill(mu_PT, w_nth)

    if testing:
        # Break loop or keep adding values
        if i == n_vals:
            print(f"Calculated: {i}/{n_vals} -> {round(100*(i/n_vals), 3)}% done", )
            break  # Just testing the first value
        else:
            print(f"Calculated: {i}/{n_vals} -> {round(100*(i/n_vals), 3)}% done \r", end="")

# Show final histograms
c = r.TCanvas("c", "c", 1920, 1080)

# Define histogram properties and add histogram to main canvas
hist_dat.SetLineWidth(0)
hist_dat.FillStyle = 'solid'
# Color properties and indexes at: https://root.cern/root/html534/TColor.html
hist_dat.SetFillColor(1)

hist_dat.GetYaxis().SetTitle("Normalised counts")  # Fraction in label example: "#frac{A}{B}"
hist_dat.GetYaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetYaxis().CenterTitle(1)

hist_dat.GetXaxis().SetTitle("Energy [#frac{GeV}{c^{2}}]")  # Fraction in label example: "#frac{A}{B}", using latex syntax
hist_dat.GetXaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetXaxis().CenterTitle(r.kTRUE)

# hist_dat = hyp_hists[mass_name]
hist_dat.Scale(1./hist_dat.Integral())
# hist_dat.Draw('HIST' if i == 0 else 'HIST SAME')
hist_dat.SetLineColor(r.kBlue)
hist_dat.Draw('HIST')

# Check all hypothesis and add them to the corresponding leyend
legend = r.TLegend(0.78, 0.27, 0.98, 0.44)  # Legend coords: (x_1, y_1, x_2, y_2)
legend.AddEntry(hist_dat, "PT data", "f")
for name, mass in masses.items():
    # Fill each hypothesis histogram
    print(f"Adding histogram: {name}")
    hist_mod_n = hyp_hists[name]
    hist_mod_n.SetLineWidth(2)
    hist_mod_n.FillStyle = 'solid'
    # Color properties and indexes at: https://root.cern/root/html534/TColor.html
    # hist_mod_n.SetFillColor(color[name])

    hist_mod_n.Scale(1./hist_mod_n.Integral())
    hist_mod_n.SetLineColor(color[name])
    hist_mod_n.Draw('HIST SAME')
    c.Update()

    # Add histogram label to legend
    legend.AddEntry(hist_mod_n, f"PT, {names[name]}", "f")

    # Sort energy, data and model values
    data_bin_cnts, model_bin_cnts = [], []
    for idx_energ in range(1, n_hist_bins+1):
        data_bin_cnts.append(hist_dat.GetBinContent(idx_energ))
        model_bin_cnts.append(hist_mod_n.GetBinContent(idx_energ))

    # Calculate chi square of fit and add to chi-squared values array
    model_chi_square = get_Chi_squared(data_bin_cnts, model_bin_cnts)
    chi_square_arr.append(model_chi_square)
legend.Draw("same")

out_img_fl_nm = f'plots/muPT_{m_W_expect}_{m_W_width}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}.png'
c.Print(out_img_fl_nm)

print(f"Gotten Chi squared values: {chi_square_arr}")

# Set variables to use for LaTex/PDF
# Summary line of data used:
abs_plot_fl_nm = f"{crrnt_abs_pth}/{out_img_fl_nm}"
all_quant_str_wrds = f"Number of data points used: {i}, mean expected W mass: {m_W_expect} [GeV/c^2], mean hypothesis masses: {hyp_mass_rng} [GeV/c^2], mass width: {m_W_width} [GeV/c^2], chi_square value of hypothesis fit: {model_chi_square}"
sum_str = f"{all_quant_str_wrds}\\\\\n"
sum_str += f"	Absolute path to figure: {abs_plot_fl_nm}\\\\\n"
sum_str += f"	Next lines are the data of the shown histograms (if needed): \\\\\n"
all_quant_str = f"	{i}, {m_W_expect}, {hyp_mass_rng}, {m_W_width}, {model_chi_square}"
sum_str += f"	All quantities: {all_quant_str}\\\\\n"
sum_str += f"	X_energ_vls = {mean_e_vl}\\\\\n"
sum_str += f"	Y_data_bin_cnts = {data_bin_cnts}\\\\\n"
sum_str += f"	Y_model_bin_cnts = {model_bin_cnts}\\\\\n"

summary_arrs.append([sum_str, abs_plot_fl_nm, all_quant_str_wrds, abs_plot_fl_nm])
# End of iteration

# Scale up values to improve accuracy
chi_square_arr_rng = np.asarray(chi_square_arr)

# Fit chi_squared distribution with parabola to get optimal values and save plot
fit_optim_parms = np.polyfit(hyp_mass_rng, chi_square_arr_rng, 2)
fit_vls = np.poly1d(fit_optim_parms)
roots = np.roots(fit_vls)
real_roots = np.unique(roots.real)

plt.title("Chi-squared distribution of fits")
plt.scatter(hyp_mass_rng, chi_square_arr, marker='o', c='red', label="chi values")
plt.plot(hyp_mass_rng,fit_vls(hyp_mass_rng), c='black', label="chi fit")
plt.xlabel("Hypothesis mass [$GeV/c^{2}$]")
plt.ylabel("Chi-squared value")
plt.legend()
out_chi_img_fl_nm = f'plots/chi_square_fits_muPT_{m_W_expect}_{m_W_width}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}.png'
plt.savefig(out_chi_img_fl_nm, dpi=300)

# Save optimal fit and data
c = r.TCanvas("c", "c", 1920, 1080)

# Define histogram properties and add histogram to main canvas
hist_dat.SetLineWidth(0)
hist_dat.FillStyle = 'solid'
# Color properties and indexes at: https://root.cern/root/html534/TColor.html
hist_dat.SetFillColor(1)

hist_dat.GetYaxis().SetTitle("Normalised counts")  # Fraction in label example: "#frac{A}{B}"
hist_dat.GetYaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetYaxis().CenterTitle(1)

hist_dat.GetXaxis().SetTitle("Energy [#frac{GeV}{c^{2}}]")  # Fraction in label example: "#frac{A}{B}", using latex syntax
hist_dat.GetXaxis().SetTitleOffset(1.0)  # Offset the label
hist_dat.GetXaxis().CenterTitle(r.kTRUE)

# hist_dat = hyp_hists[mass_name]
hist_dat.Scale(1./hist_dat.Integral())
# hist_dat.Draw('HIST' if i == 0 else 'HIST SAME')
hist_dat.SetLineColor(r.kBlue)
hist_dat.Draw('HIST')

"""# Define optimal fit histogram properties and add histogram to main canvas
hist_optim.SetLineWidth(2)
# Color properties and indexes at: https://root.cern/root/html534/TColor.html

hist_optim.Scale(1./hist_optim.Integral())
hist_optim.SetLineColor(r.kGreen)
hist_optim.Draw('HIST SAME')

# Check all hypothesis and add them to the corresponding leyend
legend = r.TLegend(0.78, 0.27, 0.98, 0.44)  # Legend coords: (x_1, y_1, x_2, y_2)
legend.AddEntry(hist_dat, "PT data", "f")
legend.AddEntry(hist_optim, "PT optimum fit", "f")
legend.Draw("same")"""

# Retrieve optimal values and calculate optimal fit

# w_boson_width_mev = 2.1*1.e3
# mass_hypo_mev = real_roots[0]*1.e3
# optimum_fit = hist_dat.Draw(f'mu_PT*1.e-3>>"Optimum_Values"',f'TMath::BreitWigner(mu_MC_BOSON_M,{mass_hypo_mev},{w_boson_width_mev})/TMath::BreitWigner(mu_MC_BOSON_M,80385.,{w_boson_width_mev})','goff')

optimum_fit = r.TF1("optimal_fit", f"TMath::BreitWigner(x,[2],[1])/TMath::BreitWigner(x,[0],[1])", e_min, e_max, 3)  # Change to final formula/implement per fits
optimum_fit.SetParameters(m_W_expect, m_W_width, real_roots[0])
# hist_dat.Draw(f'mu_PT*1.e-3>>"Optimum_Values"',optimum_fit,'goff')
optimum_fit.SetLineColor(r.kRed)
optimum_fit.SetLineStyle(2)
hist_dat.Fit(optimum_fit)
# optimum_fit.Scale(1./optimum_fit.Integral())
optimum_fit.DrawClone("same")
c.Update()

# Check all hypothesis and add them to the corresponding leyend
legend = r.TLegend(0.78, 0.27, 0.98, 0.44)  # Legend coords: (x_1, y_1, x_2, y_2)
legend.AddEntry(hist_dat, "PT data", "f")
legend.AddEntry(optimum_fit, f"Optimal fit, M' = {m_W_expect} GeV", "f")
legend.Draw("same")

out_optim_img_fl_nm = f'plots/optimum_muPT_{m_W_expect}_{m_W_width}_between_{hyp_masses_arr[0]}_and_{hyp_masses_arr[1]}.png'
c.Print(out_optim_img_fl_nm)

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

\definecolor{black}{HTML}{000000}

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
    Found optimal massses (chi-squared roots): {real_roots} [GeV/c^2]

	\\begin{{figure}}[tb]
		\\centering
		\\includegraphics[width=\\columnwidth]{{{sum_arr[1]}}}
		\\caption{{\\small {sum_arr[2]} from {sum_arr[3]} }}
		\\label{{fig: fig_{ith}}}
	\\end{{figure}}

""")
    fl.write(end_latex)
print(sum_str)

# Compile LaTex file
print(f"Corrunt abs path: {crrnt_abs_pth}")
print(f"Tex path: {crrnt_abs_pth}/{dirs_arr[1]}/{fils_nm_arr[1]}")
print(f"Sh path: {crrnt_abs_pth}/{dirs_arr[0]}/{fils_nm_arr[0]}")

sh_fl_content = """dir=$(PWD) [Not working]
Linux commands to:
Detect current directory so that it can be used to run the script
Run python script to create all files and directories necessary"""
with(open(f"{crrnt_abs_pth}/{dirs_arr[0]}/{fils_nm_arr[0]}", "w")) as fl:
    fl.write(sh_fl_content)
# Not using run.sh yet as this commands do not exist? Ask Mika

# Show running time
end_tm = datetime.datetime.now()
time_diff = str(end_tm-strt_tm)
print(f"The programm ran for: {time_diff} [s]")
print("Done")
