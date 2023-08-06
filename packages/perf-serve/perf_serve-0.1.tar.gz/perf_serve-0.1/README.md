# perf-serve

Easily serve linux perf profile for firefox profiler.

# Usage

Just run `python3 main.py` in directory containing perf.data. That will run `perf script` and start serving resulting file on some free port. See `python3 main.py --help` for more usage information.

Due to https://github.com/firefox-devtools/profiler/issues/3766 it is currently impossible to load perf profiles from URL. While this issue is not fixed, perf-serve will default to using profiler.forestryks.org, which is just hot-fixed version of firefox profiler

# Installation

TODO
