from distutils.core import setup
from httperfpy import __version__

setup(
    name='httperfpy',
    version=__version__,
    author='Joshua P. Mervine',
    author_email='joshua@mervine.net',
    packages=['httperfpy'],
    url='http://github.com/jmervine/httperfpy',
    license='LICENSE.txt',
    description='Python wrapper for httperf.',
    long_description=open('README.md').read(),
)
