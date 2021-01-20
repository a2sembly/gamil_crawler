#-*- coding: utf-8 -*-
import hashlib

def calc_file_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5 = hashlib.md5(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    return {'MD5':md5,'sha256': sha256}