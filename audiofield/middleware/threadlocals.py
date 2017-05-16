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

# middleware updated to be compatible with Django 1.10+ per below
# https://docs.djangoproject.com/en/1.11/topics/http/middleware/#upgrading-middleware
#
# Issue submitted to audiofield project on github at: https://github.com/areski/django-audiofield/issues/27

class ThreadLocals(object): 
	"""
	Middleware that gets various objects from the
	request object and saves them in thread local storage.
	"""
	

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		

		_thread_locals.request = request

		response = self.process_request(request)