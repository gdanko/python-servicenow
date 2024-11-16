import json
import logging
import random
import servicenow.exception as exception
import sys

def configure_logger(loggerid=None, debug=False):
	if loggers.get(loggerid):
		return loggers.get(loggerid)
	else:
		level = logging.DEBUG if debug == True else logging.INFO

		logger = logging.getLogger(loggerid)
		handler = logging.StreamHandler()
		formatter = logging.Formatter("%(levelname)s %(message)s")
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		logger.setLevel(level)
		logger.propagate = False
		loggers[loggerid] = logger
	return logger

def validate_json(string):
	if string:
		try:
			hash = json.loads(string)
			return hash
		except:
			return None
	else:
		return None

def generate_random(length=8):
	return "".join(random.choice("0123456789abcdef") for x in range(length))

version = sys.version_info
major = version[0]
loggers = {}
logger = configure_logger(loggerid="logger-{}".format(generate_random(length=32)), debug=False)