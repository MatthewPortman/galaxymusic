import pytest
from pathlib import Path

pj = Path

# from galfitlib import __file__ as galfitlib_file
# LIBRARY_DIR = Path(galfitlib_file).parent.absolute()

from galfitlib.classes.parameters import MultiParameter, ntMultiParameter, ntMultiParameter

# REG_TEST_DIR = pj(LIBRARY_DIR, "galfitlib", "tests")
# TEST_OUTPUT_DIR = pj(REG_TEST_DIR, "output")

global DEFAULT_VALUE
DEFAULT_VALUE = (10, 20)

global DEFAULT_FIX
DEFAULT_FIX = (1, 1)

# https://docs.pytest.org/en/stable/how-to/parametrize.html#pytest-mark-parametrize
# Used to automatically parametrize the test functions
# with two values of value and fix when desired
pytestmark = pytest.mark.parametrize(
        "value,fix",
        [
            ((20.0, 30.0), (0.0, 0.0)),
            ((30.0, 40.0), (0.0, 1.0)),
            ((30.1, 40.1), ("", "")),
        ]
)
@pytest.fixture
def setup_MultiParameter():
    yield MultiParameter(
            value            = DEFAULT_VALUE,
            fix              = DEFAULT_FIX,
            name             = "multi-parameter",
            parameter_number = "1",
            parameter_prefix = "X",
            comment          = "Comment-Comment"
    )

class TestMultiParameter:
    def test_default_tuple_input(self, value, fix):
        param = MultiParameter((0, 1))
        assert param.value            == ntMultiParameter(0, 1)

        assert param.x                == 0
        assert param.value.x          == 0

        assert param.y                == 1
        assert param.value.y          == 1

        assert param.fix              == ntMultiParameter("", "")

        assert param.fix_x            == ""
        assert param.fix.x            == ""

        assert param.fix_y            == ""
        assert param.fix.y            == ""

        assert param.name             == ""
        assert param.parameter_number == "#"
        assert param.parameter_prefix == " "
        assert param.comment          == ""

    def test_default_single_input(self, value, fix):
        param = MultiParameter(
                x = 0,
                y = 1,
                fix_x = "",
                fix_y = " "
        )
        assert param.value == ntMultiParameter(0, 1)

        assert param.x       == 0
        assert param.value.x == 0

        assert param.y       == 1
        assert param.value.y == 1

        assert param.fix   == ntMultiParameter("", " ")

        assert param.fix_x == ""
        assert param.fix.x == ""

        assert param.fix_y == " "
        assert param.fix.y == " "

    def test_init(self, setup_MultiParameter, value, fix):
        assert setup_MultiParameter.value            == ntMultiParameter(*DEFAULT_VALUE)
        assert setup_MultiParameter.fix              == ntMultiParameter(*DEFAULT_FIX)
        assert setup_MultiParameter.name             == "multi-parameter"
        assert setup_MultiParameter.parameter_number == "1"
        assert setup_MultiParameter.parameter_prefix == "X"
        assert setup_MultiParameter.comment          == "Comment-Comment"

    def test_attribute_set_priority(self, value, fix):
        param = MultiParameter(
                x     = value[0],
                y     = value[1],
                value = [10000, 2],
                fix_x = fix[0],
                fix_y = fix[1],
                fix   = ["2", "100000"]
        )

        assert param.value == ntMultiParameter(value[0], value[1])
        assert param.fix   == ntMultiParameter(fix[0], fix[1])

    def test_set_x_value(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.x               = value[0]
        assert setup_MultiParameter.x       == value[0]
        assert setup_MultiParameter.value.x == value[0]

    def test_set_y_value(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.y               = value[1]
        assert setup_MultiParameter.y       == value[1]
        assert setup_MultiParameter.value.y == value[1]

    def test_set_tuple_value(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.value         = value
        assert setup_MultiParameter.value == ntMultiParameter(*value)

        assert setup_MultiParameter.x       == value[0]
        assert setup_MultiParameter.value.x == value[0]

        assert setup_MultiParameter.y       == value[1]
        assert setup_MultiParameter.value.y == value[1]

    def test_check_value_type(self, setup_MultiParameter, value, fix):
        with pytest.raises(AssertionError):
            setup_MultiParameter.value = "not a list or tuple"

    def test_check_value_len(self, setup_MultiParameter, value, fix):
        with pytest.raises(AssertionError):
            # Should fail before it tries to convert to float
            setup_MultiParameter.value = ["this is not appropriate"]

    def test_set_x_fix(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.fix_x         = fix[0]
        assert setup_MultiParameter.fix_x == fix[0]
        assert setup_MultiParameter.fix.x == fix[0]

    def test_set_y_fix(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.fix_y         = value[0]
        assert setup_MultiParameter.fix_y == value[0]
        assert setup_MultiParameter.fix.y == value[0]

    def test_set_tuple_fix(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.fix         = fix
        assert setup_MultiParameter.fix == ntMultiParameter(*fix)

        assert setup_MultiParameter.fix_x == fix[0]
        assert setup_MultiParameter.fix.x == fix[0]

        assert setup_MultiParameter.fix_y == fix[1]
        assert setup_MultiParameter.fix.y == fix[1]

    def test_set_fix_by_string(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.fix         = "0 1"
        assert setup_MultiParameter.fix == ntMultiParameter(0.0, 1.0)

    def test_set_fix_by_string_list(self, setup_MultiParameter, value, fix):
        setup_MultiParameter.fix         = ["0", "1"]
        assert setup_MultiParameter.fix == ntMultiParameter("", "")

    def test_set_fix_exception(self, setup_MultiParameter, value, fix):
        with pytest.raises(Exception):
            setup_MultiParameter.fix = {0, 1}

    def test_repr(self, setup_MultiParameter, value, fix):
        assert repr(setup_MultiParameter) == str(ntMultiParameter(*DEFAULT_VALUE))

        setup_MultiParameter.value         = value
        assert repr(setup_MultiParameter) == str(ntMultiParameter(*value))

    # There's no pretty way to do this, so I choose to hardcode some tests
    # def test_str(self, setup_MultiParameter, value, fix):
    #     pass

    @pytest.mark.parametrize( "x, y, fix_x, fix_y, expected",
        [
            (
                    DEFAULT_VALUE[0],
                    DEFAULT_VALUE[1],
                    DEFAULT_FIX[0],
                    DEFAULT_FIX[1],
                    " #) 10 20       1  1    # "
            ),
            (10.1, 20,   0,  1,  " #) 10.1000 20  0  1    # "),
            (10.1, 20.1, 1,  0,  " #) 10.1000 20.1000 1  0 # "),
            (10.1, 20.1, "", "", " #) 10.1000 20.1000     # ")
        ]
                              )
    def test_MultiParameter_str(self, x, y, fix_x, fix_y, expected, value, fix):
        new_MP = MultiParameter(
                x = x,
                y = y,
                fix_x = fix_x,
                fix_y = fix_y
        )
        assert str(new_MP) == expected

def test_ntMultiParameter(value, fix):
    nt = ntMultiParameter(*value)
    assert nt.x == value[0]
    assert nt.y == value[1]

    nt = ntMultiParameter(*fix)
    assert nt.x == fix[0]
    assert nt.y == fix[1]
