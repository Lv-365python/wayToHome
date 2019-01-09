"""This module provides tests for Way views"""
import json

from django.test import TestCase, Client
from django.urls import reverse

from custom_user.models import CustomUser
from way.models import Way


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
				"id": 100,
				'name': 'test_name',
				'user_id': 100,
				'routes': []
			}

		]
		url = reverse('way', args=[])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(json.dumps(expected_response), json.loads(response.content))

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

		data = {
			'name': 'test_name',
			"gmaps_response":[{
				"travel_mode": "WALKING",
				"start_location": {
					"lat": 41.8507300,
					"lng": -87.6512600
				},
				"end_location": {
					"lat": 41.8525800,
					"lng": -87.6514100
				},
				"polyline": {
					"points": "a~l~Fjk~uOwHJy@P"
				},
				"duration": {
					"value": "00:00:19",
					"text": "1 min"
				},
				"html_instructions": "",
				"distance": {
					"value": 207,
					"text": "0.1 mi"
				}
			}]
		}

		expected_data = {
			'way': {
				'id': 2,
				'name': 'test_name',
				'user_id': 100
			},
			'routes': [
				{
					'end_place': {'latitude': 41.85258, 'longitude': -87.65141},
					'start_place': {'latitude': 41.85073, 'longitude': -87.65126},
					'time': '00:00:19'
				}
			]
		}

		url = reverse('way', args=[])
		response = self.client.post(url, json.dumps(data), content_type='application/json')
		response_dict = json.loads(response.content)

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

	def test_put(self):
		"""Method that test success put request for the updating the certain task."""
		data = {
			'name': 'new_name'
		}

		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.put(url, json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 200)

	def test_put_invalid_data(self):
		"""Method that tests unsuccessful put request with invalid data."""

		data = {
			'name': 23423432,
		}
		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.post(url, json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 400)

	def test_put_non_owner(self):
		"""Method that tests for request to update non owner Way instance."""
		another_user = CustomUser(id=101, email='new_mail@gmail.com', is_active=True)
		another_user.set_password('12345aaa')
		another_user.save()
		self.client.login(email='new_mail@gmail.com', password='12345aaa')

		data = {
			'name': 'new_test_name'
		}
		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.put(url, json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 403)

	def test_put_empty_json(self):
		"""Method that tests unsuccessful put request with empty JSON data."""
		data = {}
		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.put(url, json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 400)

	def test_put_wrong_id(self):
		"""Method that tests request to update non existent object."""
		data = {
			'name': 'new_test_name',
		}

		url = reverse('way', kwargs={'way_id': 1509})
		response = self.client.put(url, json.dumps(data), content_type='application/json')
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