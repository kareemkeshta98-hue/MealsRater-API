from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Meal, Rating


class MealsRaterTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='StrongPass12345'
        )
        self.token = Token.objects.create(user=self.user)
        self.meal = Meal.objects.create(title='Pizza', description='Cheese pizza')
        self.rate_url = f'/API/meals/{self.meal.id}/rate_meal/'

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register_returns_token(self):
        response = self.client.post(
            '/API/users/',
            {'username': 'newuser', 'password': 'StrongPass12345'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)

    def test_meals_without_token_returns_401(self):
        response = self.client.get('/API/meals/')
        self.assertEqual(response.status_code, 401)

    def test_rate_meal_creates_rating(self):
        self.authenticate()
        response = self.client.post(self.rate_url, {'stars': 4}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Rating.objects.count(), 1)

    def test_rate_same_meal_twice_updates(self):
        self.authenticate()
        first = self.client.post(self.rate_url, {'stars': 4}, format='json')
        second = self.client.post(self.rate_url, {'stars': 2}, format='json')
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get().stars, 2)

    def test_invalid_stars_returns_400(self):
        self.authenticate()
        too_high = self.client.post(self.rate_url, {'stars': 7}, format='json')
        missing = self.client.post(self.rate_url, {}, format='json')
        self.assertEqual(too_high.status_code, 400)
        self.assertEqual(missing.status_code, 400)

    def test_user_sees_only_own_ratings(self):
        other = User.objects.create_user(username='other', password='StrongPass12345')
        Rating.objects.create(user=other, meal=self.meal, stars=5)
        self.authenticate()
        response = self.client.get('/API/ratings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)