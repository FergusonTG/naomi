
import pytest
from email.message import EmailMessage

from naomi import rules


# @pytest.fixture
def rule_object():
    return {
          "header": "List-ID",
          "compare": "matches",
          "target": "lst-looking",
          "action": "move",
          "destination": "pentax_list",
          }


# @pytest.fixture
def message_object():
    mess = EmailMessage()
    for label, value in (
            ("from", "tim@cardiff"),
            ("to", "tim@edinburgh"),
            ("subject", "Looking for you."),
            ("list-id", "lst-looking"),
            ):
        mess.add_header(label, value)

    mess.set_content("This is a valuable message")
    return mess


def test_find_package():
    assert rules is not None


def test_matches():
    rule_obj = rule_object()
    message_obj = message_object()
    assert rules.test(message_obj, rule_obj)

    del message_obj["list-id"]
    assert not rules.test(message_obj, rule_obj)


def test_startswith():
    rule_obj = rule_object()
    rule_obj["compare"] = "startswith"
    rule_obj["target"] = "lst-"
    message_obj = message_object()
    assert rules.test(message_obj, rule_obj)

    del message_obj["list-id"]
    assert not rules.test(message_obj, rule_obj)


def test_endswith():
    rule_obj = rule_object()
    rule_obj["compare"] = "endswith"
    rule_obj["target"] = "looking"
    message_obj = message_object()
    assert rules.test(message_obj, rule_obj)

    del message_obj["list-id"]
    assert not rules.test(message_obj, rule_obj)


def test_regex():
    rule_obj = rule_object()
    rule_obj["compare"] = "regex"
    rule_obj["target"] = r".*-looking"
    message_obj = message_object()
    assert rules.test(message_obj, rule_obj)

    del message_obj["list-id"]
    assert not rules.test(message_obj, rule_obj)
