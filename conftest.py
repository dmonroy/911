from emergency.db import create_database, drop_database


def pytest_configure():
    drop_database()
    create_database()
