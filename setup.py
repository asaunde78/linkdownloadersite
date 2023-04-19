from setuptools import setup, find_packages

setup(
    name='linkdownloadersite',
    version='0.1',
    author='Asher',
    author_email='saundersasher78@gmail.com',
    description='A loopback site designed for the CatScraper module',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'Flask',
        'requests'
    ],
)