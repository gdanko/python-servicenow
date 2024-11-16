#!/usr/bin/env python3

from pprint import pprint
from servicenow.client import ServiceNow
#import servicenow.mapper as m

import sys


sn = ServiceNow(
	environment="prod",
	username="",
	password="",
	record_limit=10,
	debug=True
)

sn.change_request_find()
pprint(sn.response)
sys.exit()

sn.incident_get(number="INC0063436")
#sn.user_get(name=name)
pprint(sn.response)
sys.exit()

#sn.filter.add(var="manager.name", op="=", value="Tom Whitcomb")
sn.filter.add(var="number", op="=", value="INC0063436")
sn.filter.add(var="state", op="=", value="OpEn")
sn.filter.add(var="foo", op="like", value="bar")
sn.filter.add(var="caller_id.name", op="=", value="Gary Danko")
#sn.filter.add(var="assigned_to.name", op="=", value="Gary Danko")
#sn.asset_find()
#sn.vpn_find()

sn.incident_find()
#sn.incident_create()
#sn.db_instance_get(name="adevplddb711.corp.foo.net/MSSQLSERVER")
#sn.filter.add(var="used_for", op="=", value="Production")
#sn.db_instance_find()
#sn.filter.add(var="name", op="startswith", value="SDG-02")
#sn.conference_room_find(site="SDG", building="02", floor="01")
#sn.netgear_get(name="CTS-SX20-PHD4X-K9")
#sn.filter.add(var="manufacturer.name", op="startswith", value="netapp")
#sn.storage_qtree_find()
#sn.user_find()


cr = {
	'approval': 'requested',
	'backout_plan': 'bar',
	'change_plan': 'foo',
	'client': 'Gary Danko',
	'cmdb_ci': 'API Gateway',
	'description': 'mydesc',
	'environment': 'dev',
	'impact': 'critical',
	'opened_by': 'Gary Danko',
	'potential_impact': 'critical',
	'priority': 'critical',
	'qa_approver': 'Gary Danko',
	'risk': 'low',
	'short_description': 'mysummary',
	'sub_category': 'Release',
	'template': 'APPRELEASE',
	'test_plan': 'baz',
	'urgency': 'low',
}
#sn.change_request_get("CHG0421271")
#sn.change_request_create(cr)
#pprint(sn.response)
