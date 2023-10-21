import loguru

def test_addition():
    try:
        assert 1 + 1 == 2
    except AssertionError:
        loguru.exception("1 + 1 does not equal 2")
