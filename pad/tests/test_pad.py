from math import ceil
from os import chmod
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import mock

import pytest

from perfect_pad import pad
from perfect_pad.settings import MAX_BLOCK_SIZE


class TestCreateBlockFile:
    def test_create_block_file_refuses_to_create_huge_block(self):
        """Ensure that `create_block_file` requires the `size`
        be less than MAX_BLOCK_SIZE bytes.
        """
        bad_size = MAX_BLOCK_SIZE + 1
        with TemporaryDirectory() as tmp_dir:
            chmod(tmp_dir, 0o700)
            with pytest.raises(ValueError) as excinfo:
                pad.create_block_file(Path(tmp_dir), bad_size)
            expected_description = (
                "Cannot create blocks larger than "
                f"{MAX_BLOCK_SIZE} bytes. Received request "
                f"for {bad_size} bytes."
            )
            assert excinfo.value.args[0] == expected_description

    @mock.patch("perfect_pad.pad.os")
    @mock.patch("perfect_pad.pad.open")
    @mock.patch("perfect_pad.pad.get_random_bytes")
    def test_create_block_file_creates_block_file_at_path(
        self, mock_get_random_bytes, mock_open, mock_os
    ):
        """Ensure that `create_block_file` creates a block file at `path`"""
        fake_path = f"/tmp/pads/foo.pad/0000000000000000"
        fake_path_obj = Path(fake_path)

        res = pad.create_block_file(fake_path_obj, 100)
        assert res is None

        mock_open_calls = mock_open.return_value.__enter__.return_value.mock_calls
        assert len(mock_open_calls) == 1
        mock_open_calls[0].args[0].as_posix() == fake_path

        mock_os.chmod.assert_called_once_with(fake_path_obj, 0o400)


class TestFetchBlocks:
    def test_fetch_and_destroy_block_returns_block_contents(self):
        with TemporaryDirectory() as tmp_dir:
            block_name = "abacadaba"
            contents = b"\xaf\xde\x0a\xe5"
            block_path = Path(tmp_dir) / block_name
            # create fake block
            with open(block_path, "wb") as file:
                file.write(contents)

            res = pad.fetch_and_destroy_block(Path(tmp_dir), block_name)
            assert res == contents
            assert not (Path(tmp_dir) / block_name).exists()

    @mock.patch("perfect_pad.pad.choice")
    @mock.patch("perfect_pad.pad.os.listdir")
    def test_get_random_block(self, mock_listdir, mock_choice):
        pad_path = Path("/tmp/pads/foo.pad")

        fake_block_names = ["foo", "bar", "biz"]
        mock_listdir.return_value = fake_block_names
        mock_choice.return_value = "bar"

        res = pad._get_random_block(pad_path)
        mock_listdir.assert_called_once_with(pad_path)
        mock_choice.assert_called_once_with(fake_block_names)
        assert res == "bar"

    @mock.patch("perfect_pad.pad.os.listdir")
    def test_get_random_block_when_pad_is_empty(self, mock_listdir):
        mock_listdir.return_value = []

        pad_path = Path("/tmp/pads/foo.pad")
        with pytest.raises(pad.EmptyOneTimePadException):
            pad._get_random_block(pad_path)

    @mock.patch("perfect_pad.pad.fetch_and_destroy_block")
    @mock.patch("perfect_pad.pad._get_random_block")
    def test_fetch_and_destroy_random_block(
        self, mock_get_random_block, mock_fetch_and_destroy_block
    ):
        pad_path = Path("/tmp/pads/foo.pad")
        mock_get_random_block.return_value = "foo"
        res = pad.fetch_and_destroy_random_block(pad_path)

        mock_get_random_block.assert_called_once_with(pad_path)
        mock_fetch_and_destroy_block.assert_called_once_with(pad_path, "foo")


class TestCreateOneTimePad:
    def test_create_one_time_pad_fails_if_path_parent_dir_does_not_exist(self):
        path_missing_parent_folder = Path("/not-a-real-folder/my.pad")
        with pytest.raises(ValueError) as excinfo:
            pad.create_one_time_pad(path_missing_parent_folder, 100, 50)
        expected_description = (
            "Cannot create one-time pad at "
            + "/not-a-real-folder/my.pad; "
            + "parent directory does not exist"
        )
        assert excinfo.value.args[0] == expected_description

    def test_create_one_time_pad_fails_when_block_size_smaller_than_pad_size(self):
        with TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(Path(tmp_dir).joinpath("foo.pad"), 100, 10000)
            expected_description = (
                f"Block size cannot be greater than pad size. "
                + "Received 100 for pad size, "
                + "10000 for block size."
            )
            assert excinfo.value.args[0] == expected_description

    @pytest.mark.parametrize("block_size", [-10, 0])
    def test_create_one_time_pad_fails_for_invalid_block_size(self, block_size):
        with TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(
                    Path(tmp_dir).joinpath("foo.pad"), 100, block_size
                )
            expected_description = (
                f"Block size must be greater than zero. Received {block_size}"
            )
            assert excinfo.value.args[0] == expected_description

    @pytest.mark.parametrize("pad_size", [-10, 0])
    def test_create_one_time_pad_fails_for_invalid_pad_size(self, pad_size):
        with TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(Path(tmp_dir).joinpath("foo.pad"), pad_size, 50)
            expected_description = (
                f"Pad size must be greater than zero. Received {pad_size}"
            )
            assert excinfo.value.args[0] == expected_description

    def test_create_one_time_pad_fails_if_path_already_exists(self):
        with TemporaryDirectory() as tmp_dir:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(Path(tmp_dir), 100, 50)
            expected_description = (
                "Cannot create one-time pad at "
                + f"{tmp_dir}; file or directory "
                + "already present at location"
            )
            assert excinfo.value.args[0] == expected_description

        with NamedTemporaryFile() as tmp_file:
            with pytest.raises(ValueError) as excinfo:
                pad.create_one_time_pad(Path(tmp_file.name), 100, 50)
            expected_description = (
                "Cannot create one-time pad at "
                + f"{tmp_file.name}; file or directory "
                + "already present at location"
            )
            assert excinfo.value.args[0] == expected_description

    @pytest.mark.parametrize(
        "pad_size,block_size", [(10000000, 500), (2000, 500), (500, 500)]
    )
    @mock.patch("perfect_pad.pad.create_block_file")
    def test_create_one_time_pad_creates_correct_number_of_blocks(
        self, mock_create_block_file, pad_size, block_size
    ):
        with TemporaryDirectory() as tmp_dir:
            chmod(tmp_dir, 0o700)
            new_dir = Path(tmp_dir).joinpath("foo.pad")
            pad.create_one_time_pad(new_dir, pad_size, block_size)
            calls = mock_create_block_file.mock_calls
            assert len(calls) == ceil(pad_size / block_size)
            for i, call in enumerate(calls):
                block_name = str(i).zfill(16)
                assert call.args == (new_dir.joinpath(block_name), block_size)
