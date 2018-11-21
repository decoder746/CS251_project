import sqlite3
import time
# ts = time.time()
con = sqlite3.connect('1.db')

cur = con.cursor()

# # cur.execute('''SELECT * FROM glass2''')

# lst = []
# lst.append(ts)

# # cur.execute('''INSERT INTO glass2 VALUES("path1","documents/values/here",?)''',lst)

cur.execute('''SELECT * FROM glass4 WHERE filename = "Screenshot from 2018-09-28 22-24-10.png"''')
for row in cur:
	print(row)
con.commit()
con.close()
# import hashlib
# str2 = "glassScreenshot from 2018-09-28 22-05-03.png"
# print(str2)
# str1 = hashlib.md5(open(str2,'rb').read()).hexdigest()
# print(str1)