python-servicenow
=================
## Description
A Python-based SDK for ServiceNow.

## Requirements
- Python 3

## Installation
* Clone the [repository](https://github.com/gdanko/python-servicenow)
* Switch to the local respository directory.
* Build the pip package with: `python setup.py sdist`
* Install the resulting package with: `sudo pip3 install dist/servicenow-x-x-x.tar.gz`

## Features
The ServiceNow module currently supports the following ServiceNow features:
#### Incident Methods
	sn.incident_get()
	sn.incident_find()
#### Incident Task Methods
    sn.incident_task_get()
    sn.incident_task_find()
    sn.incident_create()
#### Major Incident Methods
    sn.major_incident_get()
    sn.major_incident_find()
    sn.major_incident_create()
#### Outage Methods
    sn.outage_get()
    sn.outage_find()
#### Service Catalog Request Methods
    sn.sc_request_get()
    sn.sc_request_find()
    sn.sc_request_create()
#### Service Catalog Request Item Methods
    sn.sc_req_item_get()
    sn.sc_req_item_find()
#### Service Catalog Task Methods
    sn.sc_task_get()
    sn.sc_task_find()
    sn.sc_task_create()
#### Netgear Methods
    sn.netgear_get()
    sn.netgear_find()
#### Problem Methods
    sn.problem_get()
    sn.problem_find()
    sn.problem_create()
#### Change Request Methods
    sn.change_request_get()
    sn.change_request_find()
    sn.change_request_create()
#### Change Task Methods
    sn.change_task_get()
    sn.change_task_find()
    sn.change_task_create()
#### Group Methods
    sn.group_get()
    sn.group_find()
#### User Methods
    sn.user_get()
    sn.user_find()
#### Label Entry Methods
    sn.label_entry_find()
#### Application Methods
    sn.application_find()
#### Configuration Item Methods
	sn.ci_get()
	sn.ci_find()
#### Colo Methods
	sn.colo_get()
	sn.colo_find()
#### Host Methods
	sn.host_get()
	sn.host_find()
#### Docker Methods
	sn.docker_engine_find()
	sn.docker_container_find()
	sn.docker_global_image_find()
	sn.docker_local_image_find()
	sn.docker_image_tag_find()

## Usage
To use the module in a script you simply import it and create an instance of it.
```
from pprint import pprint
from servicenow.client import ServiceNow

sn = ServiceNow(
	environment="dev1",
	username="bob",
	password="secret!",
	debug=True,
)
sn.incident_get(number="INC0063436")
pprint(sn.response)
```

## Using `find` Methods
If you are familiar with ServiceNow you will understand how the queries work. If you are looking for incidents created by Bob Smith, for example, you would specify on the query string `&sysparm_query=caller_id.name=Bob Smith`. Multiple queries are separarted with a carat symbol. The SDK handles all of this for you with the use of the ServiceNow Filter object.

When you create an instance of the ServiceNow module, it creates an instance of the Filter class and it can be accessed via `sn.filter` methods, which will be described below in more detail. Using the above example, you can find any incidents submitted by Bob Smith using the following script.
```
from pprint import pprint
from servicenow.client import ServiceNow

sn = ServiceNow(
	environment="dev1",
	username="bob",
	password="secret!",
	debug=True,
)
sn.filter.add(var="caller_id.name", op="=", value="Bob Smith")
sn.incident_find()
pprint(sn.response)
```

Now if you want to find Bob's incidents that are in an `Open` state you could add another filter.
```
from pprint import pprint
from servicenow.client import ServiceNow

sn = ServiceNow(
	environment="dev1",
	username="bob",
	password="secret!",
	debug=True,
)
sn.filter.add(var="caller_id.name", op="=", value="Bob Smith")
sn.filter.add(var="state", op="=", value="open")
sn.incident_find()
pprint(sn.response)
```

## ServiceNow Filter Methods
#### `sn.filter.add(var=varname, op=operator, value=value`)
This method adds a new filter to the filter list.
#### `sn.filter.delete(var=varname)`
This method deletes the filter with the name `varname`.
#### `sn.filter.count()`
This method returns the number of filters in the filter object.
#### `sn.filter.clear()`
This method empties the filter object, effectively initializing it as new.

## ToDo
* Add create methods
* Add delete methods
* Implement record limit in the constructor.

## License & Author(s)
* Authors: Gary Danko

