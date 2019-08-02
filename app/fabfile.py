from fabric import task
from invoke import run as local

@task
def test(c):
    local("coverage run manage.py test -n")
    local("coverage report -m")
    local("coverage html")
