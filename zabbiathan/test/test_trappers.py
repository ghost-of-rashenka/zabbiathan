# Tests for trappers.py
import zabbiathan.trappers


def test_protocol_is_correct():
    assert zabbiathan.trappers.ZBX_PROTOCOL == b"ZBXD"
