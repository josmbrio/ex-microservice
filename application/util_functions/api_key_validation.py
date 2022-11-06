def is_valid_api_key(request_api_key):
    api_key = '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c'
    if api_key == request_api_key:
        return True
    else:
        return False
