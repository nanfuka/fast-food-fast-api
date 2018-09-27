from unittest import TestCase
from flask import json
from app import app
from api.model.User import User
import unittest


class BaseTest(TestCase):

    def setUp(self):
        """
        initialise the app module
        create a pytest fixture called client() 
        that configures the application for testing
        """
        self.app = app
        self.context = self.app.app_context()
        self.context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Release Context"""
        self.context.pop()

    def get_auth_token(self):
        """create token from login"""
        response = self.client.post('/api/v1/login',
                                    content_type='application/json',
                                    data=json.dumps(dict(username='Deb',
                                                         password='boosiko')))
        reply = json.loads(response.data.decode())
        self.assertEquals(reply['success'], True)
        if reply['success']:
            return reply['token']
        else:
            return None

    def get_request_id(self):
        """Get Request Id for Test Purposes"""
        head = {'Authorization': self.get_auth_token(
        ), 'content_type': 'application/json'}

        request = {'food_order': 'bacon',
                   'description': 'fresh', 'quantity': '3'}
        response = self.client.post(
            '/api/v1/orders', headers=head, data=json.dumps(request))
        reply = json.loads(response.data.decode())
        assert "200 OK" == response.status
        if reply['success']:
            return reply['data']['id']
