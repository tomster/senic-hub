import nuimo
import threading


class SetupManager(nuimo.ControllerManagerListener):
    def __init__(self, adapter_name):
        self._manager = nuimo.ControllerManager(adapter_name)
        self._manager.listener = self
        self._controller = None

    def discover_and_connect_controller(self):
        # TODO: If there's a connected Nuimo, take it and don't run discovery
        self._manager.start_discovery()
        # Start D-Bus event loop. Will be stopped when a controller was connected (see below)
        self._manager.run()
        if self._controller:
            return self._controller.mac_address
        else:
            return None

    def controller_discovered(self, controller):
        controller.listener = _SetupControllerListener(self, controller)
        controller.connect()

    def controller_connected(self, controller):
        self._controller = controller
        self._manager.stop_discovery()
        self._manager.stop()


class _SetupControllerListener(nuimo.ControllerListener):
    def __init__(self, manager, controller):
        self.manager = manager
        self.controller = controller

    def connect_succeeded(self):
        self.manager.controller_connected(self.controller)

    def connect_failed(self, error):
        # TODO: If connection failed, it should then be discovered again by nuimo.ControllerManager
        pass
