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

		Place.objects.create(
			id=11,
			longitude=49.842601,
			latitude=23.968448,
			address='Широка 34, 79052',
			name='Дім',
			stop_id=None,
		)

		self.way = Way.objects.get(id=100)
		self.place = Place.objects.get(id=11)
		self.client = Client()
		self.client.login(email='mail@gmail.com', password='Password1234')

	def test_get_one(self):
		"""Provide tests for request to retrieve certain Way instance."""
		expected_response = {
			'name': 'test_name',
			'user_id': 100,
			'routes': []
		}
		url = reverse('way', kwargs={'way_id': self.way.id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		actual_response = json.loads(response.content)
		actual_response.pop('id')
		self.assertJSONEqual(json.dumps(expected_response), actual_response)

	def test_get_all(self):
		"""Provide tests for request to retrieve all user Ways"""
		expected_response = [
			{
				"name": 'new_test_name',
				"user_id": 100,
				'routes': []
			},
			{
				'name': 'test_name',
				'user_id': 100,
				'routes': []
			}

		]
		url = reverse('way', args=[])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		actual_response = json.loads(response.content)
		actual_response[0].pop('id')
		actual_response[1].pop('id')

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

		data = {
			'name': 'test_name',
			'start_place': self.place.id,
			'end_place': self.place.id,
			"steps": [{
				"start_location": {"lat": 40.8507300, "lng": -86.6512600},
				"end_location": {"lat": 41.8525900, "lng": -87.1524100},
				"duration": {"value": 190},
				"transit": {"line": {
					"short_name": "3A",
					"vehicle": {"type": "BUS"}
				}}
			}, {
				"start_location": {"lat": 41.8507300, "lng": -87.6512600},
				"end_location": {"lat": 41.8525800, "lng": -87.9514100},
				"duration": {"value": 190},
				"transit": {"line": {
					"short_name": "12",
					"vehicle": {"type": "TROLLEYBUS"}
				}}
			}, {
				"start_location": {"lat": 41.8507300, "lng": -87.6512600},
				"end_location": {"lat": 41.8525800, "lng": -87.6514100},
				"duration": {"value": 190},
				"transit": {"line": {
					"short_name": "12",
					"vehicle": {"type": "TRAM"}
				}}
			}]
		}

		expected_data = {
			'name': 'test_name',
			'user_id': 100,
			'routes': [{
				'transport_name': 'А03',
				'position': 0,
				'time': '00:03:10'
			}, {
				'transport_name': 'Тр12',
				'position': 1,
				'time': '00:03:10'
			}, {
				'transport_name': 'Т12',
				'position': 2,
				'time': '00:03:10'
			}]
		}

		url = reverse('way', args=[])
		response = self.client.post(url, json.dumps(data), content_type='application/json')
		response_dict = json.loads(response.content)
		response_dict.pop('id')
		for route in response_dict['routes']:
			route.pop('id')
			route.pop('start_place')
			route.pop('end_place')
			route.pop('way')

		self.assertEqual(response.status_code, 201)
		self.assertDictEqual(response_dict, expected_data)

	def test_post_create_fail(self):
		"""Method that tests when way was not created"""

		data = {
			'name': 'test_name',
			'start_place': self.place.id,
			'end_place': self.place.id,
		}
		url = reverse('way')

		with mock.patch('way.views.Way.create') as mock_way:
			mock_way.return_value = False
			response = self.client.post(url, json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 400)

	def test_post_invalid_data(self):
		"""Method that tests unsuccessful post request with invalid post data."""

		data = {
			'name': {},
		}
		url = reverse('way', args=[])
		response = self.client.post(url, json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 400)

	def test_post_create_route_fail(self):
		"""Method that tests when route in way post method was not created"""

		data = {
			'name': 'test_name',
			'start_place': self.place.id,
			'end_place': self.place.id,
			"steps": [{
				"start_location": {"lat": 40.8507300, "lng": -86.6512600},
				"end_location": {"lat": 41.8525900, "lng": -87.1524100},
				"duration": {"value": 190},
			}, {
				"start_location": {"lat": 41.8507300, "lng": -86.6512600},
				"end_location": {"lat": 41.8525800, "lng": -87.9514100},
				"duration": {"value": 190},
				"transit": {"line": {
					"short_name": "12",
					"vehicle": {"type": "SHARE_TAXI"}
				}}

			}, {
				"start_location": {"lat": 41.8507300, "lng": -87.6512600},
				"end_location": {"lat": 41.8525800, "lng": -87.6514100},
				"duration": {"value": 190},
			}]
		}
		url = reverse('way')

		with mock.patch('way.views.Way') as mock_way:
			mock_way._create_route.return_value = False
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
