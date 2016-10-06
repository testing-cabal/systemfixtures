import io
import argparse


class Wget(object):

    name = "wget"

    def __init__(self, locations=None):
        self.locations = locations or {}

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("url")
        parser.add_argument("-O", dest="output")
        parser.add_argument("-q", dest="quiet", action="store_true")
        parser.add_argument("--no-check-certificate", action="store_true")
        args = parser.parse_args(proc_args["args"][1:])
        content = self.locations[args.url]
        result = {}
        if args.output == "-":
            result["stdout"] = io.BytesIO(content)
        else:
            with open(args.output, "wb") as fd:
                fd.write(content)
        return result
