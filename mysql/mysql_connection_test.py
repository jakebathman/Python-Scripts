#!/usr/bin/python
print "Content-type:text/html\n\n"
import MySQLdb

try:
 conn = MySQLdb.connect (
  host = "jakebathmancom.fatcowmysql.com",
  user = "collincountymrc",
  passwd = "BtPLk74a5ZMgXCZmxx",
  db = "mrc")

except MySQLdb.Error, e:
 print "Error %d: %s" % (e.args[0], e.args[1])

print "connected to the database"
