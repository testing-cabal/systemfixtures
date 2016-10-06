import os

import argparse


class Dpkg(object):

    name = "dpkg"

    def __init__(self):
        self.actions = {}

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", dest="install")
        args = parser.parse_args(proc_args["args"][1:])
        if args.install:
            package = os.path.basename(args.install)
            if package.endswith(".deb"):
                package = package[:-len(".deb")]
            package = package.split("_")[0]
            actions = self.actions.setdefault(package, [])
            actions.append("install")
        return {}
