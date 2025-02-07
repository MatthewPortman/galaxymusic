import pytest
from pathlib import Path

pj = Path

import sys

from galfitlib import __file__ as galfitlib_file
LIBRARY_DIR = Path(galfitlib_file).parent.absolute()

from galfitlib.functions.helper_functions import *
from galfitlib.functions.helper_functions import _generate_get_set

REG_TEST_DIR = pj(LIBRARY_DIR, "tests")
TEST_OUTPUT_DIR = pj(REG_TEST_DIR, "output")
# TEST_DATA_DIR = pj(REG_TEST_DIR, "data")
# SAMPLE_DIR = pj(TEST_DATA_DIR, "samples")

# Unit test for subprocess_windows_path
@pytest.fixture(scope = "module")
def setup_test_dir():
    test_dir = pj(TEST_OUTPUT_DIR, "helper_functions_testing")
    test_dir.mkdir(exist_ok = True)

    yield test_dir

    # Tear down
    # Clean up the temporary directory and files after testing
    # Pytest tears down in FI-LO order so this should be the last thing to run
    for item in test_dir.iterdir():
        if item.is_dir():
            item.rmdir()
        else:
            item.unlink()
    test_dir.rmdir()


@pytest.fixture
def setup_find_files_glob(setup_test_dir):

    pj(setup_test_dir, "file1.txt").touch()
    pj(setup_test_dir, "file2.txt").touch()
    pj(setup_test_dir, "dir1").mkdir(exist_ok = True)
    pj(setup_test_dir, "dir2").mkdir(exist_ok = True)

    yield setup_test_dir


def test_find_files(setup_find_files_glob):
    result = find_files_glob(setup_find_files_glob, "*.txt", "f")
    expected = ["file1.txt", "file2.txt"]
    assert sorted(result) == sorted(expected)


def test_find_directories(setup_find_files_glob):
    result = find_files_glob(setup_find_files_glob, "*", "d")
    expected = ["dir1", "dir2"]
    assert sorted(result) == sorted(expected)


def test_find_all(setup_find_files_glob):
    result = find_files_glob(setup_find_files_glob, "*", "all")
    expected = ["file1.txt", "file2.txt", "dir1", "dir2"]
    assert sorted(result) == sorted(expected)


# TODO: NECESSARY FOR OLD REG TESTS
# Remove upon updating all tests
@pytest.fixture
def setup_sp():
    stdout_file = "unit_test_std_output.txt"
    stdout_dest = pj(TEST_OUTPUT_DIR, stdout_file)

    yield stdout_dest
    # if stdout_dest.exists():
    #     stdout_dest.unlink()


def test_sp_touch_command(setup_sp):
    touch_stdout = sp(f"touch {subprocess_windows_path(setup_sp)}")
    assert not touch_stdout.stderr, f"Touch failed in helper_functions unit test. {touch_stdout.stderr}"


# def test_subprocess_windows_path():
#     path = Path("C:/Users/test")
#     result = subprocess_windows_path(path)
#     expected = PurePosixPath("/mnt/c/Users/test")
#     print(result, expected)
#     assert result == expected

# # Writing this as a fixture in case I decide to tear down separately
# @pytest.fixture
# def setup_export_to_py(setup_test_dir):
#     notebook_name   = pj(setup_test_dir, "test_notebook")
#     output_filename = pj(setup_test_dir, "test_output.py")
#
#     yield notebook_name, output_filename
#     # if Path(output_filename).exists():
#     #     Path(output_filename).unlink()
#
# def test_export_to_py(mocker, setup_export_to_py):
#     notebook_name, output_filename = setup_export_to_py
#     mocker.patch('helper_functions.in_notebook', return_value = True)
#     mocker.patch('helper_functions.sp', return_value = subprocess.CompletedProcess(
#             args = [],
#             returncode = 0,
#             stdout = "test_notebook.py")
#                  )
#     export_to_py(notebook_name, output_filename)
#     assert Path(output_filename).exists()

# Leaving this in for when I eventually remove the other sp test
def test_sp_command():
    result = sp("echo Hello")
    assert result.stdout.strip() == "Hello"


@pytest.fixture
def setup_test_files(setup_test_dir):

    test_files = [pj(setup_test_dir, f"fake_{i}.fake") for i in range(10)]
    _ = [i.touch() for i in test_files]

    yield test_files


def test_exists(setup_test_files):
    for file in setup_test_files:
        assert exists(file)


def test_rm_files(setup_test_files):
    rm_files(*setup_test_files)
    for file in setup_test_files:
        assert not file.exists()


def test_rm_files_exception():
    result = rm_files("fakest_of_them_all.fake")
    assert isinstance(result[0], FileNotFoundError)

def test_generate_get_set():
    input_dict = {"x": "_x"}
    result = _generate_get_set(input_dict)
    expected = ("@property\n"
                "def x(self):\n"
                "    return self._x\n"
                "            \n"
                "@x.setter\n"
                "def x(self, new_val):\n"
                "    self._x = new_val\n"
                "\n")
    assert result == expected