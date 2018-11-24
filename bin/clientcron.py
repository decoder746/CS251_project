import time
import requests
import sys

while True:
    s1 = requests.session()
	url1 = sys.argv[1]
	block = s.get(url1)
	block_html = lxml.html.fromstring(block.text)
	inputs = block_html.xpath(r'//form//input[@type="hidden"]')
	form1 = {x.attrib["name"]: x.attrib["value"] for x in hidden}
	form1['user'] = sys.argv[2]
	form1['turn'] = "2"
	response1 = s.post(url1, data=form1)
    time.sleep(1)
