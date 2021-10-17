import matplotlib.pyplot as plt
from numpy.lib.function_base import append

def read_summary_data(inp_sum_dat_fl):
    summary_dat_arr, avg_bin_vals, n_counts, prev_ln = [], [], [], ""
    read_avg_bins, read_n_counts = False, False
    with(open(inp_sum_dat_fl, "r")) as fl:
        lines = fl.readlines()
        for line in lines:
            line = line.strip()
            if prev_ln == "Gotten avg_bin_vals values:" and not read_avg_bins:
                avg_bin_vls_strs = line.split(",")
                for ith in range(len(avg_bin_vls_strs)):
                    avg_bin_vals.append(float(avg_bin_vls_strs[ith]))
                print(f"Gotten avg_bin_vals: {avg_bin_vals}")
                read_avg_bins = True
            elif prev_ln == "Gotten n_count values:" and not read_n_counts:
                n_counts_strs = line.split(",")
                for ith in range(len(n_counts_strs)):
                    print(f"count: {n_counts_strs[ith]}")
                    n_counts.append(float(n_counts_strs[ith]))
                read_n_counts = True
            else:
                summary_dat_arr.append(line)
                prev_ln = line
    return summary_dat_arr, n_counts, avg_bin_vals

"""n_counts = [1.30478560e-03, 1.37481737e-03, 1.09344105e-03, 7.92762522e-04,
5.32060151e-04, 3.44696398e-04, 2.42306478e-04, 1.66714304e-04,
1.21569658e-04, 8.55617195e-05, 6.20953218e-05, 4.46057518e-05,
3.29215434e-05, 2.42747392e-05, 1.75385603e-05, 1.28354827e-05,
9.47964084e-06, 6.83415967e-06, 4.67858243e-06, 3.35584185e-06,
2.66997636e-06, 1.59218774e-06, 1.56769254e-06, 9.06322250e-07,
3.42932743e-07, 3.18437547e-07, 2.44951960e-07, 3.42932743e-07,
4.89903919e-08, 1.71466372e-07, 1.22475980e-07, 1.22475980e-07,
2.44951960e-08, 2.44951960e-08, 7.34855879e-08, 7.34855879e-08,
4.89903919e-08, 2.44951960e-08, 2.44951960e-08, 0.00000000e+00,
0.00000000e+00, 7.34855879e-08, 4.89903919e-08, 2.44951960e-08,
0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
0.00000000e+00, 2.44951960e-08]

bins = [3.95158822e+00, 1.63028911e+02, 3.22106234e+02, 4.81183557e+02,
6.40260879e+02, 7.99338202e+02, 9.58415525e+02, 1.11749285e+03,
1.27657017e+03, 1.43564749e+03, 1.59472482e+03, 1.75380214e+03,
1.91287946e+03, 2.07195678e+03, 2.23103411e+03, 2.39011143e+03,
2.54918875e+03, 2.70826608e+03, 2.86734340e+03, 3.02642072e+03,
3.18549804e+03, 3.34457537e+03, 3.50365269e+03, 3.66273001e+03,
3.82180734e+03, 3.98088466e+03, 4.13996198e+03, 4.29903930e+03,
4.45811663e+03, 4.61719395e+03, 4.77627127e+03, 4.93534859e+03,
5.09442592e+03, 5.25350324e+03, 5.41258056e+03, 5.57165789e+03,
5.73073521e+03, 5.88981253e+03, 6.04888985e+03, 6.20796718e+03,
6.36704450e+03, 6.52612182e+03, 6.68519915e+03, 6.84427647e+03,
7.00335379e+03, 7.16243111e+03, 7.32150844e+03, 7.48058576e+03,
7.63966308e+03, 7.79874041e+03, 7.95781773e+03]"""


tot_vals = 256632
inp_sum_dat_fl = f"FinalFigures/rest_mass_hist_{str(tot_vals)}_calc_dat.txt"
sum_dat, n_counts, avg_bin_vals = read_summary_data(inp_sum_dat_fl)

plt.scatter(y=n_counts, x=avg_bin_vals, label="Rest Mass")
plt.title("Data to fit")
plt.xlabel("bins")
plt.ylabel("n_counts")
plt.show()
