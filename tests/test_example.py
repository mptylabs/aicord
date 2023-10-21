def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a} != {b}")


def test_addition():
    assert_equal(1 + 1, 2)
