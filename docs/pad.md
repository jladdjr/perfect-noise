# Perfect Pad

[![Test Pad](https://github.com/jladdjr/perfect-noise/actions/workflows/test-pad.yaml/badge.svg)](https://github.com/jladdjr/perfect-noise/actions/workflows/test-pad.yaml)

## Overview

Perfect Pads are [one-time pads](https://en.wikipedia.org/wiki/One-time_pad)
that follow a simple, practical structure:

```
perfect.pad/
  a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a  <-- first block file
  9d0f3db671f9fb22104b984763616732d383154a7a0dcdbb9ec17ab647b64961  <-- second block file
  f865e96899b055dacef1e0132a0ec8d35adbb425812b7d3f1950c1e1c27f7ed2      ..
  f57d1b1448daae7a0a22d055c918c24e1c2bc37d45c71bd68dd90b0c3189080b
  18ff0d8e5ff6f788f77a6fdf0238c15b2ef3edcfd6760e198cd068757a922703      block names are the
  7170aa75bd668d8606f242bfd30c1c772a3e0ee2f2824ce5fb2c5305e2837dd3      cryptographic hash
  2755ad587fdb5e242deefef0b32d9adb5136fdda323898d95685ae3fc4d8f1a0      of the block's contents
  ...
```

Where each file in the *.pad directory contains a series of
[cryptographically secure random digits](https://cryptography.io/en/latest/random-numbers/#random-number-generation). These files are referred to as _blocks_.

## Usage

To work with Perfect Pads directly, use the `pad` CLI.

### Creating a pad

To create a pad, use the `create` sub-command. For example:

```bash
$ pad create
Creating 10M secure pad using 1K blocks
Done!

Pad is located at:
/home/dave/perfect.pad
```

By default, `pad create` builds a ten megabyte pad containing 10,000 one-kilobyte blocks.
The default location of a pad is `$HOME/perfect.pad`.

_Options_

`pad create` supports the following options:

- `--pad` / `-p` - custom location for the pad
- `--size` / `-s` - size of the entire pad
- `--block-size` / `-b` - size of each block

.. where sizes are specified using the following units.

- `b` - bytes
- `k` - kilobytes
- `M` - megabytes

For example:

```bash
$ pad create --pad /home/dave/alternate.pad --size 500k --block-size 500b
Creating 500k secure pad using 500b blocks
Done!

Pad is located at:
/home/dave/alternate.pad
```

### Inspecting pads

TODO: command that lists total size of pad, number of blocks, size of each block

### Listing blocks

To list the blocks in a pad, use the `block list` sub-command:

```
$ pad block list
/home/dave/perfect.pad contains the following blocks:

a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
9d0f3db671f9fb22104b984763616732d383154a7a0dcdbb9ec17ab647b64961
f865e96899b055dacef1e0132a0ec8d35adbb425812b7d3f1950c1e1c27f7ed2
f57d1b1448daae7a0a22d055c918c24e1c2bc37d45c71bd68dd90b0c3189080b
18ff0d8e5ff6f788f77a6fdf0238c15b2ef3edcfd6760e198cd068757a922703
7170aa75bd668d8606f242bfd30c1c772a3e0ee2f2824ce5fb2c5305e2837dd3
2755ad587fdb5e242deefef0b32d9adb5136fdda323898d95685ae3fc4d8f1a0
...
```

_Options_

`pad block list` supports the following options:

- `--pad` / `-p` - custom location for the pad

### Fetching blocks

To fetch the data in a block, use the `block fetch-destory` sub-command:

```
$ pad block fetch-destroy 901b40

1dad81524c2adf6cf47ce55cf9187881a20f6761c1171564532030be9895b7663ae601b0dbf41...
```

As long as the block name specified matches the initial characters of exactly one block, the command will print the block's contents in hexadecimal format and destroy the block as a safeguard against reuse. (As a reminder, the security of one-time pads requires that the pad's contents are _never_ reused).

If the block name is omitted, the very first block in the pad is retrieved and destroyed. Block names are sorted alphanumerically.

# FAQ

## Where does a block's name come from?

The block name is a crypographic hash of the contents of the block itself.

## Why break the pad into a series of blocks? Why not have one file with random digits?

Breaking the file up into discrete blocks supports consuming the pad incrementally.

## The pad _only_ contains raw random digits. Why not embed metadata, too?

The pad doesn't contain any unencrypted information by design.
