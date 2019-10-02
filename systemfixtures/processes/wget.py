import io
import os
import argparse


class Wget(object):

    name = "wget"

    def __init__(self, locations=None):
        self.locations = locations or {}

    def __call__(self, proc_args):
        cwd = proc_args.get("cwd") or ""
        parser = argparse.ArgumentParser()
        parser.add_argument("url")
        parser.add_argument("-O", dest="output")
        parser.add_argument("-q", dest="quiet", action="store_true")
        parser.add_argument("-N", dest="timestamping", action="store_true")
        parser.add_argument("--no-check-certificate", action="store_true")
        args = parser.parse_args(proc_args["args"][1:])
        content = self.locations[args.url]
        file = args.url.split("/")[-1]
        file_dir = os.path.join(cwd, file)
        result = {}
        if args.output == "-":
            result["stdout"] = io.BytesIO(content)
        elif (args.output is None):
            with open(file_dir, "wb") as fd:
                fd.write(content)
        else:
            with open(args.output, "wb") as fd:
                fd.write(content)

        return result
