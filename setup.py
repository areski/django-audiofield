from setuptools import setup, find_packages
import audiofield
import os
import re
import sys


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'(\s*git)|(\s*hg)', line):
            pass
        else:
            requirements.append(line)
    return requirements


def parse_dependency_links(file_name, install_flag=False):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-e\s+', line):
            dependency_links.append(re.sub(r'\s*-e\s+', '', line))
        if re.match(r'(\s*git)|(\s*hg)', line):
            if install_flag == True:
                line_arr = line.split('/')
                line_arr_length = len(line.split('/'))
                pck_name = line_arr[line_arr_length - 1].split('.git')
                if len(pck_name) == 2:
                    os.system('pip install -f %s %s' % (pck_name[0], line))
                if len(pck_name) == 1:
                    os.system('pip install -f %s %s' % (pck_name, line))
    return dependency_links


install_flag = False
if sys.argv[1] == "install":
    install_flag = True


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
    install_requires=parse_requirements('audiofield/requirements.txt'),
    dependency_links=parse_dependency_links('audiofield/requirements.txt', install_flag),
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
