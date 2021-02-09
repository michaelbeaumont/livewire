import argparse
from .commands import up, down, init, destroy


livewire = {
    "down": down,
    "up": up,
    "init": init,
    "destroy": destroy,
}


def add_subcommands(parser: argparse._SubParsersAction):
    up = parser.add_parser("up")
    up.add_argument(
        "-t",
        "--template",
        metavar="FILE",
        help="the file where the wg-quick config template should be read from",
    )
    up.add_argument(
        "-o",
        "--out",
        required=True,
        metavar="FILE",
        help="the file where the wg-quick config should be written",
    )
    parser.add_parser("down")
    parser.add_parser("init")
    parser.add_parser("destroy")


def run_args(args: argparse.Namespace) -> None:
    livewire[args.subcommand](args)
