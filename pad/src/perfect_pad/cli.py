import argparse
from pathlib import Path

from .pad import create_one_time_pad


def main():
    parser = argparse.ArgumentParser(prog="pad", description="One-time pad helper")

    subparsers = parser.add_subparsers(dest="command")

    parser_create = subparsers.add_parser("create", help="Create a one-time pad")
    parser_create.add_argument(
        "path", type=str, help="Path to pad (e.g. /home/dave/perfect.pad)"
    )
    parser_create.add_argument("size", type=int, help="Size of pad")
    parser_create.add_argument("block_size", type=int, help="Size of each block")
    parser_create.set_defaults(func=create_one_time_pad)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(Path(args.path), args.size, args.block_size)
