from setuptools import setup, find_packages

setup(
    name="tmech",
    version="1.0",
    packages=find_packages(where="app"),
    package_dir={
        '': 'app',
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "manage.py = app.conf.config.django_manage",
        ]
    })
