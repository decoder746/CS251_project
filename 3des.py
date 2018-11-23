import os
from Crypto.Cipher import DES3 
import sys
def encrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
 
    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                   chunk += ' '.encode() * (16 - len(chunk) % 16)
                out_file.write(des3.encrypt(chunk))
 

def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_file.write(des3.decrypt(chunk))


from Crypto import Random
iv = Random.get_random_bytes(8)
key = sys.argv[1]
# with open('to_enc.txt', 'r') as f:
#     print 'to_enc.txt: %s' % f.read()
file_name = sys.argv[2]
efn = file_name + ".enc"
encrypt_file(file_name,efn, 8192, key, iv)
#decrypt_file('to_enc.enc', 'to_enc.dec', 8192, key, iv)
