"""
Parsing is already used and tested indirectly by `test_main_handler`.
This module is for testing long-tail events.
"""
import pytest

import parsing
import errors


def test_raise_on_no_app_specified():
    """Make sure an `errors.InvalidInbound` is raised when no app is specified."""
    inbound = {
        "phone_number": "00000000000",
        "body": "noapphere"
    }

    with pytest.raises(errors.InvalidInbound):
        app = parsing.requested_app(parsing.InboundMessage(**inbound))
