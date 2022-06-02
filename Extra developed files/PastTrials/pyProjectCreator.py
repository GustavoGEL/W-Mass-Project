import os
from platform import system
from subprocess import Popen, PIPE, STDOUT

def libraryDescription():
    print("Library that creates a virtual environment and install the needed libraries for a given directory and file name")
    return None


def printPreRequisits():
    print("Before running this library, make sure that Python and pip are correctly installed. Also, create a folder for the new project")
    return None

def usageInstructions():
    print("""Usage instructions:
1) Create a new folder with the new project name
2) Copy this library and functions libraries files to that folder or substitute crrnt_abs_pth, aka project_abs_path
3) Open VS Code and open this new folder there or do the past steps from VS Code
4) Run this script to create the virtual environment
5) AN extra folder, __pycache__, will be created to import the necessary libraries, i.e. windowsFuncts, etc
6) [Developing] Install the necessary libraries from requirements.txt""")
    return None


def checkIfFileExists(abs_pth_dir, fl_nm):
    crrnt_os = system()
    print(f"Current absolute path: {abs_pth_dir}")
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        # Check if file exists in the given directory
        if os.path.exists(abs_pth_dir+"/"+fl_nm):
            return True
        else:
            return False
    else:
        errLine = f"Got operating system: {crrnt_os}, not developed for this operating system yet"
        raise Exception(errLine)


def checkPip():
    """Function that checks if pip is correctly intalled"""
    print("Checking if pip is correctly installed")
    proc = Popen(
        ['pip', '-m', 'pip', '--version',],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
    )
    stdout_value, stderr_value = proc.communicate()
    if not stderr_value:
        # print(f"stderr_value: {stderr_value}")  # Error, expect None
        print(f"Pip version: {stdout_value} (i.e. correctly installed)")
        return None
    else:
        print(f"stdout_value: {stdout_value}")  # Output, expect many lines
        errLine = f"Pip may not be installed, error gotten: {stderr_value}"  # Error, expect None
        raise Exception(errLine)


def checkPython():
    proc = Popen(
        ['python', '--version',],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
    )
    stdout_value, stderr_value = proc.communicate()
    if not stderr_value:
        # print(f"stderr_value: {stderr_value}")  # Error, expect None
        print(f"Python version: {stderr_value} (i.e. correctly installed)")
        return None
    else:
        print(f"stdout_value: {stdout_value}")  # Output, expect many lines
        errLine = f"Python not installed correctly, error gotten: {stderr_value}"  # Error, expect None
        raise Exception(errLine)


def updatePip():
    print("Updating pip library")
    proc = Popen(
        ['python', '-m', 'pip', 'install', '--user', '--upgrade', 'pip'],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
    )
    stdout_value, stderr_value = proc.communicate()
    if not stderr_value:
        print(f'Pip library was correctly updated')
        return None
    else:
        print(f"stdout_value: {stdout_value}")  # Output, expect many lines
        errLine = f"Pip may not have been updated, error gotten: {stderr_value}"  # Error, expect None
        raise Exception(errLine)


def installLib(lib_nam, lib_ver="latest"):
    print("Installing virtualenv library")
    if lib_ver == "latest":
        lib_parm = lib_nam
    else:
        lib_parm = lib_nam+"=="+lib_ver
    proc = Popen(
        ['pip', 'install', lib_parm,],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
    )
    stdout_value, stderr_value = proc.communicate()
    if not stderr_value:
        print(f'Library "{lib_nam}" correctly installed')
        return None
    else:
        print(f"stdout_value: {stdout_value}")  # Output, expect many lines
        errLine = f"Library '{lib_nam}' may not be installed, error gotten: {stderr_value}"  # Error, expect None
        raise Exception(errLine)


def createMetaFile(abs_dir_pth):
    print("Creating meta file for future runs...")
    abs_fil_nam = abs_dir_pth+"/metaRun.txt"
    with(open(abs_fil_nam, "w")) as fl:
        fl.write("FirstRun=Done\n")
    return None


def executeWinCmndLines(cmnd_lns_arr):
    full_cmnd_lin = ""
    for cmnd_lin in range(len(cmnd_lns_arr)-1):
        full_cmnd_lin += cmnd_lns_arr[cmnd_lin]+" && "
    full_cmnd_lin += cmnd_lns_arr[-1]
    os.system(full_cmnd_lin)
    return None


def createVenv(currnt_abs_pth, venv_nan):
    print("Creating venv...")
    # First, make a new directory and inside a new directory of the given name
    crrnt_os = system()
    if crrnt_os == "Windows":
        # Create virtual environment at .venv directory
        cmnd_lins = [f'cd /d "{currnt_abs_pth}"', f"py -m venv {venv_nan}"]
        executeWinCmndLines(cmnd_lins)

        # Check if the new directory already exists
        if not os.path.exists(currnt_abs_pth+"/"+venv_nan):
            stderr_value = "Not exists"
        else:
            stderr_value = None
        if not stderr_value:
            print(f'Virtual environment was created at "{currnt_abs_pth}"')
            return None
        else:
            errLine = f"Error creating venv at '{currnt_abs_pth}', error gotten: {stderr_value}"  # Error, expect None
            raise Exception(errLine)
    else:
        errLine = f"Got operating system: {crrnt_os}, not developed for this operating system yet"
        raise Exception(errLine)


def howToActivateVenv(currnt_abs_pth, venv_nan):
    print("Initialising venv...")
    crrnt_os = system()
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        cmnd_line = f'cd /d "{currnt_abs_pth}" && {venv_nan}\\Scripts\\activate'
        print("Open the CMD and copy the following line to activate the virtual environment:")
        print(cmnd_line)
        print("To deactivate the virtual environment, type 'deactivate' on the CMD")
        print("Use 'clear' on the VS Code CMD to clear it")
        return None
    else:
        errLine = f"Got operating system: {crrnt_os}, not developed for this operating system yet"
        raise Exception(errLine)


def installLibs(currnt_abs_pth, venv_nan):
    print("Initialising venv and installing necessary libraries...")
    crrnt_os = system()
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        print("Activating virtual environment and installing libraries from 'requirements.txt' using the command line:")
        cmnd_line = f'cd /d "{currnt_abs_pth}" && {venv_nan}\\Scripts\\activate'
        cmnd_line += " && pip install -r requirements.txt"
        print(cmnd_line)
        print()
        print("Trying to run the command from CMD using Python")
        os.system(cmnd_line)
        return None
    else:
        errLine = f"Got operating system: {crrnt_os}, not developed for this operating system yet"
        raise Exception(errLine)


def deactivateVenv():
    print("To deactivate the virtual environment, type 'deactivate' on the CMD")
    return None


def createPyFile(currnt_abs_pth, py_fl_nm):
    print(f"Creating main file with name {py_fl_nm}...")
    crrnt_os = system()
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        print("Creating main file")
        abs_fl_nm = currnt_abs_pth+"\\"+py_fl_nm+".py"
        with open(abs_fl_nm, "w") as fl:
            fl.write('import time\n\nprint("Hello, installed venv works!")\ntime.sleep(3)  # Wait 3s to visualise, in case that the program runs in a new window\n')
        return None
    else:
        errLine = f"Got operating system: {crrnt_os}, not developed for this operating system yet"
        raise Exception(errLine)


def createCommandsFile(currnt_abs_pth, venv_nan, py_fl_nm):
    print(f"Creating main file with name {py_fl_nm}...")
    crrnt_os = system()
    print(f"Platform system: {crrnt_os}")
    if crrnt_os == "Windows":
        print("Creating commands file")
        abs_fl_nm = currnt_abs_pth+"\\UsefulCommands.txt"
        fl_content = f"""Useful commands for Windows:

Change directory to main/root directory:
cd /d "{currnt_abs_pth}"

Activate virtual environment:
{venv_nan}\\Scripts\\activate

Run {py_fl_nm} file (after initiating virtual environment):
{py_fl_nm}.py

Deactivate virtual environment:
deactivate

Single command:
cd /d "{currnt_abs_pth}" && {venv_nan}\\Scripts\\activate && {py_fl_nm}.py

Linux/VSCode terminal:
cd "{currnt_abs_pth}"; .\\{venv_nan}\\Scripts\\activate; .\{py_fl_nm}.py
"""
        with open(abs_fl_nm, "w") as fl:
            fl.writelines(fl_content)
        return None
    else:
        errLine = f"Got operating system: {crrnt_os}, not developed for this operating system yet"
        raise Exception(errLine)


def currentDeveloping():
    print("""1) Creating VenvCreator library (include creator, initialiser, editor and deleter)
2) Create a LibraryInstaller library (at a directory anda python) (include installer (one library at the time), installer from file (i.e. requirements.txt) and uninstaller library)""")
    return None


def popenExample():
    """Main documentation: https://docs.python.org/3/library/subprocess.html"""
    exmpl_str = """p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]"""
    return exmpl_str


def pyVenvLibraryProjectCreator(crrnt_abs_pth, venv_nm, main_py_nam):
    """Function that creates (if possible) and installs (if possible) a virtual environment at a directory, 
    with the given libraries in a requirements.txt file at the same directory as the one given and creates 
    a file with useful commands to use on the CMD (at least for Windows now). It also checks that Python 
    and pip are installed, it updates pip, installs virtualenv library and uses them to perform its functions.
    It also creates a metaRun.txt file that contains extra information about the creation of the virtual 
    environment. I.e. if it is the first time that the function runs, i.e. install everything, else just 
    check if needed"""

    # currentDeveloping()
    print("Hello, starting Python Project Creator")
    # 0) Check if metaRun.txt file exists on this directory, else if the installing script has been ran before
    if not checkIfFileExists(crrnt_abs_pth, "metaRun.txt"):
        # 1) Run the following lines if running from the first time
        # Check Python, pip, update pip and install the library. Just needed once as this is the general Python
        checkPython()
        checkPip()
        updatePip()
        installLib('virtualenv', 'latest')
        createMetaFile(crrnt_abs_pth)

    # 2) Create virtual environment
    # Create virtual environment
    createVenv(crrnt_abs_pth, venv_nm)

    # 3) Install libraries from file 'requirements.txt'
    # Install library on this venv (if any) by activating it and using pip to install them
    if checkIfFileExists(crrnt_abs_pth, "requirements.txt"):
        installLibs(crrnt_abs_pth, venv_nm)
    howToActivateVenv(crrnt_abs_pth, venv_nm)

    # 4) Checking if want a main file to be created with the new environment
    createPyFile(crrnt_abs_pth, main_py_nam)

    # 5) Creating file with useful command shortcuts for this project
    createCommandsFile(crrnt_abs_pth, venv_nm, main_py_nam)

    print("Done")
    return None


def test_library():
    # Main code
    crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))  # Assuming that this script exists at the directory where the new project will be created
    # crrnt_abs_pth = "D:\Programming\Testing\LibraryInstaller"
    venv_nm = "env"
    main_py_nam = "MainTest"  # .py

    # currentDeveloping()
    print("Hello, starting Python Project Creator")
    # 0) Check if metaRun.txt file exists on this directory, else if the installing script has been ran before
    if not checkIfFileExists(crrnt_abs_pth, "metaRun.txt"):
        # 1) Run the following lines if running from the first time
        # Check Python, pip, update pip and install the library. Just needed once as this is the general Python
        checkPython()
        checkPip()
        updatePip()
        installLib('virtualenv', 'latest')
        createMetaFile(crrnt_abs_pth)

    # 2) Create virtual environment
    # Create virtual environment
    createVenv(crrnt_abs_pth, venv_nm)

    # 3) Install libraries from file 'requirements.txt'
    # Install library on this venv (if any) by activating it and using pip to install them
    if checkIfFileExists(crrnt_abs_pth, "requirements.txt"):
        installLibs(crrnt_abs_pth, venv_nm)
    howToActivateVenv(crrnt_abs_pth, venv_nm)

    # 4) Checking if want a main file to be created with the new environment
    createPyFile(crrnt_abs_pth, main_py_nam)

    # 5) Creating file with useful command shortcuts for this project
    createCommandsFile(crrnt_abs_pth, venv_nm, main_py_nam)

    print("Done")
    return None


# Creating venv and installing necessary libraries at dir
# For using on djreact. Create two more directories on this directory: 
# 1) 'backend' (where django and python will be installed)
# 2) 'frontend' (where react will be installed)
crrnt_abs_pth = os.path.dirname(os.path.realpath(__file__))
venv_nm = "WindowsVenv"
# extra_dirs = ["backend", "frontend"]
main_py_nam = "VenvTest"
pyVenvLibraryProjectCreator(crrnt_abs_pth, venv_nm, main_py_nam)

# Extra notes, for this directory,
# 1) Use the installer when using Windows and testing everything but ROOT
# 2) Run normally when using Linux as the main (current) Python in Linux contains ROOT, numpy and matplotlib
