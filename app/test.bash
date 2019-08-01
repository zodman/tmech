set -e 
pipenv run coverage run  manage.py  test   -n  # appointment.tests.AppointmentViewsTest.test_update_view
pipenv run coverage report -m 
pipenv run coverage html
