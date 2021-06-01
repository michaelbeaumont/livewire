# Livewire

Livewire makes it easy to set up an ephemeral VPN using wireguard
running in GCP. It uses
[michaelbeaumont/wireform](https://github.com/michaelbeaumont/wireform)
to setup a GCP VM with wireguard and generate the private key entirely in the
VM, exporting only the public key.

It requires `wg` and `terraform`.
Python dependencies are managed using `poetry`.

```
$ poetry install
$ poetry run ./main.py init
$ poetry run ./main.py up -o wg0.conf -t wg0.tmpl
```

## Config

Configure livewire with a `config.json` file in `${XDG_CONFIG_HOME}/livewire`
and replace `<...>`s:

```
{
  "init": {
    "region": "us-east1",
    "billing_account": "<BILLING_ACCOUNT_ID>"
  },
  "instance": {
    "source_ranges": [
      "<IP ADDRESS RANGES YOU'LL CONNECT FROM>"
    ],
    "client": {
      "public_key": "<WG_PUBLIC_KEY>",
      // or: "private_key": "<WG_PRIVATE_KEY>",
      "allowed_ips": "<CIDR CONTAINING Interface.Address FROM YOUR WG CONFIG>"
    },
    "other_peers": []
  }
}
```

along with a template `conf.tmpl` for _your client_ `wg-quick` config
(`{...}`s are replaced by `livewire`):

```
[Interface]
Address = <IP ADDRESS OF INTERFACE>
{interface_extra} # important for MTU issues with GCP
PrivateKey = {private_key} # if you put it in the livewire config
DNS = 1.1.1.1

PreUp = ./wg-vpn PreUp
PostUp = ./wg-vpn PostUp
PreDown = ./wg-vpn PreDown
PostDown = ./wg-vpn PostDown

[Peer]
PublicKey = {peer.public_key} # generated on the peer in GCP
Endpoint = {peer.ip}:{peer.port} # IP of peer in GCP
AllowedIPs = 0.0.0.0/0 # route all traffic through this peer
```
