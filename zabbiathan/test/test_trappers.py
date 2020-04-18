# Tests for trappers.py
import json
import pytest
import socket

import unittest.mock as mock
import zabbiathan.trappers as t


def test_protocol_is_correct():
    assert t.ZBX_PROTOCOL == b"ZBXD"


class TestTrapper:
    def test_trapper_init_no_params_inits_expected(self):
        trap = t.Trapper()

        assert trap.host == socket.gethostname()
        assert trap.key is ""
        assert trap.value is ""
        assert trap.clock is None

    def test_trapper_init_everything_declared_inits_expected(self):
        trap = t.Trapper(host="host.test.com", key="metric.fake", value="off the charts!", clock=1234567890)

        assert trap.host is "host.test.com"
        assert trap.key is "metric.fake"
        assert trap.value is "off the charts!"
        assert trap.clock == 1234567890

    @mock.patch('time.time', return_value=1234567890.0)
    def test_trapper_init_clock_true_sets_now(self, patch_time):
        trap = t.Trapper(clock=True)

        assert trap.clock == 1234567890
        patch_time.assert_called_once()

    def test_trapper_init_clock_false_doesnt_set(self):
        trap = t.Trapper(clock=False)

        assert trap.clock is None

    @pytest.mark.parametrize('clock_', (1234567890, 1234567890.3), ids=("int", "float"))
    def test_trapper_init_clock_numeric_types_inits_expected(self, clock_):
        trap = t.Trapper(clock=clock_)

        assert trap.clock == 1234567890

    @pytest.mark.parametrize('bad_type', ("string", list(), dict()), ids=("str", "list", "dict"))
    def test_trapper_init_clock_passed_bad_types_raises_expected(self, bad_type):
        with pytest.raises(ValueError) as e:
            t.Trapper(clock=bad_type)
            assert "Unable to determine clock value" in e.value

    def test_repr_returns_expected(self):
        expected = "Trapper(host='fake.com', key='mock.metric', value=666, clock=1234567890)"

        trap = t.Trapper(host="fake.com", key="mock.metric", value=666, clock=1234567890)

        assert repr(trap) == expected

    def test_json_without_clock_returns_expected(self):
        expected_dict = {'host': 'fake.com',
                         'key': 'mock.metric',
                         'value': 666}

        trap = t.Trapper(host="fake.com", key="mock.metric", value=666)
        reloaded_dict = json.loads(trap.json())

        assert reloaded_dict == expected_dict

    def test_json_with_clock_false_returns_expected(self):
        expected_dict = {'host': 'fake.com',
                         'key': 'mock.metric',
                         'value': 666}

        trap = t.Trapper(host="fake.com", key="mock.metric", value=666, clock=False)
        reloaded_dict = json.loads(trap.json())

        assert reloaded_dict == expected_dict

    @mock.patch('time.time', mock.MagicMock(return_value=8888888888.0))
    def test_json_with_clock_true_returns_expected(self):
        expected_dict = {'host': 'fake.com',
                         'key': 'mock.metric',
                         'value': 666,
                         'clock': 8888888888}

        trap = t.Trapper(host="fake.com", key="mock.metric", value=666, clock=True)
        reloaded_dict = json.loads(trap.json())

        assert reloaded_dict == expected_dict

    def test_json_with_clock_returns_expected(self):
        expected_dict = {'host': 'fake.com',
                         'key': 'mock.metric',
                         'value': 666,
                         'clock': 1234567890}

        trap = t.Trapper(host="fake.com", key="mock.metric", value=666, clock=1234567890)
        reloaded_dict = json.loads(trap.json())

        assert reloaded_dict == expected_dict
