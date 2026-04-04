"""This module contains common code used by multiple subcommands in the `pytater` CLI."""

import argparse


def common_arguments(subparse: argparse.ArgumentParser) -> None:
    """Add common arguments to the given subparser.

    These arguments are used by multiple subcommands in the `pytater` CLI.

    Args:
        subparse: The argument parser to which the common arguments should be added.
    """
    argparse_verbosity(subparse)
    argparse_cookie(subparse)


def argparse_verbosity(subparse: argparse.ArgumentParser) -> None:
    """Add the `--verbose` and `--debug` arguments to the given subparser.

    These arguments are used to set the logging verbosity level for the subcommand.

    Args:
        subparse: The argument parser to which the `--verbose` and `--debug` arguments should be added.
    """
    group = subparse.add_mutually_exclusive_group()
    group.add_argument(
        "--verbose",
        dest="verbosity",
        action="store_const",
        const="verbose",
        default="default",
        help="Enable verbose logging output for this command.",
    )
    group.add_argument(
        "--debug",
        dest="verbosity",
        action="store_const",
        const="debug",
        default="default",
        help="Enable debug logging output for this command.",
    )


def argparse_cookie(subparse: argparse.ArgumentParser) -> None:
    """Add the `--cookie` argument to the given subparser.

    This argument is used to specify the location of a temporary cookie file that is monitored to begin/end dictation.

    Args:
        subparse: The argument parser to which the `--cookie` argument should be added.
    """
    subparse.add_argument(
        "--cookie",
        dest="path_to_cookie",
        default="",
        type=str,
        metavar="FILE_PATH",
        help="Location for writing a temporary cookie (this file is monitored to begin/end dictation).",
        required=False,
    )
