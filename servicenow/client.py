from idps.client import Application
from pprint import pprint
import getpass
import inspect
import json
import os
import re
import servicenow.database as db
import servicenow.exception as exception
import servicenow.request as request
import servicenow.utils as utils
import sys

# https://developer.servicenow.com/app.do#!/rest_api_doc

class ServiceNow(object):
	def __init__(self, **kwargs):
		environments = {
			"dev1": {"base": "https://dev01.service-now.com/api/now/v2/table"},
			"dev2": {"base": "https://dev02.service-now.com/api/now/v2/table"},
			"prod": {"base": "https://prod.service-now.com/api/now/v2/table"},
		}
		self.response = {}
		self.debug = False
		self.filter = Filter()
		self.idps_client = None

		if "debug" in kwargs:
			self.debug = True if kwargs["debug"] == True else False

		self.logger = utils.configure_logger(
			loggerid="logger-{}".format(utils.generate_random(length=32)),
			debug=self.debug
		)

		if "environment" in kwargs:
			if kwargs["environment"] in environments:
				self.environment = kwargs["environment"]
				self.base_url = environments[self.environment]["base"]
			else:
				raise exception.InvalidEnvironment(environment=kwargs["environment"])
		else:
			raise exception.MissingConstructorParameter(parameter="environment")

		if "username" in kwargs:
			self.username = kwargs["username"]
		else:
			raise exception.MissingConstructorParameter(parameter="username")

		if "password" in kwargs:
			self.password = kwargs["password"]
		else:
			raise exception.MissingConstructorParameter(parameter="password")

		self.idps_endpoint = kwargs["idps_endpoint"] if "idps_endpoint" in kwargs else None
		self.idps_profile = kwargs["idps_profile"] if "idps_profile" in kwargs else None
		self.idps_policy_id = kwargs["idps_policy_id"] if "idps_policy_id" in kwargs else None
		self.proxies = {"http": kwargs["proxy"], "https": kwargs["proxy"]} if "proxy" in kwargs else None
		self.record_limit = kwargs["record_limit"] if "record_limit" in kwargs else None

		if self.idps_profile and self.idps_endpoint:
			raise exception.ParameterError(message="idps_profile cannot be used with idps_endpoint.")

		if self.idps_profile and self.idps_policy_id:
			raise exception.ParameterError(message="idps_profile cannot be used with idps_policy_id.")

		if self.idps_endpoint or self.idps_policy_id:
			if not (self.idps_endpoint and self.idps_policy_id):
				raise exception.ParameterError(message="You must supply idps_endpoint with idps_policy_id.")

		if self.idps_profile:
			self.idps_client = Application(profile=self.idps_profile)
		if self.idps_endpoint and self.idps_policy_id:
			self.idps_client = Application(endpoint=self.idps_endpoint, policy_id=self.idps_policy_id)

		m1 = re.match(r"^idps:(.*)$", self.username)
		m2 = re.match(r"^idps:(.*)$", self.password)
		username_key = m1.group(1) if m1 else None
		password_key = m2.group(1) if m2 else None

		if username_key and password_key:
			if self.idps_client:
				if username_key:
					self.idps_client.secret_get(name=username_key)
					if self.idps_client.success:
						self.username = self.idps_client.response["item"]
				if password_key:
					self.idps_client.secret_get(name=password_key)
					if self.idps_client.success:
						self.password = self.idps_client.response["item"]
			else:
				raise exception.ParameterError(message="You have supplied idps: as a prefix for username and password but you have not properly configured IDPS in the constructor.")

	# Begin get functions
	def incident_get(self, number=None):
		self.__generic_get(table="incident", field="number", value=number)

	def incident_task_get(self, number=None):
		self.__generic_get(table="u_incident_task", field="number", value=number)

	# def major_incident_get(self, number=None):

	def outage_get(self, number=None):
		self.__generic_get(table="cmdb_ci_outage", field="u_number", value=number)

	def sc_request_get(self, number=None):
		self.__generic_get(table="sc_request", field="number", value=number)

	def sc_req_item_get(self, number=None):
		self.__generic_get(table="sc_req_item", field="number", value=number)

	def sc_task_get(self, number=None):
		self.__generic_get(table="sc_task", field="number", value=number)

	def problem_get(self, number=None):
		self.__generic_get(table="problem", field="number", value=number)

	def change_request_get(self, number=None):
		self.__generic_get(table="change_request", field="number", value=number)

	def change_task_get(self, number=None):
		self.__generic_get(table="change_task", field="number", value=number)

	def group_get(self, name=None):
		self.__generic_get(table="sys_user_group", field="name", value=name)

	def user_get(self, name=None, username=None, email=None):
		if len(name.split(" ")) == 2:
			field = "name"
		elif len(name.split("@")) == 2:
			field = "email"
		else:
			field = "user_name"
		self.__generic_get(table="sys_user", field=field, value=name)

	def db_instance_get(self, name=None):
		self.__generic_get(table="cmdb_ci_db_instance", field="name", value=name)

	def conference_room_get(self, name=None):
		self.__generic_get(table="cmdb_ci_computer_room", field="name", value=name)
	# End get functions

	# Begin find functions
	def incident_find(self):
		self.__generic_find(table="incident")

	def incident_task_find(self):
		self.__generic_find(table="u_incident_task")

	def major_incident_find(self):
		self.filter.add(var="u_major_incident", op="=", value="true")
		self.__generic_find("incident")

	def outage_find(self):
		self.__generic_find(table="cmdb_ci_outage")

	def netgear_find(self):
		self.filter.add(var="sys_class_name", op="=", value="cmdb_ci_netgear")
		self.__generic_find(table="cmdb_ci_netgear")

	def problem_find(self):
		self.__generic_find(table="problem")

	def sc_request_find(self):
		self.__generic_find(table="sc_request")

	def sc_req_item_find(self):
		self.__generic_find(table="sc_req_item")

	def sc_task_find(self):
		self.__generic_find(table="sc_task")

	def change_request_find(self):
		self.__generic_find(table="change_request")

	def change_task_find(self):
		self.__generic_find(table="change_task")

	def user_find(self):
		self.__generic_find(table="sys_user")

	def group_find(self):
		self.__generic_find(table="sys_user_group")

	def label_entry_find(self):
		self.__generic_find(table="label_entry")

	def application_find(self):
		self.__generic_find(table="cmdb_ci_appl")

	def asset_find(self):
		self.__generic_find(table="alm_hardware")

	def vpc_find(self):
		self.filter.add(var="u_device_type", op="=", value="AWS")
		self.__generic_find(table="cmdb_ci_vpc")

	def vpn_find(self):
		self.filter.add(var="u_device_type", op="=", value="AWS")
		self.__generic_find(table="cmdb_ci_vpn")

	def docker_engine_find(self):
		self.__generic_find(table="cmdb_ci_docker_engine")

	def docker_container_find(self):
		self.__generic_find(table="cmdb_ci_docker_container")

	def docker_global_image_find(self):
		self.__generic_find(table="cmdb_ci_docker_image")

	def docker_local_image_find(self):
		self.__generic_find(table="cmdb_ci_docker_local_image")

	def docker_image_tag_find(self):
		self.__generic_find(table="cmdb_ci_docker_image_tag")

	def db_instance_find(self):
		self.__generic_find(table="cmdb_ci_db_instance")

	def conference_room_find(self, site=None, building=None, floor=None):
		if site and building and floor:
			query = "{}-{}-{}".format(site, building, floor)
		elif site and building:
			query = "{}-{}".format(site, building)
		elif site:
			query = "{}".format(site)
		self.filter.add(var="name", op="startswith", value=query)
		self.__generic_find(table="cmdb_ci_computer_room")

	def security_appliance_find(self):
		self.filter.add(var="model_id.u_device_type", op="=", value="Security Appliance")
		self.__generic_find(table="cmdb_ci_netgear")

	def storage_device_find(self):
		self.__generic_find(table="cmdb_ci_storage_server")

	def storage_volume_find(self):
		self.filter.add(var="sys_class_name", op="=", value="cmdb_ci_storage_volume")
		self.__generic_find(table="cmdb_ci_storage_volume")

	def storage_qtree_find(self):
		self.__generic_find(table="u_cmdb_ci_qtree")
	# End find functions

	# Begin create functions
	def incident_create(self, content=None):
		if not isinstance(content, dict):
			content = {}

		if not "assigned_to" in content:
			content["assigned_to"] = getpass.getuser()
		if not "u_client" in content:
			content["u_client"] = getpass.getuser()
		self.__generic_create(table="incident", content=content)

	def major_incident_create(self, content=None):
		content["u_major_incident"] = "true"
		self.__generic_create(table="incident", content=content)

	def sc_request_create(self, content=None):
		self.__generic_create(table="sc_request", content=content)

	def sc_req_item_create(self, content=None):
		self.__generic_create(table="sc_req_item", content=content)

	def sc_task_create(self, content=None):
		self.__generic_create(table="sc_task", content=content)

	def problem_create(self, content=None):
		self.__generic_create(table="problem", content=content)

	def change_request_create(self, content=None):
		self.__generic_create(table="change_request", content=content)

	def change_task_create(self, content=None):
		self.__generic_create(table="change_task", content=content)
	# End create functions

	# Begin ci functions
	def ci_get(self, name=None):
		self.__generic_get(table="cmdb_ci", field="name", value=name)

	def ci_find(self):
		self.__generic_find(table="cmdb_ci")

	def colo_get(self, name=None):
		self.__generic_get(table="cmdb_ci", field="name", value=name)

	def colo_find(self):
		self.filter.add(var="sys_class_name", op="=", value="cmdb_ci_datacenter")
		self.__generic_find(table="cmdb_ci")

	def host_get(self, name=None):
		self.__generic_get(table="cmdb_ci", field="name", value=name)

	def host_find(self):
		self.filter.add(var="sys_class_name", op="IN", value="cmdb_ci_server,cmdb_ci_vm")
		self.__generic_find(table="cmdb_ci")
	# End ci functions

	def __generic_sys_id(table=None, value=None):
		method = "get_sys_id"
		self.response = {}; qs = {}; payload = {}
		self.filter.add(var="number", op="=", value=value)
		filters = self.__process_filters(table=table, filters=self.filter)
		qs["sysparm_fields"] = "sys_id"
		qs["sysparm_query"] = filters
		request.get(self, uri=table, qs=qs)
		if self.response["success"] == True:
			return self.response[0]["sys_id"]

	def __generic_get(self, table=None, field=None, value=None, passed_content=None):
		self.response = {}; qs = {}; payload = {}
		self.filter.add(var=field, op="=", value=value)
		filters = self.__process_filters(table=table, filters=self.filter)
		qs["sysparm_display_value"] = "true"
		qs["sysparm_query"] = filters
		request.get(self, uri=table, qs=qs)

	def __generic_find(self, table=None, filters=None):
		method = self.__get_method(inspect.stack())
		self.response = {}; qs = {}; payload = {}
		qs["sysparm_display_value"] = "true"
		if self.record_limit:
			qs["sysparm_limit"] = self.record_limit
		filter_obj = None

		if filters != None:
			filter_obj = filters
		elif (self.filter):
			filter_obj = self.filter
		else:
			filter_obj = None

		if filter_obj != None:
			filters = self.__process_filters(table=table, filters=filter_obj)
			if filters:
				qs["sysparm_query"] = filters
			request.get(self, uri=table, qs=qs)
		else:
			raise exception.MissingFilter(method=method)

	def __generic_create(self, table=None, value=None, content=None):
		method = self.__get_method(inspect.stack())
		self.response = {}; qs = {}; payload = {}
		if content:
			content = self.__process_content(table=table, content=content)
			qs["sysparm_display_value"] = "true"
			request.post(self, uri=table, qs=qs, payload=content)
		else:
			raise exception.MissingPayload(method=method)

	def __process_content(self, table=None, content=None):
		# Need to handle invalid parameter values
		new_content = {}
		keys = list(content.keys())
		value_map = db.get_value_map(sn_table_name=table, parameter_list=keys)
		for parameter_name, parameter_value in content.items():
			target_parameter_name = db.get_parameter_target(sn_table_name=table, parameter_name=parameter_name)
			target = target_parameter_name if target_parameter_name != None else parameter_name

			if parameter_name in value_map:
				if parameter_value in value_map[parameter_name]:
					parameter_value = value_map[parameter_name][parameter_value]
				
				new_content[target] = parameter_value
			else:
				new_content[target] = parameter_value
		return new_content

	def __process_filters(self, table=None, filters=None):
		# Need to handle invalid parameter values
		new_filters = []
		keys = list(filters._data.keys())
		value_map = db.get_value_map(sn_table_name=table, parameter_list=keys)

		for parameter_name in filters._data.keys():
			target_parameter_name = db.get_parameter_target(sn_table_name=table, parameter_name=parameter_name)
			target = target_parameter_name if target_parameter_name != None else parameter_name

			parameter_name = parameter_name.lower()
			op = filters._data[parameter_name]["op"].upper()
			parameter_value = filters._data[parameter_name]["value"].lower()
			if parameter_name in value_map:
				if parameter_value in value_map[parameter_name]:
					parameter_value = value_map[parameter_name][parameter_value]	
				new_filters.append("{}{}{}".format(target, op, parameter_value))
			else:
				new_filters.append("{}{}{}".format(target, op, parameter_value))

		if len(new_filters) > 0:
			filters_str = "^".join(new_filters)
			return filters_str.replace("&", "%26")
		else:
			return None

	def __get_method(self, stack):
		valid_scripts = ["client.py"]
		usable_bits = [frame for frame in stack if os.path.basename(frame[1]) in valid_scripts]
		return usable_bits[-1][3] if len(usable_bits) > 0 else "unknown method"

class Filter(object):
	# http://wiki.servicenow.com/index.php?title=Operators_Available_for_Filters_and_Queries#gsc.tab=0
	# Also, validate operators
	valid_opts = [
		"startswith",
		"endswith",
		"like",
		"notlike",
		"=",
		"!="
		"isempty",
		"isnotempty",
		"anything",
		"not in"
		"in",
		"emptystring",
		"<=",
		">=",
		"<",
		">",
		"between",
		"sameas",
		"nsameas",

		"on",
		"noton",
		"before",
		"after",
		"between"
	]

	def __init__(self, **kwargs):
		self._data = {}

	def add(self, var=None, op=None, value=None):
		missing = []
		missing.append("")
		if var and op and value:
			# Validate key name here
			self._data[var] = { "op": op, "value": value }
		else:
			# Track which elements are missing and raise an exception
			print("the add method requires var, op, and value")
			sys.exit()

	def delete(self, var=None):
		self._dict.pop(var)

	def count(self):
		return len(self._data)

	def clear(self):
		self._data = {}
