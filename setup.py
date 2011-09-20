import os
from setuptools import setup

setup(
    name = "restler",
    version = "0.1",
    author = "Curtis Thompson",
    author_email = "curtis.thompson@gmail.com",
    description = "Restler provides flexible and configurable JSON and XML object serialization for the web",
    license = "XYZ",
    keywords = "serialization json xml",
    url = "https://bitbucket.org/curtis/restler",
    packages=['restler'],
    long_description=open("README.txt").read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: Utilities",
        # TBD: License
    ],
)
