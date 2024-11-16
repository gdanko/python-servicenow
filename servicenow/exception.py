class MissingConstructorParameter(Exception):
	def __init__(self, parameter=None):
		self.parameter = parameter
		return

	def __str__(self):
		self.error = "The required \"{}\" parameter is missing from the ServiceNow constructor.".format(self.parameter)
		return self.error

class ParameterError(Exception):
	def __init__(self, message=None):
		self.message = message
		return

	def __str__(self):
		self.error = self.message
		return self.error

class InvalidEnvironment(Exception):
	def __init__(self, environement=None):
		self.environment = environement
		return

	def __str__(self):
		self.error = "The specified environment, \"{}\", is invalid.".format(self.environment)
		return self.error

# The IDPS REST API returned HTML
class IdpsUnknownApiError(Exception):
	def __init__(self, url=None, status_code=None, body=None):
		self.url = url
		self.status_code = code
		self.body = body if body else "No HTML body returned"
		return

	def __str__(self):
		return "An unknown IDPS API error occurred. URL: {}; Status code {}; HTML body: {}".format(self.url, self.status_code, self.body)


# Content-type is application/json but the body is invalid JSON
class InvalidJsonError(Exception):
	def __init__(self, url=None, status_code=None, body=None):
		self.url = url
		self.status_code = status_code
		self.body = body if body else "No HTML body returned"
		return

	def __str__(self):
		return "Invalid JSON was received from IDPS. URL: {}; Status code {}; HTML body: {}.".format(self.url, self.status_code, self.body)

# Content-type is application/json but the body is invalid JSON
class MissingFilter(Exception):
	def __init__(self, method=None):
		self.method = method
		return

	def __str__(self):
		return "The method {} requires you add at least one filter. Try using ServiceNow.filter.add(var=x, op=y, value=z)".format(self.method)

class MissingPayload(Exception):
	def __init__(self, method=None):
		self.method = method
		return

	def __str__(self):
		return "When using the {} method, you must supply the JSON content in the form of a Python dictionary.".format(self.method)
