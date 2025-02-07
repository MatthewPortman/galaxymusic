import pytest
from pathlib import Path

pj = Path

#from galfitlib import __file__ as galfitlib_file
#LIBRARY_DIR = Path(galfitlib_file).parent.absolute()

from galfitlib.classes.parameters import GalfitParameter

#REG_TEST_DIR = pj(LIBRARY_DIR, "galfitlib", "tests")
#TEST_OUTPUT_DIR = pj(REG_TEST_DIR, "output")

global DEFAULT_VALUE
DEFAULT_VALUE = 10

# https://docs.pytest.org/en/stable/how-to/parametrize.html#pytest-mark-parametrize
# Used to automatically parametrize the test functions
# with two values of value and fix when desired
pytestmark = pytest.mark.parametrize(
        "value,fix",
        [
            (20, 0),
            (30, 1)
        ]
)
@pytest.fixture
def setup_GalfitParameter():
    yield GalfitParameter(
            value            = DEFAULT_VALUE,
            fix              = 0,
            name             = "parameter",
            parameter_number = "1",
            parameter_prefix = "A",
            comment          = "Comment"
    )

class TestGalfitParameter:
    def test_default(self, value, fix):
        param = GalfitParameter(0)
        assert param.value            == 0
        assert param.fix              == 1
        assert param.name             == ""
        assert param.parameter_number == "#"
        assert param.parameter_prefix == " "
        assert param.comment          == ""

    def test_init(self, setup_GalfitParameter, value, fix):
        assert setup_GalfitParameter.value            == DEFAULT_VALUE
        assert setup_GalfitParameter.fix              == 0
        assert setup_GalfitParameter.name             == "parameter"
        assert setup_GalfitParameter.parameter_number == "1"
        assert setup_GalfitParameter.parameter_prefix == "A"
        assert setup_GalfitParameter.comment          == "Comment"

    def test_set_value(self, setup_GalfitParameter, value, fix):
        setup_GalfitParameter.value         = value
        assert setup_GalfitParameter.value == value

    def test_set_fix(self, setup_GalfitParameter, value, fix):
        setup_GalfitParameter.fix         = fix
        assert setup_GalfitParameter.fix == fix

    def test_repr(self, setup_GalfitParameter, value, fix):
        assert repr(setup_GalfitParameter) == str(DEFAULT_VALUE)

        setup_GalfitParameter.value         = value
        assert repr(setup_GalfitParameter) == str(value)

    def test_str(self, setup_GalfitParameter, value, fix):
        pre_fix     = (
            f"{setup_GalfitParameter.parameter_prefix}"
            f"{setup_GalfitParameter.parameter_number}) "
            f"{DEFAULT_VALUE:<10}"
        )
        pre_comment = f"{pre_fix:<16}{setup_GalfitParameter.fix}"

        assert str(setup_GalfitParameter) == f"{pre_comment:<23} # {setup_GalfitParameter.comment}"

        setup_GalfitParameter.value = value
        setup_GalfitParameter.fix   = fix
        pre_fix = (
            f"{setup_GalfitParameter.parameter_prefix}"
            f"{setup_GalfitParameter.parameter_number}) "
            f"{setup_GalfitParameter.value:<10}"
        )
        pre_comment = f"{pre_fix:<16}{setup_GalfitParameter.fix}"

        assert str(setup_GalfitParameter) == f"{pre_comment:<23} # {setup_GalfitParameter.comment}"
