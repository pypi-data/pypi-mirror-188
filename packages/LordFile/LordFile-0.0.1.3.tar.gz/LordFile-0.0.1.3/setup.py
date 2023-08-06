
import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='LordFile',
    version='0.0.1.3',
    url='https://git.lordbex.xyz/PipModule/LordFile',
    license='',
    author='lordbex',
    author_email='lordibex@protonmail.com',
    description='File Manager',
    long_description=read('README.rst'),
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'regex', 'pyyaml', 'LordUtils'
    ],
    classifiers=[
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])