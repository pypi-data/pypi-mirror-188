import io
import os
import re
import requests

import jhdata.connections as conn
from jhdata.logger import *
from jhdata.data_tools.schemas import *
from jhdata.secrets import SecretInterfaceMemory

"""
Useful stuff:
JSON schemas: https://specs.frictionlessdata.io/table-schema/#types-and-formats
"""


class FileHelper:
    def __init__(self, bucket_name: str = None, logger: Logger = None, environment: str = None, engine = None, secrets = None):
        self.environment = environment if environment else os.getenv("ENVIRONMENT", "dev")
        self.bucket_name = bucket_name if bucket_name else self.environment
        self.logger = logger if logger else Logger()
        self.engine = engine
        self.secrets = secrets if secrets is not None else SecretInterfaceMemory()

    def set_engine(self, engine):
        self.engine = engine

    def get_engine(self):
        return self.engine if self.engine is not None else conn.db_engine

    def sql(self, statement, **kwargs):
        with self.engine.connect() as connection:
            with connection.begin():
                return connection.execute(statement, **kwargs)

    # Get path for s3fs
    def fspath(self, path: str):
        return f"{self.bucket_name}/{path}"

    def metadata(self, path: str):
        return conn.fs.metadata(self.fspath(path))

    # Last modified as datetime
    def last_modified(self, path: str) -> datetime.datetime:
        return conn.fs.modified(self.fspath(path))

    # Check if path is a directory
    def is_directory(self, path: str) -> bool:
        return conn.fs.isdir(self.fspath(path))

    # Check if a path exists
    def path_exists(self, path: str) -> bool:
        return conn.fs.exists(self.fspath(path))

    # Check if a path exists and is a directory
    def directory_exists(self, path: str) -> bool:
        return self.path_exists(path) and self.is_directory(path)

    # Check if a path exists and is a file
    def file_exists(self, path: str) -> bool:
        return self.path_exists(path) and not self.is_directory(path)

    def find(self, path: str, **kwargs):
        results = conn.fs.find(path=self.fspath(path), **kwargs)
        return ["/".join(result.split("/")[1:]) for result in results]

    def find_regex(self, path: str, regex: str, **kwargs):
        files = self.find(path, **kwargs)
        results = []

        for file in files:
            filename = file.split("/")[-1]
            match = re.search(regex, filename)
            if match is not None:
                results.append((file, match.groupdict()))

        return results

    # Generate an URL to access a file
    def url(self, path: str, **kwargs):
        return conn.fs.url(path=self.fspath(path), **kwargs)

    # Move file
    def move(self, path_from: str, path_to: str, recursive: bool = False):
        conn.fs.move(self.fspath(path_from), self.fspath(path_to), recursive=recursive)

    # Copy file
    def copy(self, path_from: str, path_to: str, recursive: bool = False):
        conn.fs.copy(self.fspath(path_from), self.fspath(path_to), recursive=recursive)

    # Delete file
    def delete(self, path: str, recursive: bool = False):
        conn.fs.rm(self, self.fspath(path), recursive=recursive)

    # Get a readable file object
    def get_readable(self, path: str):
        return conn.fs.open(self.fspath(path))

    # Get a readable file object
    def get_readable_bytes(self, path: str):
        return conn.fs.open(self.fspath(path), "rb")

    # Get a writeable file object
    def get_writeable(self, path: str):
        return conn.fs.open(self.fspath(path), "w")

    # Get a writeable file object
    def get_writeable_bytes(self, path: str):
        return conn.fs.open(self.fspath(path), "wb")

    # Download a file into a ByteIO object
    def read_byteio(self, path: str):
        output = io.BytesIO()
        conn.boto.Bucket(self.bucket_name).download_fileobj(Key=path, Fileobj=output)
        return output

    # Download file content as bytes
    def read_bytes(self, path: str):
        output = self.read_byteio(path)
        return output.getvalue()

    # Upload bytes into a file
    def write_bytes(self, path: str, data: bytes):
        self.logger.info(f"[{self.bucket_name}] Uploading bytes to {path}")
        result = conn.boto.Bucket(self.bucket_name).put_object(Key=path, Body=data)
        return result

    # Download a file from an URL to bucket using HTTP
    def download_file(self, url: str, to_path: str, **kwargs):
        self.logger.info(f"[{self.bucket_name}] Reading file bytes from {url}")
        response = requests.get(url=url, **kwargs)
        self.write_bytes(to_path, response.content)

    # Download file content as text
    def read_text(self, path: str, encoding: str = "utf8"):
        byte_content = self.read_bytes(path)
        return byte_content.decode(encoding)

    # Upload text into a file
    def write_text(self, path: str, text: str, encoding: str = "utf8"):
        self.logger.info(f"[{self.bucket_name}] Uploading text to {path}")
        result = conn.boto.Bucket(self.bucket_name).put_object(Key=path, Body=text.encode(encoding))
        return result

    # Read a JSON file into a Pandas DataFrame
    def read_json(self, path: str, **kwargs):
        return pd.read_json(self.get_readable(path), **kwargs)

    # Write to a JSON file
    def write_json(self, path: str, df: pd.DataFrame, **kwargs):
        return df.to_json(self.get_writeable(path), **kwargs)

    # Read a Parquet file into a Pandas DataFrame
    def read_parquet(self, path: str, **kwargs):
        return pd.read_parquet(self.get_readable(path), **kwargs)

    # Write to a parquet file
    def write_parquet(self, path: str, df: pd.DataFrame, **kwargs):
        return df.to_parquet(self.get_writeable_bytes(path), **kwargs)

    # Read a SQL table into a DataFrame
    def read_sql(self, table_name: str, table_schema: Schema = None, **kwargs):
        engine = self.get_engine()
        return pd.read_sql(table_name, engine, **kwargs)

    # Read a SQL table into a DataFrame
    def read_sql_table(self, table_name: str, table_schema: Schema = None, **kwargs):
        engine = self.get_engine()
        return pd.read_sql_table(table_name, engine, **kwargs)

    # Write a DataFrame into a SQL table
    def write_sql(self, table_name: str, df: pd.DataFrame, table_schema: Schema = None, if_exists="replace", index=False, **kwargs):
        engine = self.get_engine()
        result = df.to_sql(table_name, engine, if_exists=if_exists, index=index, **kwargs)
        print("Wrote to table", table_name, "- result:", result)

    # Read schema from disk
    def read_schema(self, path: str):
        schema_dict = json.loads(self.read_text(f"schemas/{path}.json"))
        print(schema_dict)
        return Schema(schema_dict)

    # Read schema from default location for a SQL table
    def read_table_schema(self, table_name: str, schema_name: str = None):
        if schema_name is None:
            return self.read_schema(table_name)
        else:
            return self.read_schema(f"{schema_name}/{table_name}")

    # Write schema to disk
    def write_schema(self, path: str, schema: Schema):
        schema_string = schema.to_json()
        self.write_text(f"schemas/{path}.json", schema_string)


Files = FileHelper()
