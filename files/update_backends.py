import json
import sys
import subprocess

existing_backends = []


def main():
    new_backends = map(lambda b: Backend.from_config(b), json.loads(' '.join(sys.argv[1:])))
    backend_manager = BackendManager()

    for backend in new_backends:
        backend_manager.update_backend(backend)

    if backend_manager.changed:
        exit(2)
    else:
        exit(0)


class BackendManager:
    def __init__(self):
        self.existing_backends = self.get_existing_backends()
        self.changed = False

    def get_existing_backends(self):
        existing_backends = []
        proc_stdout = subprocess.run(["uberspace", "web", "backend", "list"], stdout=subprocess.PIPE, encoding="utf-8")
        backend_lines = proc_stdout.stdout.splitlines()
        for backend_line in backend_lines:
            if len(backend_line.strip()) == 0:
                continue

            existing_backends += [Backend.from_config_text(backend_line)]
        return existing_backends

    def backend_exists(self, backend):
        for existing_backend in self.existing_backends:
            if backend.route == existing_backend.route:
                return True
        return False

    def backend_correct(self, backend):
        for existing_backend in self.existing_backends:
            if backend.route == existing_backend.route and \
                    type(backend) == type(existing_backend) and \
                    ((not isinstance(backend, HTTPBackend)) or backend.port == existing_backend.port):
                return True
        return False

    def update_backend(self, backend):
        if backend.state.lower() == BackendStates.PRESENT and not self.backend_correct(backend):
            backend.add()
            self.changed = True
            self.existing_backends.append(backend)
        elif backend.state.lower() == BackendStates.ABSENT and self.backend_exists(backend):
            backend.remove()
            self.changed = True


class BackendStates:
    ABSENT = "absent"
    PRESENT = "present"

class Backend:
    def __init__(self, route, state=BackendStates.PRESENT):
        self.route = route
        self.state = state
    
    def remove(self):
        subprocess.run(["uberspace", "web", "backend", "del", self.route], stdout=subprocess.PIPE, encoding="utf-8")

    @staticmethod
    def from_config(config):
        if config.get("apache") or not config.get("http"):
            return ApacheBackend(config["route"], config.get("state", BackendStates.PRESENT))
        elif config.get("http"):
            return HTTPBackend(config["route"], config["http"]["port"], config.get("state", BackendStates.PRESENT))

    @staticmethod
    def from_config_text(text):
        [route, backend_name] = text.split(" => ")[0].split()
        if backend_name.startswith("http:"):
            return HTTPBackend(route, int(backend_name.split(":")[1]))
        elif backend_name == "apache":
            return ApacheBackend(route)


class ApacheBackend(Backend):
    def __init__(self, route, state=BackendStates.PRESENT):
        super().__init__(route, state)
    
    def add(self):
        subprocess.run(["uberspace", "web", "backend", "set", self.route, "--apache"], stdout=subprocess.PIPE, encoding="utf-8")


class HTTPBackend(Backend):
    def __init__(self, route, port, state=BackendStates.PRESENT):
        super().__init__(route, state)
        self.port = port
    
    def add(self):
        subprocess.run(["uberspace", "web", "backend", "set", self.route, "--http", "--port", str(self.port)], stdout=subprocess.PIPE, encoding="utf-8")
        

if __name__ == "__main__":
    main()
