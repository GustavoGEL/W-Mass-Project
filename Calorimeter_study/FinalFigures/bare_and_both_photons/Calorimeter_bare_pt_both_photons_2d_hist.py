data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/ProcessTuples2/Wp_W_13TeV_SmearingOff_AlignCorrOff_MomScaleCorrOff.root"

from ROOT import gROOT
from ROOT import gStyle
gROOT.SetBatch(True)
import ROOT as r
# import numpy as np
from array import array
# palette = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# gStyle.SetPalette(len(palette), array('i',palette))

figs_nam = "calorimeter_bare_highest_photon"
y_var = ["mu_ISO_NC_005", "mu_ISO_NC_030", "mu_ISO_NC_050"]
data_y_lbl, data_x_lbl = "Calorimeter detected", "True bare pt plus leading photon PT"
study_var = "mu_truth_bare_pt+mu_truth_leading_photon_pt+mu_truth_subleading_photon_pt"
# weigth_var = "1" # Not using weights: "photos_fsr_weight", "herwig_fsr_weight"
# photon_weight = f'{weigth_var}*int(mu_truth_leading_photon_pt > 0 && mu_truth_subleading_photon_pt > 0)'

main_title = "True leading photon PT vs Calorimeter detected"
radi_arr = ["005", "030", "050"]
title_end = ["r = 0.05", "r = 0.30", "r = 0.50"]
run_mode = "Summary"  # "Summary", "Report"
n_bins, min_e, max_e = 100, 0, 100
test_frst_entry = False

# Set necessary variables
colors_to_omit = [3, 7]
hist_template = r.TH2F("hist_template","",n_bins,min_e,max_e,n_bins,min_e,max_e)
names, hists_arr, color, ith_color = {}, {}, {}, -1
for ith, nth_var in enumerate(radi_arr):
    names[str(ith)] = f"hist_{nth_var}"
    if ith in colors_to_omit:
        ith_color += 2
    else:
        ith_color += 1
    color[str(ith)] = ith_color+2

ifile = r.TFile(data_path)
tree = ifile.Get('DecayTree')

# Test data
if test_frst_entry:
    print("Checking first data point:")
    tree.Show(0)
    print("All data printed for first data point")
    quit()

# Iterate through each case
for ith in range(len(names)):
    # Initialise each histogram
    nth_hist_name = names[str(ith)]
    hists_arr[nth_hist_name] = r.TH2F(nth_hist_name,"",n_bins,min_e,max_e,n_bins,min_e,max_e) 
    
    # Set condition and draw histogram
    nth_str = f'{y_var[int(ith)]}:{study_var}>>{nth_hist_name}'
    tree.Draw(nth_str,'','COLZ')
    
    # Get current histogram and initialise canvas
    hist_mod_n = hists_arr[nth_hist_name]
    cn = r.TCanvas()

    # Set axis and line parameters
    cn.SetLogz()
    hist_mod_n.SetContour(30)
    hist_mod_n.Draw('COLZ')
    hist_mod_n.SetLineWidth(2)
    hist_mod_n.SetLineColor(1)

    hist_mod_n.GetYaxis().SetTitleOffset(1.0)  # Offset the label
    hist_mod_n.GetYaxis().CenterTitle(1)

    hist_mod_n.GetXaxis().SetTitleOffset(1.0)  # Offset the label
    hist_mod_n.GetXaxis().CenterTitle(r.kTRUE)
    
    hist_mod_n.GetYaxis().SetTitle(data_y_lbl)  # Fraction in label example: "#frac{A}{B}"
    hist_mod_n.GetXaxis().SetTitle(data_x_lbl)  # Fraction in label example: "#frac{A}{B}", using latex syntax
    # Set output image name
    main_fig_nam = f'{figs_nam}_{radi_arr[ith]}_{min_e}_to_{max_e}'
    if run_mode == "Summary":
        hist_mod_n.SetTitle(f'{main_title} r = 0.05')
        main_fig_nam += "_summary.png"
    elif run_mode == "Report":
        hist_mod_n.SetStats(0)
        main_fig_nam += "_report.png"
    cn.SaveAs(main_fig_nam)
print("Done")