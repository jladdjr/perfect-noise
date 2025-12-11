from pathlib import Path
import sys

from perfect_pad import cli

from unittest.mock import patch

class TestCreate:
    """Verify foo"""

    @patch("perfect_pad.cli.Path.home")
    def test_create(self, mock_path, capsys):
        mock_path.return_value = "/home/dave"
        with patch.object(sys, "argv", ["pad", "create"]):
            cli.main()
        captured = capsys.readouterr()
        expected_out = """Creating 10M secure pad using 1K blocks
Done!

Pad is located at:
/home/dave/perfect.pad"""
        assert expected_out in captured
