import argparse
import json
import os

from .config import (
    InstanceConfig,
    get_config,
    data_dir,
)
from .terraform import run_terraform, run_output, run_init
from .utils import cd, open_or_stdout
from .wireguard import render_config, make_client_peer, make_peer


def terraform_action_args(init_config: dict, config: InstanceConfig):
    return {
        "project_id": init_config["project_id"]["value"],
        "subnetwork": init_config["subnetwork"]["value"],
        "source_ranges": config.source_ranges,
        "peers": [
            make_client_peer(config.client),
            *[make_peer(p) for p in config.other_peers],
        ],
    }


def init(args: argparse.Namespace):
    config = get_config().init
    init_dir = os.path.join(data_dir, "init")
    if not os.path.isdir(init_dir):
        os.makedirs(init_dir)
        with cd(init_dir):
            run_init("gcp/init")
    init_dict = {"region": config.region, "billing_account": config.billing_account}
    with cd(init_dir):
        run_terraform("apply", init_dict)


def destroy_init():
    config = get_config().init
    init_dir = os.path.join(data_dir, "init")
    with cd(init_dir):
        # terraform is weird https://github.com/hashicorp/terraform/issues/18994
        run_terraform(
            "destroy",
            {"region": config.region, "billing_account": config.billing_account},
        )


def instance_action(subcommand: str, config: InstanceConfig):
    init_dir = os.path.join(data_dir, "init")
    with cd(init_dir):
        init_config = json.loads(run_output())
    instance_dir = os.path.join(data_dir, "instance")
    if not os.path.isdir(instance_dir):
        os.makedirs(instance_dir)
        with cd(instance_dir):
            run_init("gcp/instance")
    with cd(instance_dir):
        tfargs = terraform_action_args(init_config, config)
        run_terraform(subcommand, tfargs)


def up(args: argparse.Namespace):
    config = get_config().instance
    instance_action("apply", config)
    instance_dir = os.path.join(data_dir, "instance")
    with cd(instance_dir):
        output = run_output()
    wg_conf = render_config(args.template, json.loads(output), config.client)
    with open_or_stdout(args.out) as f:
        f.write(wg_conf)


def down(_args: argparse.Namespace):
    config = get_config().instance
    instance_action("destroy", config)


def destroy(_args: argparse.Namespace):
    down(_args)
    destroy_init()
