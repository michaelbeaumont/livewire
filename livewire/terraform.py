import json
from subprocess import run, DEVNULL


def make_terraform_env(tfvars: dict) -> dict:
    env = {}
    for k, v in tfvars.items():
        v = json.dumps(v)
        if isinstance(v, str):
            v = v.strip('"')
        env[f"TF_VAR_{k}"] = v
    return env


def run_terraform(subcommand: str, env: dict):
    run(
        ["terraform", subcommand, "-auto-approve"],
        env=make_terraform_env(env),
        check=True,
        stdout=DEVNULL,
    )


def run_output() -> bytes:
    return run(["terraform", "output", "-json"], check=True, capture_output=True).stdout


WIREFORM = "https://github.com:michaelbeaumont/wireform"


def run_init(submodule: str):
    run(
        [
            "terraform",
            "init",
            "-from-module",
            f"{WIREFORM}//{submodule}",
        ],
        check=True,
    )
