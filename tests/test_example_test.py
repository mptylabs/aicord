import pytest
from test_example import test_addition

def test_test_addition():
    with pytest.raises(AssertionError):
        test_addition(1, 2)
