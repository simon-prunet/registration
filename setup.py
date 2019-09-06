from setuptools import setup, Extension, find_packages
import io
import codecs
import os
import sys


packages = find_packages(where=".")

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    


setup(
    name='register',
    version=0.1,
    url='https://github.com/simon-prunet/register',
    license='GPLv3+',
    author='Simon Prunet',
    author_email='prunet@cfht.hawaii.edu',
    maintainer='Simon Prunet',
    maintainer_email='prunet@cfht.hawaii.edu',
    description="Image registration software",
    long_description=long_description,
    packages=packages,
    package_dir={"": "."},
    include_package_data=True,
    package_data={
        '':['LICENSE.txt', '*.md', '*.txt', 'docs/*', '*.pyx'],
        'orbs':['data/*', '*.pyx']},
    exclude_package_data={
        '': ['*~', '*.so', '*.pyc'],
        'orbs':['*~', '*.so', '*.pyc', '*.c']},
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Cython',
        'Development Status :: 0 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent' ],
)

