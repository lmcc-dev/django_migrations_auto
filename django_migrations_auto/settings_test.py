# -*- coding: utf-8 -*-
import sys
from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
     'TEST': {
         'NAME': 'memory',
        },
    }
}


try:
    from sqlite3 import dbapi2
    assert dbapi2.sqlite_version >= '3.8.3'
except Exception:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


INSTALLED_APPS += ['django_migrations_auto.test_app']


