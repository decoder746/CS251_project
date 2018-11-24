import requests, lxml.html
import sys
from bs4 import BeautifulSoup

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
	links = []
	for link in soup.findAll('input'):
		dire = str(link.get('path'))[:-1]
		file = str(link.get('value'))
		links.append(dire + file)
	for link in links[4:-1]:
		print(link)
except FileNotFoundError:
	print("Please log in to continue")
