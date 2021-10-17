# Main idea: Do the same as Z_invariant_mass_calculator.py, but iterate over while keeping track of the weighted mean.
# However, this program do not plot anything, it just:
# 1) Uses final calculator -> Calculate and saved all output energy values
# 2) Uses highest peak when showing all the data histogram to place itself and asks the user to input an energy range, while suggesting an estimate based on the weighted mean and standard deviation
# 3) Starts iterating on the same histogram to recalculate weighted mean and std while keeping track of everything that is going on, i.e. iteration number, energy range, etc
#    However, it stops every iteration to ask the user if continuing while showing the new iteration histogram. It saves all the bins, counts, etc .txt file and the generated histogram as well
# 4) If want to stop iterating, just input no/n to stop and the program will finish running

# Developing later...
