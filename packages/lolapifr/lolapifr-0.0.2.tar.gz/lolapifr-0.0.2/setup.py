from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'API de League of Legends en français'

DOCU = 'tkt'

setup(
    name='lolapifr',
    version=VERSION,
    description=DESCRIPTION,
    long_description=DOCU,
    author='Manolo',
    author_email='emmanuelardoin@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>2.28.0',
        'python-dotenv>0.21.1',
    ],
)