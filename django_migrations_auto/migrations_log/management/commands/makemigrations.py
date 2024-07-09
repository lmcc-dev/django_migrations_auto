# -*- coding: utf-8 -*-
import logging
from django.core.management.commands import makemigrations
from ...models import MigrationsDBLog
from django.apps import apps
from django.db.migrations.writer import MigrationWriter
import datetime
import os
from django.conf import settings
from django.db import transaction

logger = logging.getLogger (__name__)


class Command (makemigrations.Command):
    def handle(self, *app_labels, **options):
        try:
            # Ensure the migrations log table exists
            MigrationsDBLog.objects.create_log_table ()

            # Get all app configurations
            all_apps = {config.label: config for config in apps.get_app_configs ()}
            _app_labels = app_labels if app_labels else [config.label for config in apps.get_app_configs ()]

            for app_label in _app_labels:
                app_config = all_apps.get (app_label)
                app_path = getattr(app_config, 'path', '')

                if app_path and app_path.startswith(str (settings.BASE_DIR)):
                    try:
                        # Load existing migration files from the database
                        MigrationsDBLog.objects.load_files(app_label)
                        # Call the original makemigrations command
                        super().handle(app_label, **options)
                    except Exception as e:
                        logger.error (f"Error processing app '{app_label}': {e}")
                        raise e
                else:
                    logger.info (f'Skip: {app_label} {app_path}')
                    super().handle (app_label, **options)
        except Exception as e:
            logger.error (f"Failed to handle makemigrations command: {e}")
            raise e

    def write_migration_files(self, changes, update_previous_migration_paths=None):
        """Save migration files to the database with rollback support."""
        for app_label, app_migrations in changes.items ():
            for migration in app_migrations:
                writer = MigrationWriter (migration, self.include_header)
                defaults = {'content': writer.as_string (), 'applied': datetime.datetime.now ()}

                if not os.path.exists (writer.path):
                    migration_name = os.path.basename (writer.path)
                    logger.info (f'Saving {app_label}: {migration_name}')

                    try:
                        with transaction.atomic ():
                            obj, created = MigrationsDBLog.objects.get_or_create (
                                defaults=defaults, app=app_label, name=migration_name
                            )
                            if created:
                                _changes = {app_label: [migration]}
                                super().write_migration_files(_changes)
                    except Exception as e:
                        logger.error (f"Failed to save migration file '{migration_name}' for app '{app_label}': {e}")
                        raise e
