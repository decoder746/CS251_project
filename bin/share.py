import os
import hashlib
from Crypto.Cipher import DES3
from Crypto.Cipher import DES
from Crypto.Cipher import AES
import requests, lxml.html
import sys
import struct
import subprocess


def md5(fname):
    hash_md5 = hashlib.md5()
    with open (fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def aes_encrypt_file(infile, encfile, key, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	fsz = os.path.getsize(infile)
	with open(encfile, 'wb') as fout:
	    fout.write(struct.pack('<Q', fsz))
	    fout.write(iv)
	    sz = 2048
	    with open(infile) as fin:
	        while True:
	            data = fin.read(sz)
	            n = len(data)
	            if n == 0:
	                break
	            elif n % 16 != 0:
	                data += ' ' * (16 - n % 16) # <- padded with spaces
	            encd = aes.encrypt(data)
	            fout.write(encd)


def rc4_encrypt_file(in_filename, out_filename, key):
	p = subprocess.Popen(['bash', 'bashenc.sh', '1', in_filename, key, out_filename])


def des3_encrypt_file(in_filename, out_filename, chunk_size, key, iv):
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


try:
	a = []
	path = sys.argv[6] + "/user.txt"
	with open(path, 'r') as file:
		for line in file:
			a.append(line.split('\n')[0])
	s = requests.session()
	url = sys.argv[4] + 'uploads/'
	# Here, we're getting the login page and then grabbing hidden form
	# fields.  We're probably also getting several session cookies too.
	login = s.get(url)
	login_html = lxml.html.fromstring(login.text)
	hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
	form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
	# print(form)
	# Now that we have the hidden form fields, let's add in our
	# username and password.
	form['user'] = a[0]
	form['ifforced'] = 'sharedadmin'
	enc = []
	path3 = sys.argv[3]
	x = sys.argv[1]
	y = ""
	with open(path3, 'r') as file:
		for line in file:
			enc.append(line[:-1])
	if enc[0] == "3DES":
		key1 = hashlib.md5(enc[1].encode())
		key = key1.digest()
		iv = "12345678".encode()
		y = x+".3ds"
		des3_encrypt_file(x, y, 8192, key, iv)
		b1.append(y)
	elif enc[0] == "AES":
		y = x+".aes"
		b1.append(y)
		iv = "1234567891234567".encode()
		aes_encrypt_file(x, y, key, iv)
	elif enc[0] == "RC4":
		y = x+".rc4"
		b1.append(y)
		key = enc[1]
		rc4_encrypt_file(x, y, key)
	dirpath = sys.argv[5]
	form['folen'] = dirpath
	with open(y, 'rb') as f:
		file1 = {'myfile': f}
		form['filepath'] = x[len(dirpath):]
		form['md5'] = md5(x)
		response = s.post(url, files=file1, data=form)
	s1 = requests.session()
	url1 = sys.argv[4] + 'uploads/'
	# Here, we're getting the login page and then grabbing hidden form
	# fields.  We're probably also getting several session cookies too.
	login1 = s1.get(url1)
	login1_html = lxml.html.fromstring(login1.text)
	hidden1_inputs = login1_html.xpath(r'//form//input[@type="hidden"]')
	form1 = {x.attrib["name"]: x.attrib["value"] for x in hidden1_inputs}
	# print(form)
	# Now that we have the hidden form fields, let's add in our
	# username and password.
	form['user'] = sys.argv[2]
	form['ifforced'] = 'sharedwith'
	with open(y, 'rb') as f:
		file1 = {'myfile': f}
		form['filepath'] = y[len(dirpath):]
		form['md5'] = md5(x)
		response = s.post(url, files=file1, data=form)
