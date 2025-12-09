from pathlib import Path
from unittest.mock import patch
import sys

from perfect_pad import cli
from perfect_pad.settings import DEFAULT_BLOCK_SIZE, DEFAULT_PAD_SIZE


class TestCreate:
    """Verify foo"""

    @patch("perfect_pad.cli.create_one_time_pad")
    def test_create(self, mock_create_one_time_pad):
        fake_path = "/home/dave/perfect.pad"
        with patch.object(sys, "argv", ["pad", "create", fake_path]):
            cli.main()
        calls = mock_create_one_time_pad.mock_calls
        assert len(calls) == 1
        assert calls[0].args[0].as_posix() == fake_path
        assert calls[0].args[1:] == (DEFAULT_PAD_SIZE, DEFAULT_BLOCK_SIZE)
