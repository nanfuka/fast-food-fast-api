from flask_testing import TestCase
#from app.models.UserRequest import UserRequest 

from app import app
import unittest
import json
from api.tests.Basetest import BaseTest



class TestUserRequests(BaseTest):

	# Check if URL path exists and is protected
	def test_if_URL_exists(self):
		response = self.client.get('/api/v1/orders')
		assert "401 UNAUTHORIZED" ==response.status

	# Test For a non authenticated user
	def test_api_check_non_authorised_user(self):
		with self.client:
			response = self.client.get('/api/v1/orders')
			reply = json.loads(response.data.decode())
			self.assertEquals(reply["success"],False)
			self.assertEquals(reply["message"],"You are not authorised to access this page.")
