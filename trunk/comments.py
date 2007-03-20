#!/usr/bin/python

import sqlite

con = sqlite.connect('trac.db', encoding='utf-8')
con.autocommit = 1
cur = con.cursor()

cur.execute("SELECT ticket, newvalue FROM ticket_change WHERE field = 'comment'");
data = cur.fetchall()
comments = {}
for comment in data:
 c = None
 try:
  c = comments[comment.ticket]
 except KeyError:
  c = None
 if c == None:
  c = ""
 else:
  c += "$"
 c += comment.newvalue.decode('utf-8')
 print c
 comments[comment.ticket] = c

print "cnt = %d" % len(comments)

try:
 cur.execute("DROP TABLE ticket_change2")
except sqlite.DatabaseError:
 pass
try:
 cur.execute("CREATE TABLE ticket_change2 (id INTEGER PRIMARY KEY, comment TEXT)")
except sqlite.DatabaseError:
 print "Table exists"

for id in comments.keys():
 comment = comments[id]
 comment = comment.replace("'", "''")
 sql = "INSERT INTO ticket_change2 VALUES (%s, '%s')" % (id, comment)
 cur.execute(sql)