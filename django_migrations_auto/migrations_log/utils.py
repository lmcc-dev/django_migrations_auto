# -*- coding: utf-8 -*-
from django.db import connection, models

def create_table(tab_model, cursor=None):
    """Create database table and its indexes based on the model definition."""
    if not cursor:
        cursor = connection.cursor()
    assert cursor, 'Database cursor not set'
    assert issubclass(tab_model, models.Model), '{0} is not a database model'.format(tab_model)

    # Generate the CREATE TABLE SQL statement
    create_table_sql = generate_create_table_sql(tab_model)

    # Execute the CREATE TABLE SQL statement
    cursor.execute(create_table_sql)
    print(f"Table {tab_model._meta.db_table} created successfully.")

    # Generate and execute the CREATE INDEX SQL statements
    create_index_sqls = generate_create_index_sql(tab_model)
    for create_index_sql in create_index_sqls:
        cursor.execute(create_index_sql)
        print(f"Index created with SQL: {create_index_sql}")

def get_table_list(cursor=None):
    """Get list of database tables."""
    if not cursor:
        cursor = connection.cursor()
    return connection.introspection.get_table_list(cursor)

def table_exists(table_name, cursor=None):
    """Check if a table exists in the database."""
    table_list = set(table.name for table in get_table_list(cursor=cursor))
    return table_name in table_list


def generate_create_table_sql(model):
    """Generate the SQL CREATE TABLE statement for a Django model."""
    table_name = model._meta.db_table
    fields = []

    for field in model._meta.fields:
        column_name = field.column
        column_type = field.db_type(connection)
        not_null = " NOT NULL" if not field.null else ""
        primary_key = " PRIMARY KEY" if field.primary_key else ""
        unique = " UNIQUE" if field.unique else ""
        default = ""
        if field.has_default():
            default_value = field.get_default()
            if isinstance(default_value, str):
                default_value = f"'{default_value}'"
            default = f" DEFAULT {default_value}"
        field_sql = f"{column_name} {column_type}{not_null}{primary_key}{unique}{default}"
        fields.append(field_sql)

    fields_sql = ",\n    ".join(fields)
    create_table_sql = f"CREATE TABLE {table_name} (\n    {fields_sql}\n);"

    return create_table_sql


def generate_create_index_sql(model):
    """Generate the SQL CREATE INDEX statements for a Django model."""
    table_name = model._meta.db_table
    index_sqls = []

    for index in model._meta.indexes:
        index_name = index.name
        columns = ', '.join([field.column for field in index.fields])
        unique = "UNIQUE" if index.unique else ""
        create_index_sql = f"CREATE {unique} INDEX {index_name} ON {table_name} ({columns});"
        index_sqls.append(create_index_sql)

    return index_sqls



