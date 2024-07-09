# migrations_log/tests.py
from django.test import TestCase
from django.core.management import call_command
from django.apps import apps
from django.db import connection
from pathlib import Path
from django.conf import settings
import shutil
import importlib
import os

class MigrationsCommandsTestCase(TestCase):
    databases = '__all__'

    def setUp(self):
        super().setUp()
        self.migrations_dir = Path(os.path.join(settings.BASE_DIR,'django_migrations_auto','test_app', 'migrations'))
        self.app_dir = Path(os.path.join(settings.BASE_DIR, 'django_migrations_auto', 'migrations_log/test_app'))

        # Clean up old migration files and database tables
        self.clean_migrations()
        self.create_initial_migration()
        self.apply_initial_migration()

    def clean_migrations(self):
        """Clean up old migration files and database tables"""
        if self.migrations_dir.exists():
            shutil.rmtree(self.migrations_dir)
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS test_app_testmodel;")

    def create_initial_migration(self):
        """Create the initial migration for test_app"""
        call_command('makemigrations', 'test_app', verbosity=1)
        migration_files = list(self.migrations_dir.glob('*.py'))
        if migration_files:
            self.initial_migration_file = migration_files[0]


    def apply_initial_migration(self):
        """Apply the initial migration for test_app"""
        call_command('auto_migrate', 'test_app', verbosity=1)

    def test_makemigrations_command(self):
        """Test if the makemigrations command works correctly for test_app"""
        try:
            # Check if migration files are generated successfully
            self.assertTrue(self.migrations_dir.exists(), "Migrations directory should exist.")
            migration_files = list(self.migrations_dir.glob('*.py'))
            self.assertTrue(migration_files, "There should be migration files generated.")
        except Exception as e:
            self.fail(f"makemigrations command failed with error: {e}")


    def tearDown(self):
        super().tearDown()


