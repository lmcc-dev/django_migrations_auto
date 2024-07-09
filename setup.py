# -*- coding: utf-8 -*-
# setup.py
from setuptools import setup, find_packages

setup(
    name='django_migrations_auto',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app to store migrations in the database and apply them automatically.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lmcc-dev/django_migrations_auto',
    author='lmcc',
    author_email='lmccc.dev@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=3.2',
    ],
    python_requires='>=3.7',
)