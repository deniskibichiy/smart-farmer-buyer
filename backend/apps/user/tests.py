from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class UserAuthenticationTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.register_url = reverse('user-register')
		self.login_url = reverse('user-login')
		self.profile_url = reverse('user-profile')
		self.refresh_url = reverse('token-refresh')
		self.credentials = {
			'email': 'farmer@example.com',
			'username': 'farmer',
			'firstName': 'Casey',
			'lastName': 'Green',
			'password': 'HarvestPass123!',
			'confirmPassword': 'HarvestPass123!',
			'role': 'farmer',
		}

	def test_registration_returns_user_and_tokens(self):
		response = self.client.post(self.register_url, self.credentials, format='json')

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['user']['role'], 'FARMER')
		self.assertTrue(response.data['tokens']['access'])
		self.assertTrue(response.data['tokens']['refresh'])

	def test_login_returns_tokens_for_registered_user(self):
		self.client.post(self.register_url, self.credentials, format='json')

		response = self.client.post(self.login_url, {
			'email': self.credentials['email'],
			'password': self.credentials['password'],
		}, format='json')

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data['tokens']['access'])
		self.assertTrue(response.data['tokens']['refresh'])

	def test_access_token_authenticates_profile_request(self):
		registration = self.client.post(self.register_url, self.credentials, format='json')
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {registration.data['tokens']['access']}")

		response = self.client.get(self.profile_url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['email'], self.credentials['email'])

	def test_refresh_token_returns_new_access_token(self):
		registration = self.client.post(self.register_url, self.credentials, format='json')

		response = self.client.post(self.refresh_url, {
			'refresh': registration.data['tokens']['refresh'],
		}, format='json')

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data['access'])
