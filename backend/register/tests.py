from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here.
class RegisterUserTests(APITestCase):

    def setUp(self):
        self.url = reverse('users')
    
    def test_create_user_success(self):
        """ Create a test user (POST /users/) """
        data = {
            "username": "lucas",
            "email": "lucas@example.com",
            "password": "StrongPass123!"
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['username'], "lucas")

    def test_create_user_missing_field(self):
        """ Fail because don't have email """
        data = {
            "username": "lucas",
            "password": "StrongPass123!"
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_user_weak_password(self):
        """ Fail because password is incorrect """
        data = {
            "username": "lucas",
            "email": "lucas@example.com",
            "password": "123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)