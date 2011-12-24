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

Add ``audiofield`` into INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...
        'audiofield',
        ...)

Add the following code to your middleware::
    
    MIDDLEWARE_CLASSES = (
        ...
        'audiofield.middleware.threadlocals.ThreadLocals',
    )

If you are going to add customer audio form on your frontend, please add following::

    # Frontend widget values
    CHANNEL_TYPE_VALUE = 0  # 0-Keep original, 1-Mono, 2-Stereo

    FREQ_TYPE_VALUE = 8000  # 0-Keep original, 8000-8000Hz, 16000-16000Hz, 22050-22050Hz,
                         # 44100-44100Hz, 48000-48000Hz, 96000-96000Hz

    CONVERT_TYPE_VALUE = 0 # 0-Keep original, 1-Convert to MP3, 2-Convert to WAV, 3-Convert to OGG

Run following commands::

    python manage.py syncdb

    python manage.py collectstatic

