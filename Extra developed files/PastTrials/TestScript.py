import numpy as np
data_path = '/storage/epp2/phshgg/Public/MPhysProject_2021_2022/'

# Event data
mup_PT = 38132.5  # MeV
mup_ETA = 4.34166  # rad
mup_PHI = -2.64944  # rad
mum_PT = 39796  # MeV
mum_ETA = 3.21874  # rad
mum_PHI = 0.558677  # rad

# Calculating polar angle
nup_THETA = 2*np.arctan((mup_ETA)

# Calculating invariant mass
p_tot_x = (mup_PT*np.sin(mup_ETA)*np.cos(mup_PHI))+(mum_PT*np.sin(mum_ETA)*np.cos(mum_PHI))
p_tot_y = (mup_PT*np.sin(mup_ETA)*np.sin(mup_PHI))+(mum_PT*np.sin(mum_ETA)*np.sin(mum_PHI))
p_tot_z = (mup_PT*np.cos(mup_ETA))+(mum_PT*np.cos(mum_ETA))

print(f"p_tot = ({p_tot_x}, {p_tot_y}, {p_tot_z})")
