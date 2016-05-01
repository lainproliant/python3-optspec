from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='optspec',
    version='0.5',
    description='Wrapper around getopt for option mapping, counting, and parsing.',
    long_description=long_description,
    url='https://github.com/lainproliant/python3-optspec',
    author='Lain Supe (lainproliant)',
    author_email='lainproliant@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='argv parsing commandline',
    py_modules=["optspec"]
)

