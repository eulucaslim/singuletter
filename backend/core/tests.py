from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import News, Category, UserPreference

# Create your tests here.
class NewsViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="12345")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('news-list')
        self.category = Category.objects.create(name='Teste')
        self.news = News.objects.create(
            title="Notícia Inicial",
            content="Conteúdo original da notícia",
            category_id=self.category.id
        )
        self.detail_url = reverse('news-detail', args=[self.news.id])
        self.news_data = {
            "title": "Notícia Teste",
            "content": "Conteúdo da notícia",
            "category_id": self.category.id
        }

    def test_create_news(self):
        """Need to create a News """
        response = self.client.post(self.url, self.news_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], "Notícia Teste")
        self.assertEqual(response.data['data']['content'], "Conteúdo da notícia")

    def test_list_news(self):
        """ Return all News (GET /news/)"""
        News.objects.create(**self.news_data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_get_news_detail(self):
        """ Return the news specific (GET /news/{id}/)"""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.news.title)
        self.assertEqual(response.data['content'], self.news.content)

    def test_patch_news(self):
        """ Updated partial news (PATCH /news/{id}/)"""
        data = {"title": "Título Atualizado"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, "Título Atualizado")

    def test_delete_news(self):
        """ Remove the last notice (DELETE /news/{id}/)"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(News.objects.count(), 0)

class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="12345")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('preferences-list')
        self.category = Category.objects.create(name='Teste')
        self.detail_url = reverse('preferences-detail', args=[self.category.id])
        self.category_data = {
            "name": "Inteligencia Artificial",
        }

    def test_create_categories(self):
        """Need to create a Category """
        response = self.client.post(self.url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], "Inteligencia Artificial")

    def test_list_categories(self):
        """ Return all Category (GET /preferences/)"""
        Category.objects.create(**self.category_data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_category_detail(self):
        """ Return the category specific (GET /preferences/{id}/)"""
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id) 
        self.assertEqual(response.data['name'], self.category.name)

    def test_patch_category(self):
        """ Updated partial preferences (PATCH /preferences/{id}/)"""
        data = {"name": "Software Engineer"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Software Engineer")

    def test_delete_preferences(self):
        """ Remove the last notice (DELETE /preferences/{id}/)"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

class UserPreferenceViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="lucas", password="123456")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create categories to add in User
        self.cat1 = Category.objects.create(name="Tecnologia")
        self.cat2 = Category.objects.create(name="Esportes")
        self.cat3 = Category.objects.create(name="Política")

        # Create user preference
        self.pref = UserPreference.objects.create(user=self.user)
        self.pref.categories.set([self.cat1, self.cat2])

        self.url = "/users/me/preferences/"

    def test_get_user_preferences(self):
        """ Return user preferences """
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = [c["name"] for c in response.data["categories"]]
        self.assertIn("Tecnologia", categories)
        self.assertIn("Esportes", categories)
        self.assertNotIn("Política", categories)

    def test_creates_user_preference_if_not_exists(self):
        """Create a user preference case not exists (GET /users/me/preferences/)"""
        self.pref.delete()
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserPreference.objects.filter(user=self.user).exists())

    def test_patch_updates_categories(self):
        """Update user categories (PUT /users/me/preferences/)"""
        data = {"category_ids": [self.cat2.id, self.cat3.id]}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pref.refresh_from_db()

        updated_names = list(self.pref.categories.values_list("name", flat=True))
        self.assertIn("Esportes", updated_names)
        self.assertIn("Política", updated_names)
        self.assertNotIn("Tecnologia", updated_names)

    def test_requires_authentication(self):
        """ Error to use client not authenticated """
        client = APIClient()
        response = client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)