""" mcli describe Endpoint """
from __future__ import annotations

import argparse
import logging

from mcli.cli.m_describe.describe_runs import describe_run

logger = logging.getLogger(__name__)


def describe_entrypoint(parser, **kwargs):
    del kwargs
    parser.print_help()


def describe_runs_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser = subparser.add_parser('run', help='List metadata about a specific run')
    run_parser.add_argument('run_name', type=str, help='Run name')
    run_parser.set_defaults(func=describe_run)


def add_describe_parser(subparser: argparse._SubParsersAction) -> argparse.ArgumentParser:
    describe_parser: argparse.ArgumentParser = subparser.add_parser(
        'describe',
        help='Get detailed information on an object',
    )
    return _configure_argparser(parser=describe_parser)


def _configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Objects',
                                       description='The table below shows the objects that you can describe',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=describe_entrypoint, parser=parser)
    describe_runs_argparser(subparser=subparsers)
    return parser
