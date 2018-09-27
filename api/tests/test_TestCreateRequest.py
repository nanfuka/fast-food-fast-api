from flask_testing import TestCase
from app import app
import unittest
import json
from api.tests.Basetest import BaseTest


class TestCreateRequests(BaseTest):

    def test_if_URL_exists(self):
        """ Check if URL path exists and is protected"""
        response = self.client.post('/api/v1/orders')
        assert "401 UNAUTHORIZED" == response.status

    def test_api_check_non_authorised_user(self):
        """"Test for non authenticated user"""
        with self.client:
            response = self.client.post('/api/v1/orders')
            reply = json.loads(response.data.decode())
            self.assertEquals(reply["success"], False)
            self.assertEquals(
                reply["message"],
                "You are not authorised to access this page.")

    def test_api_when_no_parameters_have_been_passed(self):
        """Test for authenticated user but no parameters"""
        with self.client:
            head = {'Authorization': self.get_auth_token()}
            response = self.client.post(
                '/api/v1/orders', headers=head, data=json.dumps({}))
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['success'], False)
            self.assertEquals(reply['message'], 'All fields required.')

    def test_api_when_parameters_have_been_passed(self):
        """Test for authenticated and parameters provided"""
        with self.client:
            head = {'Authorization': self.get_auth_token(
            ), 'content_type': 'application/json'}
            request = {'food_order': 'bacon',
                       'description': 'fresh', 'quantity': '3'}
            response = self.client.post(
                '/api/v1/orders', headers=head, data=json.dumps(request))
            reply = json.loads(response.data.decode())
            assert "200 OK" == response.status
            self.assertEquals(reply['success'], True)
            self.assertEquals(reply['message'],
                              'Your request was submitted successfully.')
