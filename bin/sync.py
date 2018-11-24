import requests, lxml.html
import sys


s = requests.session()
url = 'http://127.0.0.1:8000/uploads/'
### Here, we're getting the login page and then grabbing hidden form
### fields.  We're probably also getting several session cookies too.
login = s.get(url)
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
#print(form) 
### Now that we have the hidden form fields, let's add in our 
### username and password.
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
for x in b:		
	with open(x, 'rb') as f:
		file1 = {'myfile': f}
		form['filepath'] = x
		response = s.post(url, files=file1, data=form)
		if (response.status_code==500):
			z = input("Do you want to overwrite " + x + " yes/no: ")
			if (z=='yes'):
				form['ifforced'] = 'yes'
				response = s.post(url, files=file1, data=form)
				form['ifforced'] = 'no'
