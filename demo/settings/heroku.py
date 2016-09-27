from __future__ import absolute_import, unicode_literals
import dj_database_url
from .base import *

DEBUG = False
DATABASES['default'] = dj_database_url.config()
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost']

try:
    from .local import *
except ImportError:
    pass
