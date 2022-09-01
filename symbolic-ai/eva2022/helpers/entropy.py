import zlib
from helpers.getsize import getsize

def estimateEntropy(value):
    return getsize(zlib.compress(value))/getsize(value)
