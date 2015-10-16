import os
import sys

from attrdict import AttrDict

DEFAULT_DATABASE = 'psycopg2+postgresql://postgres@localhost:5432/emergency'

if sys.argv[0].endswith('/py.test'):
    DATABASE_URL = '{}_test_{}{}{}'.format(
        DEFAULT_DATABASE,
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )
else:  # pragma: no cover
    DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DATABASE)


BASE_SETTINGS = dict(
    db_url=DATABASE_URL,
    debug=True
)


def get_settings():
    return AttrDict(BASE_SETTINGS)
