"""Interpret and act on rules."""

import re  # NOQA


def test(message, rule):
    """Test whether a message matches a rule."""
    if not message[rule["header"]]:
        return False

    if rule["compare"] == "matches":
        return message[rule["header"]] == rule["target"]

    if rule["compare"] == "startswith":
        return message[rule["header"]].startswith(rule["target"])

    if rule["compare"] == "endswith":
        return message[rule["header"]].endswith(rule["target"])

    if rule["compare"] == "regex":
        pattern = re.compile(rule["target"])
        return pattern.fullmatch(message[rule["header"]])

    raise ValueError(f"Not a valid compare rule: {rule['compare']}")
