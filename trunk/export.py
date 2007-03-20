#!/usr/bin/python

import sqlite
import time

con = sqlite.connect('trac.db', encoding='utf-8')
cur = con.cursor()

cur.execute("SELECT t.id AS ticket, t.type AS type, t.component, t.version, t.time AS created, t.changetime as changetime, t.summary, t.description, t.priority, t.reporter as reporter, t.resolution, t.status, t.keywords, ticket_change2.comment FROM ticket t LEFT JOIN ticket_change2 ON (t.id = ticket_change2.id)")

data = cur.fetchall()
for d in data:
 d.ticket = str(d['ticket']).replace('$', '####')
 d.description = str(d['description']).replace('$', '####')
 d.keywords = str(d['keywords']).replace('$', '####')

 # date convert
 t = time.localtime(int(d['created']))
 d.created = "%d/%d/%d %d:%d:%d" % (t[0], t[1], t[2], t[3], t[4], t[5])
 t = time.localtime(int(d['changetime']))
 d.changetime = "%d/%d/%d %d:%d:%d" % (t[0], t[1], t[2], t[3], t[4], t[5])

 # add quotes to strings
 d.summary  = '"' + d['summary'].rstrip().replace('"', '""') + '"'
 d.description  = '"' + d.description.rstrip().replace('"', '""').replace("[[BR]]", "\n").replace("aaaaaa", ",") + '"'
 d.keywords = '"' + d['keywords'].rstrip().replace('"', '""') + '"'

 # add quotes to comments in d[13]
 if d.comment:
  comments = d['comment'].split('@@')
  for k in range(len(comments)):
   comments[k] = '"' + comments[k].rstrip().replace('"', '""').replace("[[BR]]", "\n").replace("aaaaaa", ",") + '"'
  d.comment = "$".join(comments)
 else:
  d.comment = ''
 if d.resolution == None:
  d.resolution = 'Opened'
 
 d.description = d.description.replace('«', '').replace('»', '')
 dd = ( str(d['ticket']), d['type'], d['component'], d['version'], d.created, d.changetime, d.summary, d.description, d.priority, d.reporter, d.resolution, d.status, d.keywords, d.comment)
 print "$".join(dd)
