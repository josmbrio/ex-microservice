from util_functions.api_key_validation import is_valid_api_key


def test_is_valid_api_key():
    assert is_valid_api_key('1q1q2w2w3e3e4r4r') is False
