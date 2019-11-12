import hashlib


# MD5
def md5(string, secret=''):
    return hashlib.md5((string + secret).encode(encoding='utf-8')).hexdigest()
