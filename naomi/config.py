import pathlib
from os.path import expandvars

import tomli
import secretstorage


def _check_secret_storage():
    try:
        conn = secretstorage.dbus_init()
        return secretstorage.check_service_availability(conn)

    except secretstorage.exceptions.SecretServiceNotAvailableException:
        return False


def _get_config_file():
    paths = [
        "config.toml",
        "$XDG_CONFIG_HOME/naomi/config.toml",
        "$XDG_CONFIG_HOME/naomi.conf",
        "$HOME/.config/naomi/config.toml",
        "$HOME/.config/naomi.conf",
        "$HOME/.naomi.conf",
        ]
    for path in paths:
        real_path = expandvars(path)
        if pathlib.Path(real_path).is_file():
            # print(f"Config found in index {indx}, {path}")
            return real_path
    raise RuntimeError("Cannot find configuration file.")


def _get_config_object(config_file_path):
    """Return the config file as a python dict."""
    configfile = pathlib.Path(config_file_path)
    return tomli.loads(configfile.read_text())


def _getsscollection():
    """Open the secret storage collection."""
    conn = secretstorage.dbus_init()
    coll = secretstorage.get_default_collection(conn)
    if coll.is_locked():
        coll.unlock()
        if coll.is_locked():
            raise RuntimeError("Can't unlock secret storage.")
    return coll


def _getserverdetails(ss_collection, item_path):
    """Return username and password from secret storage."""
    criterion = {"Path": item_path}
    items = list(ss_collection.search_items(criterion))
    if not items:
        raise ValueError(f"Keepass item {item_path} not found.")
    if len(items) > 1:
        raise ValueError("{len(items}} ambiguous Keepass items found.")

    username = items[0].get_attributes()["UserName"]
    password = items[0].get_secret()
    if isinstance(password, bytes):
        password = password.decode(encoding='ascii')

    return username, password


def _get_config():
    """Assemble config data from config file and secret storage."""

    if not _check_secret_storage():
        raise RuntimeError("Cannot access secret service.")

    config_file_path = _get_config_file()
    config = _get_config_object(config_file_path)

    ss_collection = _getsscollection()

    for server in config["servers"]:

        try:
            username, password = _getserverdetails(
                    ss_collection,
                    config['servers'][server]["path"]
                    )
        except ValueError:
            continue

        config['servers'][server]["username"] = username
        config['servers'][server]["password"] = password

    ss_collection.lock()
    return config


if __name__ == "__main__":
    config = _get_config()
