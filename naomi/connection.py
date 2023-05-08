"""IMAP4 Connection object."""

import imaplib


class Connection():
    """Encapsulate function of a connection to an IMAP server."""

    def __init__(self, hostname, user, password):
        print(f"init: logging in to {hostname}")
        self.imap = imaplib.IMAP4_SSL(hostname)

        self._status = "PRE-AUTH"

        print(f"init: authenticating as {user}")
        self.imap.login(user, password)

        print("Success")
        self._status = "AUTH"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def close(self):
        if self._status == "SELECTED":
            self.imap.close()

        self.imap.logout()

        self._status = "LOGGEDOUT"

    def select(self, mailboxname):
        """Select a given mailbox and return number of messages."""
        status, ret = self.imap.select(mailboxname)
        if status == 'OK':
            self._status = "SELECTED"
            return int(ret[0])

        raise RuntimeError(str(ret))

    def connected(self):
        return self._status in ["AUTH", "SELECTED"]
