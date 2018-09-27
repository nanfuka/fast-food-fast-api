from flask_testing import TestCase
from app import app
import unittest
import json
from api.tests.Basetest import BaseTest


class TestUserRequests(BaseTest):

    def test_if_URL_exists(self):
        """Check if URL path exists and is protected"""
        response = self.client.get('/api/v1/orders')
        assert "401 UNAUTHORIZED" == response.status

    def test_api_check_non_authorised_user(self):
        """Test For a non authenticated user"""
        with self.client:
            response = self.client.get('/api/v1/orders')
            reply = json.loads(response.data.decode())
            self.assertEquals(reply["success"], False)
            self.assertEquals(
                reply["message"],
                "You are not authorised to access this page.")
