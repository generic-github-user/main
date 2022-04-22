import hashlib

# Based on https://stackoverflow.com/a/22058673
def hash_file(filepath, buffersize=65536):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(buffersize)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    return md5.hexdigest()
