from dataclasses import dataclass
from subprocess import run
from typing import Optional

from .config import get_template, ClientConfig


@dataclass
class Peer:
    ip: str
    port: str
    public_key: str


def render_config(
    template_loc: Optional[str], output: dict, client: ClientConfig
) -> str:
    tmpl_vars = {
        "interface_extra": output["interface_extra"]["value"],
        "peer": Peer(
            ip=output["ip"]["value"],
            port=output["port"]["value"],
            public_key=output["public_key"]["value"],
        ),
    }
    if client.private_key:
        tmpl_vars["private_key"] = client.private_key
    return get_template(template_loc).format_map(tmpl_vars)


def make_client_peer(client: ClientConfig) -> str:
    public_key = client.public_key
    if client.private_key is not None:
        public_key = run(
            ["wg", "pubkey"],
            input=client.private_key,
            check=True,
            encoding="UTF-8",
            capture_output=True,
        ).stdout.strip()
    if public_key is None:
        raise Exception("couldn't generate public_key or find in config")
    return make_peer({"PublicKey": public_key, "AllowedIPs": client.allowed_ips})


def make_peer(peer: dict) -> str:
    return f"""PublicKey = {peer["PublicKey"]}
AllowedIPs = {peer["AllowedIPs"]}
        """
