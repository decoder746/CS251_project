import shutil
from Crypto.Cipher import AES
import struct
import requests
import lxml.html
import sys
from bs4 import BeautifulSoup
import os
from Crypto.Cipher import DES3
import hashlib
import subprocess


def md5(fname):
	hash_md5 = hashlib.md5()
	with open(fname, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


def aes_decrypt_file(encfile, verfile, key):
	with open(encfile, 'rb') as fin:
		fsz = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
		iv = fin.read(16)
		aes = AES.new(key, AES.MODE_CBC, iv)
		with open(verfile, 'wb') as fout:
			while True:
				data = fin.read(fsz)
				n = len(data)
				if n == 0:
					break
				decd = aes.decrypt(data)
				n = len(decd)
				if fsz > n:
					fout.write(decd)
				else:
					fout.write(decd[:fsz])
				fsz -= n


def rc4_decrypt_file(in_filename, out_filename,key):
	p = subprocess.Popen(['bash', 'bashenc.sh', '2', in_filename, key, out_filename])



def des3_decrypt_file(in_filename, out_filename, chunk_size, key, iv):
	des3 = DES3.new(key, DES3.MODE_CFB, iv)
	with open(in_filename, 'rb') as in_file:
		with open(out_filename, 'wb') as out_file:
			while True:
				chunk = in_file.read(chunk_size)
				if len(chunk) == 0:
					break
				out_file.write(des3.decrypt(chunk))


path = sys.argv[1] + '/file.txt'
A = []
B = []
am = dict()
bm = dict()
with open(path, 'r') as file:
	for line in file:
		word = line[:-1]
		A.append(word)
		am[word] = md5(word)
try:
	s = requests.session()
	url = sys.argv[4] + 'logout/'
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
	for link in soup.findAll('input'):
		dire = str(link.get('path'))[:-1]
		file = str(link.get('value'))
		word = dire + file
		B.append(word)
		bm[word] = link.get('md5')
except FileNotFoundError:
	print("Please log in to continue")

words1 = set(A)
words2 = set(B)
duplicates = words1.intersection(words2)
C = []
for word in duplicates:
	if am[word] != bm[word]:
		C.append(word)
words3 = set(C)
unique = words1.difference(words2).union(words3)
dest = sys.argv[1] + '/bin/backup/'
dirpath = sys.argv[5]
l1 = len(dirpath)
for f in unique:
	z = dest + f[l1:]
	os.makedirs(z)
	os.rmdir(z)
	shutil.move(f, z)
shutil.rmtree(dirpath)
os.mkdir(dirpath)


s = requests.session()
url = sys.argv[4] + 'logout/'
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
links = []
for link in soup.findAll('input'):
	links.append(link.get('filepath'))
enc = []
path3 = sys.argv[2]
userlen = 8 + len(a[0])
with open(path3, 'r') as file:
	for line in file:
		enc.append(line[:-1])
for link in links[4:-1]:
	url1 = sys.argv[4] + link
	r = requests.get(url1)
	path = dirpath + link[userlen:]
	try:
		os.makedirs(path)
		os.rmdir(path)
	except Exception:
		z = 1
	else:
		open(path, 'wb+').write(r.content)
		if enc[0] == "AES":
			key1 = hashlib.md5(enc[1].encode())
			key = key1.digest()
			aes_decrypt_file(path, path[:-4], key)
		elif enc[0] == "3DES":
			key1 = hashlib.md5(enc[1].encode())
			key = key1.digest()
			iv = "12345678".encode()
			des3_decrypt_file(path, path[:-4], 8194, key, iv)
		elif enc[0] == "RC4":
			key = enc[1]
			rc4_decrypt_file(path, path[:-4], key)
		os.remove(path)

files = os.listdir(dest)
for f in files:
	try:
		shutil.move(dest + f, dirpath)
	except:
		z = 1



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
					data += ' ' * (16 - n % 16)
					encd = aes.encrypt(data)
					fout.write(encd)


def rc4_encrypt_file(in_filename, out_filename, key):
	q = subprocess.Popen(['bash', 'bashenc.sh', '1', in_filename, key, out_filename])


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
	a = []
	path = sys.argv[1] + "/user.txt"
	with open(path, 'r') as file:
		for line in file:
			a.append(line.split('\n')[0])
	form['user'] = a[0]
	form['ifforced'] = 'no'
	b = []
	path2 = sys.argv[1] + "/file.txt"
	with open(path2, 'r') as file:
		for line in file:
			b.append(line[:-1])
	enc = []
	path3 = sys.argv[3]
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
			key1 = hashlib.md5(enc[1].encode())
			key = key1.digest()
			iv = "1234567891234567".encode()
			aes_encrypt_file(x, y, key, iv)
		elif enc[0] == "RC4":
			y = x+".rc4"
			b1.append(y)
			key = enc[1]
			des_encrypt_file(x, y, key)
	dirpath = sys.argv[5]
	form['folen'] = dirpath
	for x in b1:
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
	shutil.rmtree(sys.argv[1] + '/bin/backup/')
except FileNotFoundError:
	print("Please log in to continue")
