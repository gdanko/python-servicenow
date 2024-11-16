#!/usr/bin/env python3

from pprint import pprint
from servicenow.client import ServiceNow
#import servicenow.mapper as m

import sys


sn = ServiceNow(
	environment="prod",
	username="",
	password="",
	#record_limit=10,
	debug=True
)

sn.filter.add(var='opened_at', op='>=', value='2018-07-01 00:00:00')
sn.filter.add(var='state', op='in', value='Closed')
sn.filter.add(var='cmdb_ci.name', op='=', value='API Gateway')
sn.change_request_find()
pprint(sn.response)
sys.exit()

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

