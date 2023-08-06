import os, sys, math
from pathlib import Path
import logging
import base64

def prep_logger(verbose_count):
    log_level = logging.WARNING
    if verbose_count == 1:
        print("Info mode enabled.")
        log_level = logging.INFO
    elif verbose_count > 1:
        print("Debug mode enabled.")
        log_level = logging.DEBUG
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)


def cli(args=None):
    import argparse
    parser = argparse.ArgumentParser(description="Serialize binary file[s] into a javascript package which loads data and exports it as an object.")
    parser.add_argument("paths", nargs="+", help="Path to directory/directories or file[s] that are to be serialized and sharded.")
    parser.add_argument('-e', '--extensions', default=None, nargs='+', help='File extension[s] to filter by.')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-o', '--output', default='./output', help='Directory to output serialized js files.')
    parser.add_argument('-s', '--shard_size', default=64, type=int, help='The max size of each shard in megabytes. The default is 64 megabytes per shard.')
    parser.add_argument('-d', '--dcp', action='store_true', help='Turn on dcp package creation mode.')
    parser.add_argument('-p', '--package-name', type=str, help='The final DCP package name.')
    parser.add_argument('-f', '--network-patch', action='store_true', help='Turn on fetch and xmlhttprequest patch mode')
    args = parser.parse_args(args)

    prep_logger(args.verbose)

    if args.dcp:
        if (args.package_name is None):
            parser.error("--dcp/-d requires --package-name/-p.")
        from .dcp_package_serialize import serialize_files
    else:
        from .node_module_serialize import serialize_files

    serialize_files(**vars(args))
