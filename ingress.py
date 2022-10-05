import requests
from .resurrect import Resurrect
from time import sleep
from ops.charm import CharmBase

class MyCharm(CharmBase):
    def __init__(self, charm):
        self.resurrect = Resurrect(self, self._check_endpoint())
        self.framework.observe(self.resurrect.on.trigger, self._on_resurrect_trigger)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.remove, self._on_remove)

    def _on_start(self, _):
        # prime the Resurrect with the current env, plus this additional custom var.
        self.resurrect.prime({'CUSTOM_ENV_VAR':'foo'})
        self.resurrect.start()

    def _check_endpoint(self) -> None:
        r = requests.get("http://example.com")

        while r.return_code == 404:
            sleep(1)

        return

    def _on_resurrect_trigger(self, _):
        print("Ingress is ready!")

    def _on_remove(self, _):
        self.resurrect.stop()
