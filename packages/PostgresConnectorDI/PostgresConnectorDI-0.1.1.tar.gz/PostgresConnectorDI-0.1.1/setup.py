from setuptools import setup, find_packages

setup(
    name="PostgresConnectorDI",
    version="0.1.1",
    author="José Pulido",
    author_email='jpulido@dataint.mx',
    install_requires=['sqlalchemy','pandas','psycopg2-binary']
)
