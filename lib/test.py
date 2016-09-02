#-*- coding: utf-8 -*-
from pasifik import PasifikAPI
class TestCase(object):
	"""docstring for TestCase"""
	def __init__(self):
		username = "YOUR_USERNAME"
		password = "YOUR_PASSWORD"
		self.header = "YOUR_COMPANY"
		lang = "tr" # 'tr': Turkish response, 'en': English response, 'ar': Arabic response.
		DEBUG = True
		self.obj = PasifikAPI(username, password, lang, DEBUG)

	def send_one_message_to_many_receipients(self):
		result = self.obj.submit(header=self.header, to="905999999998,905999999999", 
			text="SMS Test")
	def send_one_message_to_many_receipients_schedule_delivery(self):
		# "%Y-%m-%dT%H:%M:%SZ" format e.g "2016-07-23T21:54:02Z" in UTC Timezone.
		scheduled_delivery_time = "2016-09-28T09:30:00Z"
		result = self.obj.submit(header=self.header, to="905999999998,905999999999",
			universal=False, alphabet="Default",
			text="SMS Test",scheduled_delivery_time=scheduled_delivery_time)
	def send_one_message_to_many_receipients_schedule_delivery_with_validity_period(self):
		# "%Y-%m-%dT%H:%M:%SZ" format e.g "2016-07-23T21:54:02Z" in UTC Timezone.
		scheduled_delivery_time = "2016-09-28T09:30:00Z"
		# minutes number e.g 1440 minutes for 24 hours
		period = 1440
		result = self.obj.submit(header=self.header, to="905999999998,905999999999",
			universal=False, alphabet="Default",
			text="SMS Test",scheduled_delivery_time=scheduled_delivery_time, period=period)
	def send_one_message_to_many_receipients_turkish_language(self):
		text = "Artık Ulusal Dil Tanımlayıcısı ile Türkçe karakterli smslerinizi rahatlıkla iletebilirsiniz."
		result = self.obj.submit(header=self.header, to="905999999998,905999999999",
			universal=False, alphabet="TurkishSingleShift",
			text=text)
	def send_one_message_to_many_receipients_flash_sms(self):
		text = "My first Flash SMS, It will be temporary on your phone."
		result = self.obj.submit(header=self.header, to="905999999998,905999999999",
			universal=False, alphabet="DefaultMclass0",
			text=text)
	def send_one_message_to_many_receipients_unicode(self):
		text = "メッセージありがとうございます"
		result = self.obj.submit(header=self.header, to="905999999998,905999999999",
			universal=False, alphabet="UCS2",
			text=text)
	def send_one_message_to_many_receipients_outside_turkey(self):
		# '+' required e.g '+43' for Germany mobile prefix number
		to = "+435999999998,+435999999999"
		universal = True
		result = self.obj.submit(header=self.header, to=to,
			universal=universal,
			text="SMS Test",scheduled_delivery_time=scheduled_delivery_time)
	def send_many_message_to_many_receipients(self):
		envelopes = [
			{"to": "905999999998", "text": "test 1"},
			{"to": "905999999999", "text": "test 2"},
		]
		result = self.obj.submit_multi(header=self.header, envelopes=envelopes)
	def query_multi_general_report(self):
		start_date = "01.03.2016" # formated as turkish date time format "%d.%m.%Y"
		end_date = "01.03.2016" # formated as turkish date time format "%d.%m.%Y"
		result = self.obj.query_multi(start_date=start_date, end_date=end_date)
	def query_multi_general_report_with_id(self):
		sms_id = "123456"
		result = self.obj.query_multi_id(sms_id)
	def query_detailed_report_with_id(self):
		sms_id = "123456"
		result = self.obj.query(sms_id)
	def get_account_settings(self):
		result = self.obj.getsettings()
	def get_authority(self):
		encode = False
		result = self.obj.authorization_test(encode=encode)
	def get_cdr_report(self):
		i_account = 123456
		result = self.obj.call_history(i_account=i_account)
	def get_cdr_report_range_datetime(self):
		i_account = 123456
		start_date = "2016-08-31T10:12:45Z"
		end_date = "2016-09-01T10:12:45Z"
		cli = ""
		cld = ""
		offset = 0
		limit = 100
		result = self.obj.call_history(i_account=i_account, 
			start_date=start_date, end_date=end_date, cli=cli, cld=cld, 
			offset=offset, limit=limit)
	def get_cdr_report_with_type(self):
		i_account = 123456
		start_date = ""
		end_date = ""
		cli = ""
		cld = ""
		offset = 0
		limit = 50
		type_flag = ["non_zero_and_errors", "non_zero", "all", "complete", "incomplete", "errors"]
		type = type_flag[0]
		result = self.obj.call_history(i_account=i_account, 
			start_date=start_date, end_date=end_date, cli=cli, cld=cld, 
			offset=offset, limit=limit, type=type)
	def get_active_calls(self):
		i_account_list = [123, 456]
		result = self.obj.call_active(i_account_list=i_account_list)
	def get_disconnect_active_call(self):
		id = 123456
		result = self.obj.call_active_disconnect(id=id)