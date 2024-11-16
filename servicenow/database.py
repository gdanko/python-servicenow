from pprint import pprint
import os
import re
import sqlite3
import sys

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_valid_parameter_values(sn_table_name=None, parameter_name=None):
	valid_values = []
	select = "SELECT friendly_value FROM parameter_values WHERE sn_table_name='{}' AND parameter_name='{}'".format(sn_table_name, parameter_name)
	res = cursor.execute(select)
	conn.commit()
	for row in res:
		valid_values.append(row["friendly_value"])
	return valid_values

def get_parameter_target(sn_table_name=None, parameter_name=None):
	select = "SELECT target_parameter_name FROM parameters WHERE sn_table_name='{}' AND parameter_name='{}'".format(sn_table_name, parameter_name)
	cursor.execute(select)
	result = cursor.fetchone()
	return result["target_parameter_name"] if result else None

def get_value_map(sn_table_name=None, parameter_list=None):
	value_map = {}
	select = "SELECT * FROM parameter_values WHERE sn_table_name='{}' AND parameter_name IN({})".format(sn_table_name, quote_list(parameter_list))
	res = cursor.execute(select)
	conn.commit()
	for row in res:
		parameter_name = row["parameter_name"]
		friendly_value = row["friendly_value"]
		actual_value = row["actual_value"]
		if not parameter_name in value_map:
			value_map[parameter_name] = {}
		value_map[parameter_name][friendly_value] = actual_value
	return value_map

def quote_list(l):
	return ",".join(["\'{}\'".format(x) for x in l])

def _dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

dbfile = os.path.join(PACKAGE_ROOT, "data", "servicenow.db")
conn = sqlite3.connect(dbfile, check_same_thread=False)
conn.row_factory = _dict_factory
cursor = conn.cursor()