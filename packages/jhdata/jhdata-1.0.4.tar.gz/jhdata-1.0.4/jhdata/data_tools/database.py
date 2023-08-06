import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy import Table, MetaData, select, insert, delete

from jhdata.filehelper import Files
from jhdata.data_tools.dataframes import *


def create_schema_if_not_exists(schema_name: str, filehelper=None):
    filehelper = filehelper if filehelper is not None else Files
    engine = filehelper.get_engine()
    if schema_name not in engine.dialect.get_schema_names(engine):
        engine.execute(CreateSchema(schema_name))


def create_table_if_not_exists(table_name: str, table_schema = None, schema_name: str = None, filehelper = None):
    filehelper = filehelper if filehelper is not None else Files
    table_schema = table_schema if table_schema is not None else filehelper.read_table_schema(table_name, schema_name)
    engine = filehelper.get_engine()

    inspector = inspect(engine)

    if schema_name is not None:
        create_schema_if_not_exists(schema_name, filehelper)

    if not inspector.has_table(table_name, schema=schema_name):
        filehelper.write_sql(table_name, table_schema.make_df(), schema=schema_name)

    return Table(table_name, MetaData(engine), autoload_with=engine, schema=schema_name)


def table_exists(table_name: str, schema_name: str = None, filehelper = None):
    filehelper = filehelper if filehelper is not None else Files
    engine = filehelper.get_engine()

    inspector = inspect(engine)
    return inspector.has_table(table_name, schema=schema_name)


def upsert(update_df: pd.DataFrame, table_name: str, table_schema = None, schema_name: str = None, filehelper = None):
    filehelper = filehelper if filehelper is not None else Files
    table_schema = table_schema if table_schema is not None else filehelper.read_table_schema(table_name, schema_name)

    create_table_if_not_exists(table_name, table_schema, schema_name, filehelper)

    current_df = filehelper.read_sql_table(table_name, schema=schema_name)
    updated_df = upsert_dataframes(current_df, update_df, table_schema)

    return filehelper.write_sql(table_name, updated_df, schema=schema_name, table_schema=table_schema)


def insert_missing(update_df: pd.DataFrame, table_name: str, table_schema = None, schema_name: str = None, filehelper = None):
    filehelper = filehelper if filehelper is not None else Files
    table_schema = table_schema if table_schema is not None else filehelper.read_table_schema(table_name, schema_name)

    create_table_if_not_exists(table_name, table_schema, schema_name, filehelper)

    current_df = filehelper.read_sql_table(table_name, schema=schema_name)
    updated_df = append_missing_values(current_df, update_df, table_schema)

    return filehelper.write_sql(table_name, updated_df, schema=schema_name, table_schema=table_schema)


def insert_one(item: dict, table_name: str, table_schema = None, schema_name: str = None, filehelper = None):
    filehelper = filehelper if filehelper is not None else Files
    table_schema = table_schema if table_schema is not None else filehelper.read_table_schema(table_name, schema_name)

    table = create_table_if_not_exists(table_name, table_schema, schema_name, filehelper)

    statement = insert(table).values(**item)
    print(statement)

    return filehelper.sql(statement)
