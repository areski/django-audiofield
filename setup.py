#! /usr/bin/env python
# coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import audiofield


def read(*parts):
    return open(os.path.join(os.path.dirname(__file__), *parts)).read()


setup(
    name='django-audiofield',
    version=audiofield.__version__,
    description='Django application to upload and convert audio files (mp3, wav and ogg format)',
    long_description=read('README.rst'),
    url='http://github.com/Star2Billing/django-audiofield',
    author='Belaid Arezqui',
    author_email='areski@gmail.com',
    license='MIT License',
    zip_safe=False,
    packages=[
        'audiofield',
    ],
    include_package_data=True,
    package_data={},
    install_requires=[
        'celery>=3.1.7',
        'django-celery>=3.1.1',
        'six>=1.9',
        # -*- Extra requirements: -*-
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
