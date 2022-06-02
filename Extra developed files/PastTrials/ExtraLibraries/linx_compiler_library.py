import os
from subprocess import PIPE, run


def before_using_steps(language_nm):
    """Instructions to know what to do and to install to make this library work properly for an array of languages"""
    language_nm.sort()  # Show in alphabetical order
    for lnguage in language_nm:
        lnguage = lnguage.lower()
        if lnguage == "c":
            print('For C. First, install GCC and the necessary dependencies before using C compilation functions from '
                  'this library')
        else:
            print("Language not available for this library, but may be added")
    return None


def compile_c(fil_dir_abs, c_fl_nm, exe_fl_nm):  # Developing
    """Function that compiles a .c file into a .exe file. NOTE: Check that gcc is already installed and working before
    using this function. Otherwise, it is not going to work"""
    cmnd_line = f'cd /d "{fil_dir_abs}" && gcc -o "{exe_fl_nm}" "{c_fl_nm}.c"'
    os.system(cmnd_line)
    print(f"{exe_fl_nm}.exe file compiled from {c_fl_nm}.c")
    return None


# Used at beginning of 3rd year, not sure if useful right now
def compile_c_uni_settings(fil_dir_abs, c_fl_nm, exe_fl_nm):  # Developing?
    """Function that compiles a .c file into a .exe file. NOTE: Check that gcc is already installed and working before
    using this function. Otherwise, it is not going to work"""
    # print("They asked for the following extra parameters when using gcc")
    # print(' -x c -Wall -Werror -std=c99 -lm')
    # print("Where each parameter have the following function:")
    # print("-x c : Explicitly specify to use language c to compile")
    # print("-Wall: This option enables all the warnings in GCC. i.e.: $ gcc -Wall main.c -o main")
    # print("-Werror: Convert any warning into an error. i.e.: $ gcc -Wall -Werror main.c -o main")
    # print("-std=c99: Determine standard language to c99")
    # print("-lm: link a library to use (generally math library with floating point)")
    print("The new command that it is being used is:")
    print(f'gcc -x c -Wall -Werror -std=c99 -lm -o "{exe_fl_nm}" "{c_fl_nm}.c"')
    cmnd_line = f'cd /d "{fil_dir_abs}" && gcc -x c -Wall -Werror -std=c99 -lm -o "{exe_fl_nm}" "{c_fl_nm}.c"'
    os.system(cmnd_line)
    print(f"{exe_fl_nm}.exe file compiled from {c_fl_nm}.c")
    return None


def run_c_file(fil_dir_abs, exe_fl_nm):  # Developing
    cmnd_line = f'cd /d "{fil_dir_abs}" && "{exe_fl_nm}.exe'
    print(f"Running {exe_fl_nm}.exe...\n")
    os.system(cmnd_line)
    return None


def test_c_compilation():  # Developing
    """Testing C compiler (GCC compiler) and using the following absolute paths"""
    # fil_dir_abs_pth = "D:\Personal Programming and electronics experiments\C programming"
    # c_fil_nm = "cTutorial2"  # This is a .c file. I.e. "cTutorial2" -> "cTutorial2.c"
    # exe_fil_nm = "Test3"

    crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
    fil_dir_abs_pth = crrnt_abs_pth+r"\WinTestFiles"
    c_fil_nm = r"c_test"  # This is a .c file. I.e. "cTutorial2" -> "cTutorial2.c"
    exe_fil_nm = r"c_win_test_out"

    print("Starting to compile...")
    compile_c(fil_dir_abs_pth, c_fil_nm, exe_fil_nm)
    print()
    print("Starting to run...")
    run_c_file(fil_dir_abs_pth, exe_fil_nm)
    print()
    print("Done running")
    return None


def debug_c_compilation(fil_dir_abs_pth, c_fil_nm, exe_fil_nm):  # Developing
    """Debugging C compiler (GCC compiler) and using the following absolute paths"""
    print("Starting to compile...")
    compile_c(fil_dir_abs_pth, c_fil_nm, exe_fil_nm)
    print()
    print("Starting to run...")
    run_c_file(fil_dir_abs_pth, exe_fil_nm)
    print()
    print("Done running")
    return None


def get_running_file_abs_pth():
    return os.path.abspath(os.path.dirname(__file__))


languages_to_check = ["C"]
before_using_steps(languages_to_check)
test_c_compilation()

# Copy when using library to compile DataCrunchers, i.e. less time to run when compared to Python
"""crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
fil_dir_abs_pth = crrnt_abs_pth+r"\WinTestFiles"
c_fil_nm = r"c_test"  # This is a .c file. I.e. "cTutorial2" -> "cTutorial2.c"
exe_fil_nm = r"c_win_test_out"

print("Starting to compile...")
compile_c(fil_dir_abs_pth, c_fil_nm, exe_fil_nm)
print()
print("Starting to run...")
run_c_file(fil_dir_abs_pth, exe_fil_nm)
print()
print("Done running")"""
