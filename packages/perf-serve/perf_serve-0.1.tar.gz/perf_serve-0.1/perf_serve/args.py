from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Args:
    path: Path
    address: str
    port: int
    hyperlinks_enabled: bool
    profiler_url: str


def parse_args() -> Args:
    parser = ArgumentParser()
    parser.add_argument("--address", help="set address to serve on, defaults to 0.0.0.0", default="0.0.0.0", type=str)
    parser.add_argument("--port", help="set port to serve on, defaults to random", default=0, type=int)
    parser.add_argument("--no-hyperlinks", help="disable hyperlinks", action="store_true")
    parser.add_argument("--profiler-url", help="change profiler url used for generating links", default="profiler.forestryks.org", type=str)
    parser.add_argument("file", help="path to perf.data, defaults to perf.data in current directory", nargs="?", default=Path("perf.data"), type=Path)
    args = parser.parse_args()

    return Args(args.file, args.address, args.port, not args.no_hyperlinks, args.profiler_url)
