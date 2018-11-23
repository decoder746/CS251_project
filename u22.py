import hashlib
import time
import sqlite3
import string
import os
from django.views.decorators.csrf import csrf_exempt

str2 = "SELECT * FROM ACCESS WHERE turn = \"1\" AND user=\"" + "glass8" + "\""
            
conn = sqlite3.connect('1.db')
cursor1 = conn.cursor()
# -- cursor1.execute("""CREATE TABLE ACCESS (user varchar[300],turn varchar[300])""")
# str1 = "INSE/RT INTO ACCESS VALUES(\"" + "glass8" +"\""+ "," + "\"0\"" + ")"
            
cursor1.execute(str2)
# conn.commit()
# conn.close()
# i = 0
for row in cursor1:
    print(row)
str2 = "SELECT * FROM ACCESS"
# # cursor1.execute(str2)
# # i = 0
# # for row in cursor1:
# #     print(row)

# str1 = "UPDATE ACCESS SET turn = \"1\" WHERE user = \"" + "glass8" + "\""
# cursor1.execute(str1)

# cursor1.execute(str2)
# i = 0
# for row in cursor1:
#     print(row)

conn.commit()
conn.close()