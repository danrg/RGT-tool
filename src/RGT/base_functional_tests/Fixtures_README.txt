This file explains how the fixtures, in every test package, are created.

In order to create a fixture so it can contain information about a registered user, so it can be used
for example for the login operation, we do the following:

python manage.py dumpdata auth.User --indent=2 > grid_functional_tests/fixtures/admin_user.json