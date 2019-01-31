"""This module provides helpers functions for daemons."""

import argparse


def parse_args():
    """Provides parser for daemon`s arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'frequency',
        type=int,
        help='amount of seconds between two sequences of daemon execute method.'
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-M',
        '--minutes',
        action='store_true',
        help='flag that determines the frequency parameter as number of minutes.'
    )
    group.add_argument(
        '-H',
        '--hours',
        action='store_true',
        help='flag that determines the frequency parameter as number of hours.'
    )

    args = parser.parse_args()
    arg_frequency = args.frequency
    if args.minutes:
        arg_frequency = args.frequency * 60
    elif args.hours:
        arg_frequency = args.frequency * 60 * 60

    return arg_frequency
