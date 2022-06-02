import os
data_path = "/storage/epp2/phshgg/Public/MPhysProject_2021_2022/13TeV__2018__magnet_down_data__Z_candidates.root"

# In PC
crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
data_path = crrnt_abs_pth+"/Data/13TeV__2018__magnet_down_data__Z_candidates.root"  # In my computer/local

print(data_path)

import ROOT
import matplotlib.pyplot as plt
import numpy as np

input_file = ROOT.TFile(data_path)
input_file.ls()

tree = input_file.Get('DecayTree')

print("First data point:")
tree.Show(0)
print("All data printed for first data point")

for entry in tree:
        # Sorting entry data
        mup_PT = entry.mup_PT
        mup_ETA = entry.mup_ETA
        mup_PHI = entry.mup_PHI
        mum_PT = entry.mum_PT
        mum_ETA = entry.mum_ETA
        mum_PHI = entry.mum_PHI

        print("First particle:")
        print(f"Momentum: {mup_PT}")
        print(f"Theta: {mup_ETA}")
        print(f"Phi: {mup_PHI}")

        print("Second particle:")
        print(f"Momentum: {mum_PT}")
        print(f"Theta: {mum_ETA}")
        print(f"Phi: {mum_PHI}")

        # Calculate total momentum, assuming two final particles
        p_tot_x = (mup_PT*np.sin(mup_ETA)*np.cos(mup_PHI))+(mum_PT*np.sin(mum_ETA)*np.cos(mum_PHI))
        p_tot_y = (mup_PT*np.sin(mup_ETA)*np.sin(mup_PHI))+(mum_PT*np.sin(mum_ETA)*np.sin(mum_PHI))
        p_tot_z = (mup_PT*np.cos(mup_ETA))+(mum_PT*np.cos(mum_ETA))

        p_tot_mag = ((p_tot_x**2)+(p_tot_y**2)+(p_tot_z**2))**(0.5)

        print(f"Total momentum: [{p_tot_x}, {p_tot_y}, {p_tot_z}] [MeV]")
        print(f"Total momentum magnitude: {p_tot_mag} [MeV]")

        # Total energy of decay:
        m_mu = 105.7  # MeV/c^2
        E_tot = p_tot_mag + 2*m_mu
        print(f"Total energy: {E_tot} [MeV]")

        print("Individually calculated:")
        m_mu = 105.7  # MeV/c^2

        p_1_x = mup_PT*np.sin(mup_ETA)*np.cos(mup_PHI)
        p_1_y = mup_PT*np.sin(mup_ETA)*np.sin(mup_PHI)
        p_1_z = mup_PT*np.cos(mup_ETA)

        p_tot_1_squared = (p_1_x**2)+(p_1_y**2)+(p_1_z**2)
        E_tot_1 = (p_tot_1_squared + (m_mu*m_mu))**(0.5)

        p_2_x = mum_PT*np.sin(mum_ETA)*np.cos(mum_PHI)
        p_2_y = mum_PT*np.sin(mum_ETA)*np.sin(mum_PHI)
        p_2_z = mum_PT*np.cos(mum_ETA)

        p_tot_2_squared = (p_2_x**2)+(p_2_y**2)+(p_2_z**2)
        E_tot_2 = (p_tot_2_squared + (m_mu*m_mu))**(0.5)

        # Total energy of decay:
        print(f"Total energy: {E_tot} [MeV]")

        print(f"Using kinetic energy and momentum relationships")
        break

"""for entry in tree:
        # Sort entry data
        mup_PT = entry.mup_PT
   # mup_ETA = entry.mup_ETA
   # mup_PHI = entry.mup_PHI
   # mum_PT = entry.mum_PT
   # mum_ETA = entry.mum_ETA
   # mum_PHI = entry.mum_PHI
   # Calculate total momentum, assuming two final particles
   print(f"Testing numpy: {np.cos(0)}")
   # Calculate the invariant mass
   invariant_mass = ((mup_PT**2)-(mup_PT**2))**(0.5)
   # See if can plot it in matplotlib"""
