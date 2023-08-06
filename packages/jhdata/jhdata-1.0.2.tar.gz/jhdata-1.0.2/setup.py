from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "jhdata"
DESCRIPTION = "Abstractions around cloud file interfaces (WIP)"
URL = "https://github.com/jothapunkt/jhdata"
EMAIL = "jakob-hoefner@web.de"
AUTHOR = "Jothapunkt"
VERSION = "1.0.2"
REQUIRED = [
    "boto3",
    "s3fs",
    "pandas",
    "pyarrow",
    "sqlalchemy"
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    install_requires=REQUIRED,
    url=URL,
    packages=["jhdata"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8"
)
