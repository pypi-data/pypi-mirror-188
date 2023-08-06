from typing import List, Tuple

import netifaces


def get_local_ips() -> List[Tuple[str, str]]:
    ips = []
    for interface in netifaces.interfaces():
        ifaddresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET not in ifaddresses:
            continue
        for link in ifaddresses[netifaces.AF_INET]:
            ips.append((interface, link['addr']))
    return ips
