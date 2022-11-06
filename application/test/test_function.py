from util_functions.api_key_validation import is_valid_api_key


def test_is_valid_api_key():
    assert is_valid_api_key('xxxxxxxx') == False
