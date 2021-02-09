#!/usr/bin/env python3.9

import argparse
from livewire import run_args, add_subcommands


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(
        title="subcommand", dest="subcommand", required=True
    )
    add_subcommands(subcommands)
    run_args(parser.parse_args())
