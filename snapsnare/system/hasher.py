import hashlib


def sha256(value, encoding='utf-8'):
    hash = hashlib.sha256()
    hash.update(value.encode(encoding))
    return hash.hexdigest()
