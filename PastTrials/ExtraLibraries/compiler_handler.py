# Program that decides which library to use when compiling, depending on the system which is being used
from platform import system
import os

def decideAndCompile(fil_dir_abs_pth, c_fil_nm, out_fil_nm):
    """Function that decides which library to use to compile C programs, if the given file exists. Assuming same output directory"""
    crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
    crrnt_os = system()
    abs_pth_inp_fl = fil_dir_abs_pth+"\\"+c_fil_nm+".c"  # Assuming just C files
    print(f"Current absolute path: {crrnt_abs_pth}")
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        # Check if file to compile exists in the given directory
        print(f"Checking: {abs_pth_inp_fl}")
        if os.path.exists(abs_pth_inp_fl):
            # Compile and return done
            import win_compiler_library as wcl

            print("Starting to compile...")
            wcl.compile_c(fil_dir_abs_pth, c_fil_nm, out_fil_nm)
            print("Done Compiling\n")
            fl_ext = "exe"
            return fil_dir_abs_pth, out_fil_nm, fl_ext
        else:
            errLine = f"Check input file, it does not exists. Input: {abs_pth_inp_fl}"
            raise Exception(errLine)
    elif crrnt_os == "Linux":
        # Check if file exists in the given directory
        if os.path.exists(abs_pth_inp_fl):
            return crrnt_abs_pth+r"\linx_compiler_library.py"
        else:
            errLine = f"Check input file, it does not exists. Input: {abs_pth_inp_fl}"
            raise Exception(errLine)
    else:
        errLine = f"Not developed for {crrnt_os} yet"
        raise Exception(errLine)


def decideRun(fil_dir_abs_pth, out_fil_nm, fl_ext):
    """Function that decides which library to use to run compiled C programs, if the given file exists. Assuming same output directory"""
    crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
    crrnt_os = system()
    abs_pth_inp_fl = fil_dir_abs_pth+"/"+out_fil_nm+"."+fl_ext
    print(f"Current absolute path: {crrnt_abs_pth}")
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        # Check if file to compile exists in the given directory
        print(f"Checking: {abs_pth_inp_fl}")
        if os.path.exists(abs_pth_inp_fl):
            # Compile and return done
            import win_compiler_library as wcl
            print("Starting to run...")
            wcl.run_c_file(fil_dir_abs_pth, out_fil_nm)
            print()
            print("Done running")
            return None
        else:
            errLine = f"Check input file, it does not exists. Input: {abs_pth_inp_fl}"
            raise Exception(errLine)
    elif crrnt_os == "Linux":
        # Check if file exists in the given directory
        if os.path.exists(abs_pth_inp_fl):
            return crrnt_abs_pth+r"\linx_compiler_library.py"
        else:
            errLine = f"Check input file, it does not exists. Input: {abs_pth_inp_fl}"
            raise Exception(errLine)
    else:
        errLine = f"Not developed for {crrnt_os} yet"
        raise Exception(errLine)


def compile_and_run(c_fl_nm, out_fl_nm):
    # Function that compiles and runs a C file. It assumes that the file is inside the 'DataCruchers' directory
    crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
    lst_dir = crrnt_abs_pth.split("\\")[-1]
    c_programs_abs_dir = crrnt_abs_pth.replace("\\"+lst_dir, "")+"\\DataCrunchers"

    abs_pth_out_dir, out_fil_nam, out_fl_ext = decideAndCompile(c_programs_abs_dir, c_fl_nm, out_fl_nm)
    decideRun(abs_pth_out_dir, out_fil_nam, out_fl_ext)
    return "Done"



# Example of use, picking a file from DataCruchers directory
c_fl_nm = "Z_invariant_mass_calculator"  # .c file
out_fl_nm = "Z_invariant_mass_calculator"  # Output file, .exe if windows, checking for Linux
compile_and_run(c_fl_nm, out_fl_nm)
