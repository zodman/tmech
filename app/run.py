# Define your GoodConf in `myproject/conf.py`
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
from app.conf import config

if __name__ == '__main__':
    config.django_manage()
