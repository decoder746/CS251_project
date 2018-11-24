from Crypto.Cipher import AES
import struct
import requests, lxml.html
import sys
from bs4 import BeautifulSoup
import os
from Crypto.Cipher import DES3
import hashlib
import subprocess


def aes_decrypt_file(encfile, verfile, key):
    with open(encfile,'rb') as fin:
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
                    fout.write(decd[:fsz]) # <- remove padding on last block
                fsz -= n    

def rc4_decrypt_file(in_filename, out_filename, key):
    q = subprocess.Popen(['bash', 'bashenc.sh', '2', in_filename, key, out_filename])



def des3_decrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_file.write(des3.decrypt(chunk))


try:
    a = []
    path = sys.argv[1] + "/user.txt"
    with open(path, 'r') as file:
        for line in file:
            a.append(line.split('\n')[0])
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
    url = sys.argv[3] + 'logout/'
    login = s.get(url)
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    form['username'] = a[0]
    form['password'] = a[1]
    response = s.post(url, data=form)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for link in soup.findAll('input'):
        links.append(link.get('filepath'))
    enc = []
    path3 = sys.argv[2]
    files = []
    path4 = sys.argv[1] + "/file.txt"
    with open(path4, 'r') as file:
        for line in file:
            files.append(line[:-1])
    with open(path3, 'r') as file:
        for line in file:
            enc.append(line[:-1])
    b1 = []
    dirpath = sys.argv[4]
    userlen = len(a[0])
    for link in links[4:-1]:
        url1 = str(sys.argv[3])[:-1] + link
        r = requests.get(url1)
        sh = link[7:]
        if sh[0:6] == "shared":
            userlen = 6
        else:
            userlen = userlen
        path = dirpath + link[userlen:]
        if path[:-4] in files:
            continue
        else:
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
                    des3_decrypt_file(path, path[:-4], 8192, key, iv)
                elif enc[0] == "RC4":
                    key = enc[1]
                    des_decrypt_file(path, path[:-4], key)
                os.remove(path)
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
    print('Please log in to continue')
