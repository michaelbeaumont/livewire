import os
from typing import List, Optional
from pydantic import BaseModel, Field

from .utils import open_or_stdin


class InitConfig(BaseModel):
    region: str
    billing_account: str


class ClientConfig(BaseModel):
    private_key: Optional[str]
    public_key: Optional[str]
    allowed_ips: Optional[str]


class InstanceConfig(BaseModel):
    source_ranges: List[str] = Field(default_factory=list)
    client: ClientConfig
    other_peers: List[dict] = Field(default_factory=list)


class Config(BaseModel):
    init: InitConfig
    instance: InstanceConfig


xdg_config = (
    os.environ["XDG_CONFIG_HOME"]
    if "XDG_CONFIG_HOME" in os.environ
    else os.path.expanduser("~/.config")
)
config_dir = os.path.join(xdg_config, "livewire")

xdg_data = (
    os.environ["XDG_DATA_HOME"]
    if "XDG_DATA_HOME" in os.environ
    else os.path.expanduser("~/.local/share")
)
data_dir = os.path.join(xdg_data, "livewire")


def get_template(loc: Optional[str]) -> str:
    with open_or_stdin(loc if loc else os.path.join(config_dir, "conf.tmpl")) as f:
        return f.read()


def get_config() -> Config:
    with open(os.path.join(config_dir, "config.json")) as f:
        return Config.parse_raw(f.read())
