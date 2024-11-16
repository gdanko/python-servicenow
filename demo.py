#!/usr/bin/env python3

from pprint import pprint
from servicenow.client import ServiceNow

sn = ServiceNow(
	environment="prod",
	username="",
	password="",
	record_limit=10,
	debug=True
)

sn.incident_get(number="INC0063436")
pprint(sn.response)
