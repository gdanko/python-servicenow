import idps.exception as exception
import idps.utils as utils
import inspect
import json
import os
import re
import requests
import sys
from urllib.parse import urlencode

from pprint import pprint

# request.get(self, table=table, field=field, value=value, passed_content=passed_content)
def get(client, uri=None, qs=None, payload=None, sys_id=None):
	__servicenow_request(client, http_method="GET", uri=uri, qs=qs, payload=payload, sys_id=sys_id)

def post(client, uri=None, qs=None, payload=None, sys_id=None):
	__servicenow_request(client, http_method="POST", uri=uri, qs=qs, payload=payload, sys_id=sys_id)

#def put(client, uri=None, qs=None, payload=None):
#	__servicenow_request(client, http_method="PUT", uri=uri, qs=qs)

#def delete(client, uri=None, qs=None, payload=None):
#	__servicenow_request(client, http_method="DELETE", uri=uri, qs=qs)

def __get_method(stack):
	valid_scripts = ["client.py"]
	usable_bits = [frame for frame in stack if os.path.basename(frame[1]) in valid_scripts]
	return usable_bits[-1][3] if len(usable_bits) > 0 else "unknown method"

def __servicenow_request(client, http_method=None, uri=None, qs=None, payload=None, sys_id=None):
	method = __get_method(inspect.stack())
	url = None
	req = None
	res = None
	body = None
	json_body = None
	client.logger.debug("Executing method: {0}".format(method))
	headers = {}
	errors, message = [],[]

	url = "{}/{}".format(client.base_url, uri)
	if sys_id:
		url = "{}/{}".format(url, sys_id)

	if qs and isinstance(qs, dict):
		if len(qs.keys()) > 0:
			qs_arr = []
			for k in qs.keys():
				qs_arr.append( urlencode({k: str(qs[k])}) )
			qs_str = "&".join(qs_arr)
			url = "{0}?{1}".format(url, qs_str)
		else:
			url = url
	else:
		url=url

	client.logger.debug("{0} {1}".format(http_method, url))
	if payload:
		client.logger.debug("payload: {0}".format(payload))

	if payload:
		res = requests.request(http_method, url, auth=(client.username, client.password), proxies=client.proxies, headers=headers, data=json.dumps(payload))
	else:
		res = requests.request(http_method, url, auth=(client.username, client.password), proxies=client.proxies, headers=headers)

	# HTML body
	body = res.text
	#print(body);sys.exit()
	if len(body) <= 0: body = ""

	# Content-length
	if res.headers.get("content-length"):
		content_length = int(res.headers.get("content-length"))
	else:
		content_length = len(body) if len(body) > 0 else 0

	# JSON body
	try:
		if isinstance(body, str):
			json_body = utils.validate_json(body)
		elif isinstance(body, bytes):
			json_body = utils.validate_json(body.decode("utf-8"))
	except:
		json_body = None

	# Other stuff
	status_code = res.status_code
	content_type = res.headers.get("content-type")

	# Trap oddball errors
	# Invalid JSON received from IDPS
	if (content_type == "application/json") and (not json_body):
		client.success = False
		raise exception.InvalidJsonError(url=url, status_code=status_code, body=body)

	client.response = {}

	if content_length > 0:
		if "application/json" in content_type:
			records = []
			if "error" in json_body:
				client.response = json_body["error"]
			else:
				if isinstance(json_body["result"], dict):
					records.append(json_body["result"])
				elif isinstance(json_body["result"], list):
					for record in json_body["result"]:
						records.append(record)

				client.response["records"] = records
				client.response["count"] = len(records)

		elif "text/html" in content_type:
			raise exception.UnknownApiError(url=url, status_code=status_code, body=body)

	client.response["status_code"] = status_code

	if (status_code >= 200) and (status_code < 400):
		client.response["success"] = True
		if content_length <= 0:
			client.response["body"] = "The method {0} completed successfully".format(method)
	else:
		client.response["success"] = False
		if content_length <= 0:
			client.response["body"] = "The method {0} completed unsuccessfully".format(method)

	client.success = client.response["success"]
