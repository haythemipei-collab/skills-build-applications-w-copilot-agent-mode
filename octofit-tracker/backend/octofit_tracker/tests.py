from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Team, User, Activity, Workout, Leaderboard

class TeamTests(APITestCase):
	def test_create_team(self):
		url = reverse('api:team-list')
		data = {'name': 'Test Team', 'description': 'A test team'}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserTests(APITestCase):
	def setUp(self):
		self.team = Team.objects.create(name='Test Team', description='A test team')
	def test_create_user(self):
		url = reverse('api:user-list')
		data = {'name': 'Test User', 'email': 'test@example.com', 'team': self.team.id}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ActivityTests(APITestCase):
	def setUp(self):
		self.team = Team.objects.create(name='Test Team', description='A test team')
		self.user = User.objects.create(name='Test User', email='test@example.com', team=self.team)
	def test_create_activity(self):
		url = reverse('api:activity-list')
		data = {'user': self.user.id, 'type': 'run', 'duration': 30, 'distance': 5}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class WorkoutTests(APITestCase):
	def test_create_workout(self):
		url = reverse('api:workout-list')
		data = {'name': 'Morning Cardio', 'description': 'Cardio session'}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LeaderboardTests(APITestCase):
	def setUp(self):
		self.team = Team.objects.create(name='Test Team', description='A test team')
		self.user = User.objects.create(name='Test User', email='test@example.com', team=self.team)
	def test_create_leaderboard(self):
		url = reverse('api:leaderboard-list')
		data = {'user': self.user.id, 'points': 100}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
