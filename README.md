# django-migrations-auto

![License](https://img.shields.io/badge/license-MIT-green)
[![Build Status](https://travis-ci.com/lmcc-dev/django_migrations_auto.svg?branch=main)](https://travis-ci.com/lmcc-dev/django_migrations_auto)
[![Coverage Status](https://coveralls.io/repos/github/lmcc-dev/django_migrations_auto/badge.svg?branch=main)](https://coveralls.io/github/lmcc-dev/django_migrations_auto?branch=main)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-migrations-auto.svg)](https://pypi.org/project/django-migrations-auto/)
[![PyPI Version](https://img.shields.io/pypi/v/django-migrations-auto.svg)](https://pypi.org/project/django-migrations-auto/)



A Django app to store migrations in the database and apply them automatically.

## Overview

`django-migrations-auto` is a Django application designed to manage database schema migrations by storing migration files in the database and applying them automatically. This approach simplifies deployment processes by reducing the need to maintain migration files across different environments.

### Key Features

- **Database Migration Logging**: Store migration files directly in the database.
- **Automatic Migration Application**: Automatically generate and apply migrations during deployment.
- **Version Control Integration**: Simplify version control by reducing the need to track migration files.
- **Custom Management Commands**: Enhanced `makemigrations` and `migrate` commands for streamlined migration management.
- **Environment and Database Consistency**: Ensure consistent deployment environments, databases, and migration files, eliminating the need to maintain different migration files in the version control repository.

## Installation

```bash
pip install django-migrations-auto
```


## Usage

### 1. Add to Installed Apps

Add `'django_migrations_auto.migrations_log'` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_migrations_auto.migrations_log',
]
```

### 2. Run Migrations
```bash 
python manage.py auto_migrate migrations_log
```
### 3. Custom Management Commands

#### `makemigrations`

This command generates new migrations based on the changes detected to your models.

Usage:

```bash
python manage.py makemigrations [app_label]
```
#### auto_migrate
This command runs makemigrations and migrate automatically, storing migration files in the database.
```bash 
python manage.py auto_migrate [app_label]
```

## Running Tests

To run the tests, first set up the test environment:

1. Ensure your `DATABASES` setting in `settings_test.py` points to a test database.

2.	Before running tests, ensure sqlite3 is updated by executing the `install_sqlite3.sh` script located in the test_app/scripts directory. This script checks the current version of sqlite3 and installs the required version if necessary.
3.	Run the tests using the following command:
```bash
DJANGO_SETTINGS_MODULE=django_migrations_auto.settings_test python manage.py test django_migrations_auto.tests
```
#### install_sqlite3.sh Script

The install_sqlite3.sh script is located in the test_app/scripts directory and is used to ensure that the correct version of sqlite3 is installed. This script is particularly useful for environments where the default sqlite3 version does not meet the minimum requirements for the application.

## Compatibility

This package is compatible with Django versions 3.2 to 5.0 and requires Python 3.7 to 3.12.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

### Steps to Contribute

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the maintainer at lmccc.dev@gmail.com.



