.. _testing:

Test Case Descriptions
======================

----------------
How to run tests
----------------

**1. Run full test suite**::

    $ python manage.py test --verbosity=2

**2. Run AudiofileTestCase**::

    $ python manage.py test audiofield.AudiofieldAdminInterfaceTestCase --verbosity=2


.. _audiofield-admin-testcases:

:class:`AudiofieldAdminInterfaceTestCase`
-----------------------------------------

Different test-cases of the audiofield

    **def test_admin_index()** : Test Function to check Admin index page

    **def test_admin_audiofield()** : Test Function to check Audiofield Admin pages


