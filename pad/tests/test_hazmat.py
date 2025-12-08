from unittest import mock

from perfect_pad.hazmat.hazmat import get_random_bytes


@mock.patch("perfect_pad.hazmat.hazmat.urandom")
def test_get_random_bytes(mock_urandom):
    mock_result = b"\x13\xce\xfa\x95"
    mock_urandom.return_value = mock_result

    res = get_random_bytes(5)

    mock_urandom.assert_called_once_with(5)
    assert res == mock_result
