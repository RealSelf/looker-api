import time

import requests

from helpers import tidy_dates

ENDPOINTS_DATA = {
}


class LookerInvalidEndpoint(Exception):
	pass


class LookerRequestError(Exception):
	pass


class LookerResponseError(Exception):
	pass


class InvalidParameters(Exception):
	pass


class LookerTimeoutException(Exception):
	pass


class Looker(object):
	""" An object for getting data from the Looker API"""

	def __init__(self, subdomain, client_id, client_secret):

		self.base_url = self._make_base_url(subdomain)
		self.client_id = client_id
		self.client_secret = client_secret
		self.access_token = None
		self.access_expiration = None

	def _make_base_url(self, subdomain, port=19999):

		return "https://" + subdomain + ".looker.com:" + str(port)

	def _make_api_request_url(self, endpoint, rtn_format):
		return self.base_url + "/api/3.0" + endpoint + rtn_format

	def _do_request(self, url, kwargs):
		""" Execute a request """
		if (not (self.access_token and self.access_expiration > time.time())):
			self._login()
		
		headers = {"Authorization":"token "+ self.access_token}

		r = requests.get(url, kwargs, headers=headers)

		status_code = r.status_code
		if status_code == 400:
			raise StatRequestError("Bad request")
		elif status_code == 401:
			raise StatRequestError("Unauthorized API key")
		elif status_code == 403:
			raise StatRequestError("Usage Limit Exceeded")
		elif status_code == 404:
			raise StatRequestError("Not Found")
		elif status_code == 500:
			raise StatRequestError("Internal Server Error")

		response_data = r.json()
		
		return response_data

	def _login(self):
		""" Make a request to the realself.looker.com API login endpoint
		adds the authentication key to the Looker object
		"""

		url = self._make_api_request_url('/login', "")

		data = (('client_id',self.client_id),('client_secret',self.client_secret))

		r = requests.post(url, data=data)

		status_code = r.status_code
		if status_code == 400:
			raise StatRequestError("Bad request")
		elif status_code == 401:
			raise StatRequestError("Unauthorized API key")
		elif status_code == 403:
			raise StatRequestError("Usage Limit Exceeded")
		elif status_code == 404:
			raise StatRequestError("Not Found")
		elif status_code == 500:
			raise StatRequestError("Internal Server Error")

		response_data = r.json()

		if 'access_token' not in response_data or 'expires_in' not in response_data:
			raise StatResponseError(response_data)

		self.access_expiration = time.time() + (int(response_data['expires_in']) - 5)
		self.access_token = response_data['access_token']

	def run_look(self, look_id, rtn_format, **kwargs):
		endpoint = "/looks/{0}/run".format(look_id)

		url = self._make_api_request_url(endpoint,rtn_format)

		return self._do_request(url, kwargs)

	def request(self, endpoint, **kwargs):
		""" Make a request to the getstat.com API

		endpoint should correspond to an endpoint listed in the documentation
		kawrgs should be a dictionary of query parameters for the request
		"""

		if endpoint not in ENDPOINTS_DATA.keys():
			raise StatInvalidEndpoint("The endpoint {endpoint} does not exist".format(endpoint))

		allowed_parameters = ENDPOINTS_DATA[endpoint]
		illegal_paramters = [key for key in kwargs.keys()
							 if key not in allowed_parameters]
		if illegal_paramters:
			raise InvalidParameters("The parameter(s) {parameters} are not legal"
									" for the endpoint `{endpoint}`".format(
										parameters=illegal_paramters,
										endpoint=endpoint))

		url = self._make_api_request_url(endpoint, "/json")
		kwargs = tidy_dates(kwargs)

		return self._do_request(url, kwargs)