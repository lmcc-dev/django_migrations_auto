# -*- coding: utf-8 -*-

# migrations_log/models.py

import datetime
import os
import glob
import shutil
from importlib import import_module
from django.db import models, connection
from django.utils.module_loading import module_dir
from django.db.migrations.loader import MigrationLoader
from .utils import create_table, table_exists

class MigrationsDBLogManager(models.Manager):
    def create_log_table(self):
        """Create the migrations log table."""
        cursor = connection.cursor()
        #self.model._meta.db_table = 'django_migrations_db_log'
        if not table_exists(self.model._meta.db_table, cursor=cursor):
            print(f'Creating migrations table: {self.model._meta.db_table}')
            try:
                create_table(self.model, cursor=cursor)
            except Exception as e:
                print(e)

    def load_files(self, app):
        """Load migration files from the database."""
        migrations_package_name, _ = MigrationLoader.migrations_module(app)
        try:
            base_module_path = import_module(".".join(migrations_package_name.split('.')[:-1]))
            base_dir = module_dir(base_module_path)
            migrations_dir = os.path.join(base_dir, migrations_package_name.split('.')[-1])
        except ModuleNotFoundError:
            return

        if not os.path.isdir(migrations_dir):
            os.makedirs(migrations_dir)
            open(os.path.join(migrations_dir, '__init__.py'), 'w').close()

        self._clean_and_save_files(migrations_dir, app)

    def _clean_and_save_files(self, migrations_dir, app):
        """Clean and save migration files."""
        for file in glob.glob(os.path.join(migrations_dir, '*')):
            file_name = os.path.basename(file)
            if file_name.startswith('__init__.'):
                continue
            elif os.path.isdir(file) and file_name == '__pycache__':
                shutil.rmtree(file)
            else:
                self._process_migration_file(app, file, file_name, migrations_dir)

    def _process_migration_file(self, app, file_path, file_name, migrations_dir):
        """Process a single migration file."""
        if os.path.isfile(file_path) and os.path.basename(os.path.dirname(file_path)) == 'migrations':
            if self.filter(app=app, name=file_name).exists():
                print(f'Cleaning {app}: {file_path}')
                os.unlink(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                defaults = {'content': content, 'applied': datetime.datetime.now()}
                print(f'Saving {app}: {file_path}')
                MigrationsDBLog.objects.get_or_create(defaults=defaults, app=app, name=file_name)

        for migration_obj in self.filter(app=app).order_by('applied').all():
            obj_path = os.path.join(migrations_dir, migration_obj.name)
            print(f'Loading {app}: {obj_path}')
            with open(obj_path, "w", encoding='utf-8') as file:
                file.write(migration_obj.content)


class MigrationsDBLog(models.Model):
    app = models.CharField('App', max_length=255)
    name = models.CharField('Migration Name', max_length=255, db_index=True)
    content = models.TextField('Migration Content')
    applied = models.DateTimeField('Applied Date')

    objects = MigrationsDBLogManager()

    class Meta:
        verbose_name = 'Migrations DB Log'
        verbose_name_plural = verbose_name
        unique_together = [('app', 'name')]
        managed = False

