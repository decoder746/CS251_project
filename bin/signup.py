import requests, lxml.html
import sys
s = requests.session()

### Here, we're getting the login page and then grabbing hidden form
### fields.  We're probably also getting several session cookies too.
url = sys.argv[5] + 'signup/'
login = s.get(url)
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
#print(form) 
### Now that we have the hidden form fields, let's add in our 
### username and password.
form['username'] = sys.argv[1]
form['password1'] = sys.argv[2]
form['password2'] = sys.argv[3]
response = s.post(url, data=form)
if form['password1'] != form['password2']:
	print("The two password fields didn't match.")
elif response.url == url:
	print("A user with that username already exists.")
else:
	path = sys.argv[4] + '/user.txt'
	with open(path, 'w') as file:
		file.write(sys.argv[1])
		file.write("\n")
		file.write(sys.argv[2])
	print("User Created and logged in.")
