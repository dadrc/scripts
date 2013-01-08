#!/usr/bin/env python
import MySQLdb

db = MySQLdb.connect(host="SET ME", user="SET ME", passwd="SET ME", db="SET ME")
cur = db.cursor()

#replace 'APT status' with the name of your service.
cur.execute("SELECT objects.name1 FROM icinga_servicestatus AS status JOIN icinga_objects AS objects ON (status.service_object_id = objects.object_id) WHERE status.current_state != 0 AND objects.name2 LIKE 'APT status'")

for row in cur.fetchall():
  name = str(row[0])
  print name.lower()

# clean up
cur.close()
db.close()
