from .server import start_server
from .perf_script import run_perf_script
from .args import Args, parse_args
from .interfaces import get_local_ips

from pathlib import Path
from time import sleep
from typing import List, Tuple, Optional

import urllib.parse
import requests


def check_file_exists(path: Path):
    if not path.exists():
        print(f"Cannot find {path}")
        exit(1)


def make_hyperlink(label: str, url: str):
    escape_mask = '\033]8;;{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(url, label)


def get_my_ip() -> str:
    return requests.get('https://api.ipify.org').text


def display_url_via_ip(ip: str, port: int, prefix: str, name: str, args: Args):
    data_url = f"http://{ip}:{port}/"
    url = f"https://{args.profiler_url}/from-url/{urllib.parse.quote(data_url, safe='')}"
    if args.hyperlinks_enabled:
        link = make_hyperlink(name, url)
        print(f"{prefix} {link}")
    else:
        print(f"{prefix} {name}: {url}")


def find_vpn_ip(ips: List[Tuple[str, str]]) -> Optional[str]:
    for ip in ips:
        if ip[0].startswith("tun"):
            return ip[1]
    return None


def remove_ip_from_list(ips: List[Tuple[str, str]], to_remove: str):
    index = next((i for i in range(len(ips)) if ips[i][1] == to_remove), None)
    if index is None:
        return
    ips.pop(index)


def try_display_public(ips: List[Tuple[str, str]], port: int, args: Args):
    public_ip = get_my_ip()
    if public_ip is not None:
        remove_ip_from_list(ips, public_ip)
        display_url_via_ip(public_ip, port, "🚀", f"via public ip ({public_ip})", args)


def try_display_vpn(ips: List[Tuple[str, str]], port: int, args: Args):
    vpn_ip = find_vpn_ip(ips)
    if vpn_ip is not None:
        remove_ip_from_list(ips, vpn_ip)
        display_url_via_ip(vpn_ip, port, "🚀", f"via VPN ({vpn_ip})", args)


def display_possible_urls(port: int, args: Args):
    ips = get_local_ips()
    try_display_public(ips, port, args)
    try_display_vpn(ips, port, args)

    if len(ips) > 0:
        print("Other variants:")
        for ip in ips:
            display_url_via_ip(ip[1], port, "➤", f"via {ip[1]}", args)


def display_hyperlinks_warning():
    print("If you don't see links, add '--no-hyperlinks' flag")


def main():
    args = parse_args()

    check_file_exists(args.path)

    perf_script_output = run_perf_script(args.path)
    http_server = start_server(Path(perf_script_output.name), args.address, args.port)


    if args.hyperlinks_enabled:
        display_hyperlinks_warning()
    print()
    display_possible_urls(http_server.server_address[1], args)

    while True:
        sleep(1)


if __name__ == "__main__":
    main()
