import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os, datetime

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

print("Checking first data point:")
tree.Show(0)
print("All data printed for first data point")

energies_arr, rest_mass_arr, errors_arr = [], [], []
# Limiter for tester
n_vals, nth_val = 10000, 1
tot_vals = 0

# Go through each data point
for entry in tree:
        # Count number or datapoints
        tot_vals += 1

        # Sorting entry data
        mup_PT = entry.mup_PT
        mup_ETA = entry.mup_ETA
        mup_PHI = entry.mup_PHI
        mum_PT = entry.mum_PT
        mum_ETA = entry.mum_ETA
        mum_PHI = entry.mum_PHI

        print("First particle:")
        print(f"Transverse momentum (pt): {mup_PT}")
        print(f"Pseudorapidity (eta): {mup_ETA}")
        print(f"Azimuthal angle (phi): {mup_PHI}")

        print("Second particle:")
        print(f"Transverse momentum (pt): {mum_PT}")
        print(f"Pseudorapidity (eta): {mum_ETA}")
        print(f"Azimuthal angle (phi): {mum_PHI}")

        # Calculate rest mass of Z_0

        # # # # # # # # # # # # # # # # Way 1 # # # # # # # # # # # # # # # #
        mup_P_squared = (mup_PT*np.cos(mup_ETA))**2
        mum_P_squared = (mum_PT*np.cos(mum_ETA))**2

        print("Individually calculated momentum:")
        p_1_THETA = 2*np.arctan(np.exp(-mup_ETA))
        p_2_THETA = 2*np.arctan(np.exp(-mum_ETA))
        m_mu = 105.7  # MeV/c^2

        p_1_x = mup_PT*np.sin(p_1_THETA)*np.cos(mup_PHI)
        p_1_y = mup_PT*np.sin(p_1_THETA)*np.sin(mup_PHI)
        p_1_z = mup_PT*np.cos(p_1_THETA)

        p_tot_1_squared = (p_1_x**2)+(p_1_y**2)+(p_1_z**2)
        E_tot_1 = (p_tot_1_squared + (m_mu*m_mu))**(0.5)

        p_2_x = mum_PT*np.sin(p_2_THETA)*np.cos(mum_PHI)
        p_2_y = mum_PT*np.sin(p_2_THETA)*np.sin(mum_PHI)
        p_2_z = mum_PT*np.cos(p_2_THETA)

        p_tot_2_squared = (p_2_x**2)+(p_2_y**2)+(p_2_z**2)
        E_tot_2 = (p_tot_2_squared + (m_mu*m_mu))**(0.5)

        E_tot = E_tot_1+E_tot_2+2*m_mu

        # Total energy of decay:
        print(f"Total energy: {E_tot} [MeV]")

        # Developing a new method, using the same, but in the end, check if adding properly the energies
        # # # # # # # # # # # # # # # # Way 2 # # # # # # # # # # # # # # # #
        print("Individually calculated momentum:")
        p_1_THETA = 2*np.arctan(np.exp(-mup_ETA))
        p_2_THETA = 2*np.arctan(np.exp(-mum_ETA))
        m_mu = 105.7  # MeV/c^2

        p_1_x = mup_PT*np.sin(p_1_THETA)*np.cos(mup_PHI)
        p_1_y = mup_PT*np.sin(p_1_THETA)*np.sin(mup_PHI)
        p_1_z = mup_PT*np.cos(p_1_THETA)

        p_tot_1_squared = (p_1_x**2)+(p_1_y**2)+(p_1_z**2)
        E_tot_1 = (p_tot_1_squared + (m_mu*m_mu))**(0.5)

        p_2_x = mum_PT*np.sin(p_2_THETA)*np.cos(mum_PHI)
        p_2_y = mum_PT*np.sin(p_2_THETA)*np.sin(mum_PHI)
        p_2_z = mum_PT*np.cos(p_2_THETA)

        p_tot_2_squared = (p_2_x**2)+(p_2_y**2)+(p_2_z**2)
        E_tot_2 = (p_tot_2_squared + (m_mu*m_mu))**(0.5)

        E_tot = E_tot_1+E_tot_2  # +2*m_mu

        Z_rest_mass = ((E_tot*E_tot)-(m_mu*m_mu))**(0.5)

        # Total energy of decay:
        print(f"Total energy (method 2): {E_tot} [MeV]")
        print(f"Rest mass of Z boson (method 2): {Z_rest_mass} [MeV]")

        expected_Z_mass = 91500  # [MeV]
        print(f"Expecting rest mass of Z boson around: {expected_Z_mass} [MeV]")
        print(f"Error (%): {100*(Z_rest_mass-expected_Z_mass)/(expected_Z_mass)}")

        # Add values to array
        energies_arr.append(E_tot)
        rest_mass_arr.append(Z_rest_mass)
        errors_arr.append((Z_rest_mass-expected_Z_mass)/(expected_Z_mass))

        # Break loop or keep adding values
        """if nth_val == n_vals:
            break  # Just testing the first value
        else:
            nth_val += 1"""

# Convert arrays into numpy arrays to improve efficiency
# np.asarray(energies_arr)
np.asarray(rest_mass_arr)
# np.asarray(errors_arr)

# Plot distribution of masses vs energy 
print(f"Using {tot_vals} values in plot")
print("Setting up plot")

# Plotting calculated data
# plt.plot(energies_arr, rest_mass_arr)
"""plt.scatter(energies_arr, rest_mass_arr)
plt.xlabel("Total Energy [MeV]")
plt.ylabel("Rest Mass [MeV/c²]")
plt.title("Z⁰ rest mass")
plt.savefig(f"Figures/energy_restmass_{tot_vals}_plot.png", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')
# plt.show()"""

# Plotting errors calculated:
plt.scatter(energies_arr, errors_arr)
plt.xlabel("Total Energy [MeV]")
plt.ylabel("Error [0-1]")
plt.title("Z⁰ errors")
plt.savefig(f"Figures/energy_restmasserrors_{tot_vals}_plot.png", dpi=600, facecolor='w', edgecolor='w', orientation='portrait')
# plt.show()

# Calculate average and std
avg_rest_mass = np.mean(rest_mass_arr)
str_rest_mass = np.std(rest_mass_arr)

print(f"Average Z boson rest mass: {avg_rest_mass} [MeV/c²]")
print(f"Standard deviation of Z boson rest mass: {str_rest_mass} [MeV/c²]")
# Saving in a file
end_tm = datetime.datetime.now()
time_diff = str(end_tm-strt_tm)
print(f"The programm ran for: {time_diff} [s]")
with open(f"Figures/OutputDat_{tot_vals}.txt", "w") as fl:
    fl.write("average rest mass[MeV/c²],standard deviation[MeV/c²],number of fitted datapoints,time of that the program ran[h:m:s]\n")
    fl.write(str(avg_rest_mass)+"\n")
    fl.write(str(str_rest_mass)+"\n")
    fl.write(str(tot_vals)+"\n")
    fl.write(str(time_diff)+"\n")
print("Done saving everything, check Figures folder on this directory")
