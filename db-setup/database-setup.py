#!/usr/bin/env python3

from pprint import pprint
import json
import os
import sqlite3
import sys

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

dbfile = os.path.join(PACKAGE_ROOT, "servicenow.db")
conn = sqlite3.connect(dbfile, check_same_thread=False)
cursor = conn.cursor()

#insert = "INSERT INTO bot_users (id,username,password,level) VALUES (?,?,?,?)"
#cursor.execute(insert, (
#	id,
#	username,
#	password,
#	level
#))
#conn.commit()

tables = ["parameters", "parameter_values"]
for table in tables:
	drop = "DROP TABLE IF EXISTS {}".format(table)
	cursor.execute(drop)
	conn.commit()

create = "CREATE TABLE parameters (sn_table_name TEXT NOT NULL, parameter_name TEXT NOT NULL, target_parameter_name TEXT NOT NULL)"
cursor.execute(create)
conn.commit()

create = "CREATE TABLE parameter_values (sn_table_name TEXT NOT NULL, parameter_name TEXT NOT NULL, friendly_value TEXT NOT NULL, actual_value TEXT NOT NULL)"
cursor.execute(create)
conn.commit()

parameter_map = json.loads(open("parameter_map.json", "r").read())

for table_name, table_obj in sorted(parameter_map.items()):
	for parameter_name in sorted(parameter_map[table_name]["parameters"]):
		if "target" in parameter_map[table_name]["parameters"][parameter_name]:
			target_parameter_name = parameter_map[table_name]["parameters"][parameter_name]["target"]
		else:
			target_parameter_name = parameter_name

		insert = "INSERT INTO parameters (sn_table_name, parameter_name, target_parameter_name) VALUES (?,?,?)"
		cursor.execute(insert, (table_name, parameter_name, target_parameter_name))
		conn.commit()
		if "valid" in parameter_map[table_name]["parameters"][parameter_name]:
			for friendly_value, actual_value in parameter_map[table_name]["parameters"][parameter_name]["valid"].items():
				insert = "INSERT INTO parameter_values (sn_table_name, parameter_name, friendly_value, actual_value) VALUES (?,?,?,?)"
				cursor.execute(insert, (table_name, parameter_name, friendly_value, actual_value))
				conn.commit()
 