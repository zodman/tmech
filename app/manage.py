#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from app.conf import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    #main()
    config.django_manage()
