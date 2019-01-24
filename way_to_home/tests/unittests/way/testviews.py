"""This module provides tests for Way views"""

import json

from django.test import TestCase, Client
from django.urls import reverse
from unittest import mock

from custom_user.models import CustomUser
from way.models import Way
from place.models import Place


class WayViewsTestCase(TestCase):
	"""TestCase for providing View views testing"""

	def setUp(self):
		"""Method that provides preparation before testing Way views."""
		user = CustomUser(id=100, email='mail@gmail.com', is_active=True)
		user.set_password('Password1234')
		user.save()

		Way.objects.create(
			id=100,
			name='test_name',
			user=user
		)

		Way.objects.create(
			id=101,
			name='new_test_name',
			user=user
		)

		self.way = Way.objects.get(id=100)
		self.client = Client()
		self.client.login(email='mail@gmail.com', password='Password1234')

	def test_get_one(self):
		"""Provide tests for request to retrieve certain Way instance."""
		expected_response = {
			"id": 100,
			'name': 'test_name',
			'user_id': 100,
			'routes': []
		}
		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(json.dumps(expected_response), json.loads(response.content))

	def test_get_all(self):
		"""Provide tests for request to retrieve all user Ways"""
		expected_response = [
			{
				'id': 101,
				"name": 'new_test_name',
				"user_id": 100,
				'routes': []
			},
			{
				'id': 100,
				'name': 'test_name',
				'user_id': 100,
				'routes': []
			}

		]
		url = reverse('way', args=[])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		actual_response = json.loads(response.content)
		self.assertJSONEqual(json.dumps(expected_response), actual_response)

	def test_get_wrong_id(self):
		"""Method that tests request to retrieve non existent object."""
		url = reverse('way', args=[1501])
		response = self.client.get(url)

		self.assertEqual(response.status_code, 400)

	def test_get_non_owner(self):
		"""Method that tests for request to retrieve non owner Way instance."""
		another_user = CustomUser(id=101, email='new_mail@gmail.com', is_active=True)
		another_user.set_password('12345aaa')
		another_user.save()
		self.client.login(email='new_mail@gmail.com', password='12345aaa')

		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 403)

	def test_post(self):
		"""Method that tests the success post request for creating Way."""

		Place.objects.create(
			id=11,
			longitude=49.842601,
			latitude=23.968448,
			address='Широка 34, 79052',
			name='Дім',
			stop_id=None,
		)

		data = {
			'name': 'test_name',
			'start_place': 11,
			'end_place': 11,
			"steps": [{
				"Dep": {
					"Stn": {
						"y": 41.8507300,
						"x": -87.6512600
					}
				},
				"Arr": {
					"Stn": {
						"y": 40.8507300,
						"x": -77.6512600
					}
				},

				"Journey": {
					"duration": "PT13M"
				},
			}]
		}

		expected_data = {
			'name': 'test_name',
			'routes': [{
				'position': 0,
				'time': '00:13:00',
				'transport_id': None,
				'way': 2}],
			'user_id': 100}

		url = reverse('way', args=[])
		response = self.client.post(url, json.dumps(data), content_type='application/json')
		response_dict = json.loads(response.content)
		response_dict.pop('id')
		response_dict['routes'][0].pop('id')
		response_dict['routes'][0].pop('start_place')
		response_dict['routes'][0].pop('end_place')

		self.assertEqual(response.status_code, 201)
		self.assertDictEqual(response_dict, expected_data)

	def test_post_invalid_data(self):
		"""Method that tests unsuccessful post request with invalid post data."""

		data = {
			'name': {},
		}
		url = reverse('way', args=[])
		response = self.client.post(url, json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 400)

	def test_post_empty_json(self):
		"""Method that tests unsuccessful post request with empty JSON data."""

		data = {}
		url = reverse('way', args=[])
		response = self.client.post(url, json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 400)

	def test_delete(self):
		"""Method that tests successful delete request"""

		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 200)

	def test_delete_wrong_id(self):
		"""Method that tests request to delete non existent object."""

		url = reverse('way', kwargs={'way_id': 1509})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 400)

	def test_delete_non_owner(self):
		"""Method that tests for request to delete non owner Way instance."""
		another_user = CustomUser(id=101, email='new_mail@gmail.com', is_active=True)
		another_user.set_password('12345aaa')
		another_user.save()
		self.client.login(email='new_mail@gmail.com', password='12345aaa')

		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.delete(url)

		self.assertEqual(response.status_code, 403)

	def test_delete_db_fail(self):
		"""Method that tests the unsuccessful request to delete way in case of database failure."""
		url = reverse('way', kwargs={'way_id': self.way.id})
		with mock.patch('way.views.Way.delete_by_id') as delete_by_id:
			delete_by_id.return_value = False
			response = self.client.delete(url)
			self.assertEquals(response.status_code, 400)
