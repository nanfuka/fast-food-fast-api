from flask_testing import TestCase
from app import app
import unittest
import json
from api.tests.base_test import BaseTest


class TestSingleRequests(BaseTest):

    def test_if_URL_exists(self):
        """Test if the URL path is available"""
        response = self.client.get(
            '/api/v1/orders/{}'.format(self.get_request_id()))
        assert "401 UNAUTHORIZED" == response.status

    def test_api_check_non_authorised_user(self):
        """Test for non authenticated user"""
        with self.client:
            response = self.client.get(
                '/api/v1/orders/{}'.format(self.get_request_id()))
            reply = json.loads(response.data.decode())
            self.assertEquals(reply["success"], False)
            self.assertEquals(
                reply["message"],
                "You are not authorised to access this page.")

    def test_api_check_request(self):
        """Test for authenticated user"""
        with self.client:
            head = {'Authorization': self.get_auth_token()}
            response = self.client.get(
                '/api/v1/orders/{}'.format(
                    self.get_request_id()), headers=head)
            reply = json.loads(response.data.decode())
            assert "200 OK" == response.status
            self.assertEquals(reply['success'], True)
            self.assertEquals(reply['message'],
                              'Your request was submitted successfully.')
