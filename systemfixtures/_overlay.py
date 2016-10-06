from fixtures import MonkeyPatch


class Overlay(MonkeyPatch):

    def __init__(self, name, overlay, condition):
        super(Overlay, self).__init__(name, self._new_value)
        self.overlay = overlay
        self.condition = condition

    def _setUp(self):
        # XXX copied from MonkeyPatch
        location, attribute = self.name.rsplit('.', 1)
        __import__(location, {}, {})
        components = location.split('.')
        current = __import__(components[0], {}, {})
        for component in components[1:]:
            current = getattr(current, component)
        self._old_value = getattr(current, attribute)
        super(Overlay, self)._setUp()

    def _new_value(self, *args, **kwargs):
        if self.condition(*args, **kwargs):
            return self.overlay(self._old_value, *args, **kwargs)
        else:
            return self._old_value(*args, **kwargs)
