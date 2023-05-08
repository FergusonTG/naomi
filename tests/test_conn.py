
import pytest

import naomi


@pytest.fixture
def new_connection():
    server = naomi.config["servers"]["GMX"]
    hostname = server["hostname"]
    user = server["username"]
    password = server["password"]

    return naomi.Connection(hostname=hostname, user=user, password=password)


def test_folder(new_connection):
    count = new_connection.select("INBOX")
    new_connection.close()

    assert count == 2

#
