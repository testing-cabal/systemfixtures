import io


class Systemctl(object):

    name = "systemctl"

    def __init__(self):
        self.actions = {}

    def __call__(self, proc_args):
        action, service_name = proc_args["args"][1:]
        actions = self.actions.setdefault(service_name, [])
        returncode = 0
        stdout = io.BytesIO()
        if action == "is-active":
            if not actions or actions[-1] != "start":
                returncode = 3
                stdout.write(b"inactive\n")
            else:
                stdout.write(b"active\n")
        else:
            actions.append(action)
        return {"stdout": stdout, "returncode": returncode}
