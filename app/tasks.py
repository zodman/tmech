from invoke import task as task_local
from invoke import run as local

@task_local
def gen_conf(c):
    c.run('pipenv run python  -c "import app.conf; print(app.conf.config.generate_yaml())"')

@task_local
def make(c):
    c.run("yarn run prod")
    #c.run("pipenv run python  manage.py collectstatic --noinput")
    with c.cd("../"):
        cmd = [
            "shiv",
            "-o", "tmech.pyz",
            "-e", "django.core.management:execute_from_command_line",
            "--site-packages=$(pipenv --venv)/lib/python3.6/site-packages/",
            "--python='/usr/bin/env python3.6'",
            "--no-deps", "."
        ]
        c.run(" ".join(cmd))
    c.run("scp ../tmech.pyz waifu.ca:apps/tmech/")

@task_local
def test(c):
    c.run("coverage run manage.py test -n --failfast  ")
    c.run("coverage report -m")
    c.run("coverage html")
