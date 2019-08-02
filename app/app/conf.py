import os
import base64
from goodconf import GoodConf, Value

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(GoodConf):
    "Configuration for My App"
    DEBUG = Value(default=False, help="Toggle debugging.")

    DATABASE_CONF = Value(default={
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        cast_as=dict,
        help="Database connection.")
    SECRET_KEY = Value(
        initial=lambda: base64.b64encode(os.urandom(60)).decode(),
        help="Used for cryptographic signing. "
        "https://docs.djangoproject.com/en/2.0/ref/settings/#secret-key")
    STATIC_ROOT = Value(
        default=os.path.join(BASE_DIR, "static"),
        help="static directory"
    )


config = Config(
   default_files=["tmech_conf.yaml"]
)
