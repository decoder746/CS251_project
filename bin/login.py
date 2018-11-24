import requests, lxml.html
import getpass
import sys


s = requests.session()
url = sys.argv[4] + 'logout/'
### Here, we're getting the login page and then grabbing hidden form
### fields.  We're probably also getting several session cookies too.
login = s.get(url)
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
#print(form) 
### Now that we have the hidden form fields, let's add in our 
### username and password.
form['username'] = sys.argv[1]
form['password'] = sys.argv[2]
response = s.post(url, data=form)
if response.url==url:
	print("Your username and password didn't match. Please try again.")
else:
	print("User Authenticated")
	path = sys.argv[3] + '/user.txt'
	with open(path, 'w') as file:
		file.write(sys.argv[1])
		file.write("\n")
		file.write(sys.argv[2])
#print(response.text)
