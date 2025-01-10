from setuptools import setup
import io
import os
import re

def read(*names, **kwargs):
    """Python 2 and Python 3 compatible text file reading.
    Required for single-sourcing the version string.
    """
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    """
    Search the file for a version string.
    file_path contain string path components.
    Reads the supplied Python module as text without importing it.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = find_version('rb', '__init__.py')


setup(
    name='pyrb',
    version=version,   
    description='Radiobarrier protocols library',
    url='http://gitlabs.uniscan.biz/radiobarier/pyrb',
    author='Andrey Bykov',
    author_email='bykov.a@uniscan.biz',
    license='BSD 2-clause',
    packages=['rb'],
    install_requires=['pyserial>=3.5'],

    classifiers=[
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator'
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
    ],
)