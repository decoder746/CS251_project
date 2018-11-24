import os
import hashlib
from Crypto.Cipher import DES3
from Crypto.Cipher import AES
import requests, lxml.html
import sys
import struct
import subprocess
from bs4 import BeautifulSoup


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
	q = subprocess.Popen(['bash', 'bashenc.sh', '1', in_filename, key, outfilename])


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
	s = requests.session()
	url = sys.argv[2] + 'logout/'
	login = s.get(url)
	login_html = lxml.html.fromstring(login.text)
	hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
	form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
	a = []
	path = sys.argv[1] + "/user.txt"
	with open(path, 'r') as file:
		for line in file:
			a.append(line.split('\n')[0])
	form['username'] = a[0]
	form['password'] = a[1]
	response = s.post(url, data=form)
	soup = BeautifulSoup(response.text, "html.parser")
	shared = []
	for link in soup.findAll('input'):
		filepath = str(link.get('filepath'))[7:]
		if filepath[0:6] == "shared":
			dire = str(link.get('path'))[:-1]
			file = str(link.get('value'))
			shared.append(dire + file)
	
	s1 = requests.session()
	url1 = sys.argv[3] + 'block/'
	block = s.get(url1)
	block_html = lxml.html.fromstring(block.text)
	inputs = block_html.xpath(r'//form//input[@type="hidden"]')
	form1 = {x.attrib["name"]: x.attrib["value"] for x in inputs}
	form1['user'] = a[0]
	form1['turn'] = "1"
	response1 = s.post(url1, data=form1)
	p = subprocess.Popen(['python3', 'clientcron.py', url1, a[0]])
	s = requests.session()
	url = sys.argv[3] + 'uploads/'
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
	form['ifforced'] = 'no'
	b = []
	path2 = sys.argv[1] + "/file.txt"
	with open(path2, 'r') as file:
		for line in file:
			b.append(line[:-1])
	enc = []
	path3 = sys.argv[2]
	with open(path3, 'r') as file:
		for line in file:
			enc.append(line[:-1])
	b1 = []
	for x in b:
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
	dirpath = sys.argv[4]
	form['folen'] = dirpath
	for x in b1:
		if x[:-4] in shared:
			form['ifforced'] = 'sharedsync'
		else:
			form['ifforced'] = 'no'
		with open(x, 'rb') as f:
			file1 = {'myfile': f}
			form['filepath'] = x[len(dirpath):]
			form['md5'] = md5(x)
			response = s.post(url, files=file1, data=form)
			if response.status_code == 500:
				z = input("Do you want to overwrite " + x + " yes/no: ")
				if z == 'yes':
					form['ifforced'] = 'yes'
					response = s.post(url, files=file1, data=form)
					form['ifforced'] = 'no'
		os.remove(x)
	p.terminate()
	s2 = requests.session()
	url2 = sys.argv[3] + 'block/'
	block1 = s.get(url2)
	block1_html = lxml.html.fromstring(block1.text)
	inputs1 = block1_html.xpath(r'//form//input[@type="hidden"]')
	form2 = {x.attrib["name"]: x.attrib["value"] for x in inputs1}
	form2['user'] = sys.argv[2]
	form2['turn'] = "0"
	response2 = s.post(url2, data=form2)
except FileNotFoundError:
	print("Please log in to continue")
