from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as app_models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Clean up collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email for users
        db.users.create_index('email', unique=True)

        # Teams
        marvel_team = {'name': 'Team Marvel', 'description': 'Superheroes from Marvel Universe'}
        dc_team = {'name': 'Team DC', 'description': 'Superheroes from DC Universe'}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_team_id},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team_id': dc_team_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user_id': user_ids[0], 'type': 'run', 'duration': 30, 'distance': 5},
            {'user_id': user_ids[1], 'type': 'cycle', 'duration': 60, 'distance': 20},
            {'user_id': user_ids[2], 'type': 'swim', 'duration': 45, 'distance': 2},
            {'user_id': user_ids[3], 'type': 'run', 'duration': 25, 'distance': 4},
            {'user_id': user_ids[4], 'type': 'cycle', 'duration': 70, 'distance': 22},
            {'user_id': user_ids[5], 'type': 'swim', 'duration': 50, 'distance': 2.5},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'name': 'Morning Cardio', 'description': 'Cardio session for all'},
            {'name': 'Strength Training', 'description': 'Strength and resistance workout'},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 80},
            {'user_id': user_ids[3], 'points': 110},
            {'user_id': user_ids[4], 'points': 95},
            {'user_id': user_ids[5], 'points': 85},
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database has been populated with test data.'))
