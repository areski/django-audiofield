#
# django-audiofield License
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2014 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

import threading

_thread_locals = threading.local()

# middleware updated to be compatible with Django 1.10+ 5/16/2017 per - https://docs.djangoproject.com/en/1.11/topics/http/middleware/#upgrading-middleware
# updates on lines 22 - 23 and 35 - 41 on 5/16/2017 are to attempt to add back compatibility with Django 1.9 and prev. - testing needed
# Issue submitted to audiofield project on github at: https://github.com/areski/django-audiofield/issues/27

def get_current_request():
    return getattr(_thread_locals, 'request', None)

class ThreadLocals(object): 
	"""
	Middleware that gets various objects from the
	request object and saves them in thread local storage.
	"""
	def process_request(self, request):
		_thread_locals.request = request	

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = None

		_thread_locals.request = request
		
		if hasattr(self, 'process_request'):
			response = self.process_request(request)
		if not response:
			response = self.process_request(request)

		self.get_response(request)

		return response