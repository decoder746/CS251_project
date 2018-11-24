import requests, lxml.html
import sys
from bs4 import BeautifulSoup


def md5(fname):
	hash_md5 = hashlib.md5()
	with open (fname, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


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
duplicates  = words1.intersection(words2)
unique1 = words1.difference(words2)
unique2 = words2.difference(words1)
print("Only on Client")
for x in unique1:
	print("-" + x)
print("Only on Server")
for x in unique2:
	print("-" + x)
print("On both")
for x in duplicates:
	print("-" + x)

C = []
for word in duplicates:
	if am[word] != bm[word]:
		C.append(word)
print("Files not synced")
for x in C:
	print("-" + x)

