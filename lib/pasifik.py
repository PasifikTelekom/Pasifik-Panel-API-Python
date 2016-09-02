#-*- coding: utf-8 -*-
import httplib
import json
from urlparse import urlparse
class PasifikAPI(object):
	"""
* Pasifik Telekom API
* Version: 2.0
* Author: Tarek Kalaji
* License: MIT
* Release Date: 2016/09/01
"""
	def __init__(self, username, password, lang="tr", DEBUG=False):
		self.authorization = str("%s:%s" % (username, password)).encode("base64").replace("\n", "")
		self.base_url = "https://oim.pasifiktelekom.com.tr/%s/api/" % lang
		self.DEBUG = DEBUG
		self.timeout = 60
	def submit(self, header, to, text, universal=False, alphabet="Default", scheduled_delivery_time="", period=0):
		data = {
			"from": header,
			"to": to,
			"text": text,
			"universal": universal,
			"alphabet": alphabet,
		}
		if len(scheduled_delivery_time) > 0:
			data["scheduled_delivery_time"] = scheduled_delivery_time
		if period > 0:
			data["period"] = period
		return self._post("sms/submit/", data)
	def submit_multi(self, header, envelopes, universal=False, alphabet="Default", scheduled_delivery_time="", period=0):
		data = {
			"from": header,
			"envelopes": envelopes,
			"universal": universal,
			"alphabet": alphabet,
		}
		if len(scheduled_delivery_time) > 0:
			data["scheduled_delivery_time"] = scheduled_delivery_time
		if period > 0:
			data["period"] = period
		return self._post("sms/submit/multi/", data)
	def query_multi(self, start_date, end_date):
		data = {"start_date": start_date, "end_date": end_date}
		return self._post("sms/query/multi/", data)
	def query_multi_id(self, sms_id="123123"):
		data = {"sms_id": sms_id}
		return self._post("sms/query/multi/id/", data)
	def query(self, sms_id="123123"):
		data = {"sms_id": sms_id}
		return self._post("sms/query/", data)
	def getsettings(self):
		data = {}
		return self._post("user/getsettings/", data)
	def authorization_test(self, encode=False):
		auth = self.authorization if encode else self.authorization.decode("base64")
		if self.DEBUG:
			print(auth)
		return auth
	def call_history(self, i_account, start_date="", end_date="", 
			cli="", cld="", offset=0, limit=0, type=""):
		data = {}
		data["i_account"] = i_account
		data["start_date"] = start_date
		data["end_date"] = end_date
		data["cli"] = cli
		data["cld"] = cld
		data["offset"] = offset
		data["limit"] = limit
		data["type"] = type
		return self._post("tel/history/", data)
	def call_active(self, i_account_list):
		data = {"i_account_list": i_account_list}
		return self._post("tel/live/", data)
	def call_active_disconnect(id):
		data = {"id": id}
		return self._post("tel/live/disconnect/", data)
	def _post(self, resource, data):
		full_url = "%s%s" % (self.base_url, resource)
		prs = urlparse(full_url)
		json_data = json.dumps(data)
		headers = {	
			"Content-Type": "application/json",
			"Accept": "application/json",
			"Authorization": self.authorization,
			"Content-Length": len(json_data),
		}
		conn = httplib.HTTPSConnection(prs.netloc, timeout=self.timeout)
		conn.request(method="POST", url=prs.path, body=json_data, headers=headers)
		response = conn.getresponse()
		result = ""
		if response.status != 200:
			result = json.dumps({"status": response.status, 
				"message": "can not access %s, error code %s, reason %s" % (
					self.base_url, response.status, response.reason)})
		else:
			result = response.read()
		if self.DEBUG:
			print("REQUEST:")
			print(json.dumps(json.loads(json_data), indent=4, sort_keys=True) + "\n\n" if len(json_data) > 0 else json_data + "\n\n")
			print("HEADER: \n" + json.dumps(headers, indent=4, sort_keys=True) + "\n\n")
			print("RESPONSE:")
			print(json.dumps(json.loads(result), indent=4, sort_keys=True) + "\n\n" if len(result) > 0 else result + "\n\n")
		conn.close()
		return result