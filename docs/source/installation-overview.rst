.. _installation-overview:

=====================
Installation overview
=====================

.. _install-requirements:

Install requirements
====================

A requirements file stores a list of dependencies to be installed for your project/application.

To get started with Django-audiofield you must have the following installed:

- python >= 2.4 (programming language)
- Apache / http server with WSGI modules
- Django Framework >= 1.3 (Python based Web framework)
- Django-uuidfield


.. _install_dependencies:

Install dependencies
====================

Install dependencies on Debian::
    
    apt-get -y install libsox-fmt-mp3 libsox-fmt-all mpg321 ffmpeg


Install dependencies on Redhat/CentOS::
    
    yum -y install python-setuptools libsox-fmt-mp3 libsox-fmt-all mpg321 ffmpeg


.. _install_requirements:

Install requirements
====================

Use PIP to install the dependencies listed in the requirments file,::

    $ pip install -r requirements.txt


.. _configuration:

Configuration
=============

- Add ``admin_tools_stats`` & ``chart_tools`` into INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...
        'audiofield',
        ...)

- Add the following code to your middleware::
    
    MIDDLEWARE_CLASSES = (
        ...
        'audiofield.middleware.threadlocals.ThreadLocals',
    )

- Run ``manage.py syncdb`` and ``manage.py collectstatic``


