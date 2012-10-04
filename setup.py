from setuptools import setup, find_packages
import audiofield
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name='django-audiofield',
    version=audiofield.__version__,
    description='Django application which allows audio file upload and conversion to mp3, wav and ogg format',
    long_description=README,
    url='http://github.com/Star2Billing/django-audiofield',
    author='Belaid Arezqui',
    author_email='areski@gmail.com',
    license='MIT License',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
