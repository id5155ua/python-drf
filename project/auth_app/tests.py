from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserTestCase(APITestCase):
    def test_create_user(self):
        url = reverse('user-create')
        data = {'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        # Check that the response is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the user was created and has the correct email
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, data['email'])

    def test_login(self):
        # Create a test user
        User.objects.create_user(email='testuser@example.com', password='testpassword')

        url = reverse('user-login')
        data = {'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the token is returned
        self.assertTrue('token' in response.data)

    def test_logout(self):
        # Create a test user
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)

        url = reverse('user-logout')
        response = self.client.post(url, format='json')

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the user's token has been deleted
        self.assertEqual(user.auth_token.key, '')


