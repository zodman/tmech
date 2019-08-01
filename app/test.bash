set -e 
coverage run  manage.py  test   -n  # appointment.tests.AppointmentViewsTest.test_update_view
coverage report -m 
coverage html
