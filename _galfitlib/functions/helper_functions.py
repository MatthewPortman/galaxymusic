#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path, PurePosixPath #, PurePath

# Short for path join but in pathlib form
pj = Path

import shutil
import subprocess
import os
from os import environ
from sys import platform
from types import GeneratorType


# In[ ]:


from _galfitlib import __file__ as galfitlib_file
LIBRARY_DIR = Path(galfitlib_file).parent.absolute()


# In[ ]:


# Provide Path overwrite for working with Windows + WSL
def subprocess_windows_path(path):
    # To avoid this see:
    # https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html#create-wsl-interpreter
    # for working on windows with Pycharm + WSL
    if platform == "win32":
        path_split = path.parts
        return PurePosixPath(f"/mnt/{path_split[0][0].lower()}", *path_split[1:])
    else:
        return Path(path)


# In[ ]:


# For debugging purposes
from IPython import get_ipython
def in_notebook():
    ip = get_ipython()
    
    if ip:
        return True
    else:
        return False


# In[ ]:


def export_to_py(notebook_name, output_filename = ""):
    
    notebook_name   = Path(notebook_name)
    output_filename = Path(output_filename)
    
    notebook_name = notebook_name.with_suffix(".ipynb")
    
    # For some reason there's an issue with setting locales when using WSL
    # remote environment in PyCharm. This is a tentative workaround.
    if "WSL_DISTRO_NAME" in environ:
        environ["LC_ALL"] = "C"
    
    if in_notebook():
        print(f"Converting {notebook_name}")
        
        result = get_ipython().getoutput('jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to script {notebook_name}')
        
        if output_filename:
            print(result)
            filename = Path(result[1].split()[-1])
            output_filename = output_filename.with_suffix(".py")
            
            try:
                #os.rename(filename, output_filename)
                filename.rename(output_filename).absolute()
                
            except FileNotFoundError as f:
                print(f"Could not find {filename} per error {f}...")
                print("Output from nbconvert: ", *result)


# In[ ]:


def sp(cmd_str, capture_output = True, timeout = None, **kwargs):
    
    shell = True
    
    if platform == "win32":
        shell = False
        # For some reason Windows needs some dummy string before the actual command
        cmd_str = f"dummy {cmd_str}"
        
    # For some reason there's an issue with setting locales when using WSL
    # remote environment in PyCharm. This is a tentative workaround.
    elif "WSL_DISTRO_NAME" in environ:
        environ["LC_ALL"] = "C"
    
    # Wrapping subprocess because it is a pain in the butt to call it with all these kwargs
    return subprocess.run(
            cmd_str, 
            capture_output = capture_output,
            text           = True,
            shell          = shell,
            timeout        = timeout,
            # Platform check used more for debugging purposes than anything else... 
            executable     = shutil.which("bash"),
            #stdin          = subprocess.PIPE,
            **kwargs
    )


# In[ ]:


def check_programs():

   # This seems to work in Python directly so I'm leaving it as-is
   # Checking galfit
   # TODO: Is this needed any more?
   #hostname = sp(f"hostname").stdout.split(".")[0]
   
   #galfit_cmd = shutil.which(f"galfit_{hostname}")
   #if not galfit_cmd:
   galfit_cmd  = shutil.which(f"galfit")

   # Checking fitspng
   fitspng_cmd = shutil.which("fitspng")

   # Checking exact python3 call
   python_cmd  = shutil.which("python3")
   
   # Checking sourceextractor
   source_extractor_cmd = shutil.which(f"sex")

   return {
       "galfit"           : galfit_cmd, 
       "fitspng"          : fitspng_cmd, 
       "python"           : python_cmd, 
       "source_extractor" : source_extractor_cmd,
   }

# To be set upon import of this module
# global run_galfit
# global run_fitspng
# global run_python
program_dict = check_programs()
RUN_GALFIT           = program_dict["galfit"]
RUN_FITSPNG          = program_dict["fitspng"]
RUN_PYTHON           = program_dict["python"]
RUN_SOURCE_EXTRACTOR = program_dict["source_extractor"]


# In[ ]:


def find_files(search_dir = ".", search_pattern = "*", filetype = "f"):

    if filetype in ("d", "folder", "dir", "directory"):
        type_cmd = "d"

    elif filetype in ("f", "file"):
        type_cmd = "f"

    else:
        type_cmd = filetype

    search_dir = subprocess_windows_path(search_dir)
    result = sp(f"find -L {search_dir} -maxdepth 1 -type {type_cmd} -name \"{search_pattern}\"")
    return [Path(i).name for i in result.stdout.split("\n") if i]


# In[ ]:


def find_files_glob(search_dir = ".", search_pattern = "*", filetype = "f"):
            
    # TODO: Make sure this still works as anticipated in the running scripts
    # TODO: Also confirm glob follows symlinks
    # It could be another case of Python being too slow to update with the file system
    
    # results = sp(f"find -L {pj(search_dir)} -maxdepth 1 -type {type_cmd} -name \"{search_pattern}\"")
    results = Path(search_dir).glob(search_pattern)
    
    if filetype in ("d", "folder", "dir", "directory"):
        return [i.name for i in results if i and i.is_dir()]
        
    elif filetype in ("f", "file"):
        return [i.name for i in results if i and i.is_file()]
    
    else:
        return [i.name for i in results if i]


# In[ ]:


# Writing this to do generic deletion without calling subprocess
def rm_files(*args):
    # Assume list/tuple given by accident
    if not args:
        print("Nothing was fed into rm_files...")
        return None

    if isinstance(args[0], (tuple, list, GeneratorType)):
        print("Please expand your iterable(s) before feeding into rm_files, thanks!")
        print("Assuming the first argument is the only thing that needs to be deleted.")
        args = args[0]
        
    if isinstance(args, str):
        args = [args]
        
    # Thanks! https://stackoverflow.com/a/8915613
    # May the list comp live on
    def catch(func, *argss, handle=lambda e : e, **kwargs):
        try:
            return func(*argss, **kwargs)
        except FileNotFoundError as e:
            return handle(e)
    
    # unlink, i.e. delete file
    return [catch(Path.unlink, Path(i)) for i in args]


# In[ ]:


# Writing this to replace os.path.exists since that's too slow
def exists(filename):
    filename = subprocess_windows_path(filename)
    results = sp(f"[ -e {filename} ] && echo 1 || echo 0")
    return bool(int(results.stdout))


# In[ ]:


# This is simply a convenience method for generating the string used to
# create the get and set methods for the classes
def _generate_get_set(input_dict): #, exclude = []):
    to_print_str = ""
    for key,v in input_dict.items():
        to_print_str += f"""@property
def {key}(self):
    return self.{v}
            
@{key}.setter
def {key}(self, new_val):
    self.{v} = new_val

"""
    return to_print_str


# In[ ]:


if __name__ == "__main__":
    # The below are imported and directories are made
    from galfitlib.tests.reg_test import *
    
    # REG_TEST_DIR    = pj(_LIBRARY_DIR, "tests")
    # TEST_OUTPUT_DIR = pj(REG_TEST_DIR, "output")
    # TEST_DATA_DIR   = pj(REG_TEST_DIR, "data")
    # SAMPLE_DIR      = pj(TEST_DATA_DIR, "samples")


# In[ ]:


# Unit test for sp
# The components and things will overwrite files rather than append
# so the second touch is unnecessary
if __name__ == "__main__":
    stdout_file   = "unit_test_std_output.txt"
    # writeout_file = "UnitTestWriteOuput.txt"
    
    stdout_dest   = pj(TEST_OUTPUT_DIR, stdout_file)
    # writeout_dest = pj(_MODULE_DIR, "RegTest", "TestOutput", writeout_file)
    
    touch_stdout  = sp(f"touch {subprocess_windows_path(stdout_dest)}")
    # touch_writeout = sp(f"touch {writeout_dest}")
    
    # if touch_stdout.stderr or touch_writeout.stderr:
    if touch_stdout.stderr:
        print("Touch failed in helper_functions unit test.")
        print(touch_stdout.stderr)
        # print(touch_writeout.stderr)
        raise(Exception())


# In[ ]:


# Unit test for rm files
if __name__ == "__main__":
    # Cleaning up old reg test (if it was previously run)
    # if TEST_OUTPUT_DIR.exists():
    #     print("Cleaning up old unit/regression test files from TestOutput directory.")
    #     shutil.rmtree(TEST_OUTPUT_DIR)
    # 
    # TEST_OUTPUT_DIR.mkdir()
    
    fake_files = [pj(TEST_OUTPUT_DIR, f"fake_{i}.fake") for i in range(10)]
    
    for fake in fake_files:
        with open(fake, mode = 'a'): pass
    
    # Check try catch
    fake_files.append(pj(TEST_OUTPUT_DIR, "fakest_of_them_all.fake"))
    
    # Check warning message
    print(rm_files(fake_files)) #*fake_files
    assert not list(Path(TEST_OUTPUT_DIR).glob(f"fake_*")), "Files were not deleted, something went wrong!!!"


# In[ ]:


# Unit test for list_files
if __name__ == "__main__":
    
    print(sorted(find_files(pj(TEST_DATA_DIR, "in"),  "*.fits", "f")))
    print()
    print(sorted(find_files(pj(TEST_DATA_DIR, "out"), "123*", "d")))


# In[ ]:


# Unit test for exists
if __name__ == "__main__":
    
    print("Does test in exist?",  exists(pj(TEST_DATA_DIR, "in")))
    print("Does test out exist?", exists(pj(TEST_DATA_DIR, "out")))


# In[ ]:


# Unit test for generate_get_set
if __name__ == "__main__":
    assert _generate_get_set({"x" : "_x"}) =="""@property
def x(self):
    return self._x
            
@x.setter
def x(self, new_val):
    self._x = new_val

"""


# In[ ]:


if __name__ == "__main__":   
    # Exporting the helper functions 
    export_to_py("helper_functions", pj(LIBRARY_DIR, "functions", "helper_functions"))

