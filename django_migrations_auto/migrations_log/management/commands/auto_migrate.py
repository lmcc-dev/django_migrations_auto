# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from ...models import MigrationsDBLog
from django.apps import apps
from django.db import connections, DEFAULT_DB_ALIAS
import os

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automatically calls makemigrations and then applies migrations. Generates migration files from the database before applying.'

    def add_arguments(self, parser):
        parser.add_argument(
            'app_label',
            nargs='?',
            help='App label of the application to migrate.'
        )
        parser.add_argument(
            'migration_name',
            nargs='?',
            help='Database state to migrate to.'
        )
        parser.add_argument(
            '--database',
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Defaults to the "default" database.',
        )
        parser.add_argument(
            '--fake',
            action='store_true',
            help='Mark migrations as run without actually running them.',
        )
        parser.add_argument(
            '--fake-initial',
            action='store_true',
            help='Detect if tables already exist and fake-apply initial migrations if so.',
        )

    def handle(self, *args, **options):
        app_label = options.get('app_label')
        migration_name = options.get('migration_name')
        database = options.get('database')
        fake = options.get('fake')
        fake_initial = options.get('fake_initial')

        try:
            # Ensure the migrations log table exists
            logger.info('Ensuring the migrations log table exists...')
            MigrationsDBLog.objects.create_log_table()

            # Call the custom makemigrations command to create new migrations
            logger.info('Calling makemigrations...')
            call_command('makemigrations', verbosity=options.get('verbosity'), interactive=False)

            # Load migration files from the database before applying migrations
            logger.info('Loading migration files from the database...')
            self.load_migration_files_from_db()

            # Call the original migrate command
            logger.info('Applying migrations...')
            call_command('migrate',
                         app_label=app_label,
                         migration_name=migration_name,
                         database=database,
                         fake=fake,
                         fake_initial=fake_initial,
                         verbosity=options.get('verbosity'),
                         interactive=False)

            logger.info('Migrations applied successfully.')

        except CommandError as e:
            logger.error(f"CommandError: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error during auto_migrate: {e}")
            raise CommandError(f"An error occurred while running auto_migrate.  {e}")

    def load_migration_files_from_db(self):
        """Load migration files from the database and save them to the filesystem."""
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            migrations_module = app_config.name + '.migrations'

            # Check if the migrations module exists
            if not apps.is_installed(migrations_module):
                continue

            try:
                # Load existing migration files from the database
                MigrationsDBLog.objects.load_files(app_label)
            except Exception as e:
                logger.error(f"Failed to load migration files for app '{app_label}': {e}")
                raise CommandError(f"Failed to load migration files for app '{app_label}': {e}")