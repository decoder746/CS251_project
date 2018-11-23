import pyAesCrypt
import sys

# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
password = sys.argv[1]
file_name = sys.argv[2]
# encrypt
encryptedfile_name = file_name + '.enc'
pyAesCrypt.encryptFile(file_name,encryptedfile_name, password, bufferSize)
# decrypt
#pyAesCrypt.decryptFile("data.txt.aes", "dataout.txt", password, bufferSize)