from charms.reactive import (
    RelationBase,
    scopes,
    hook,
    bus)
from charmhelpers.core import hookenv


class BasicAuthCheckRequires(RelationBase):

    scope = scopes.UNIT

    class states(bus.StateList):
        available = bus.State('{relation_name}.available')
        changed = bus.State('{relation_name}.changed')

    @hook('{requires:basic-auth-check}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('port'):
            # If the port is configured, relation data are correctly set
            conv.set_state(self.states.available)
            hookenv.log('basic-auth-check relation available')
        self._check_state_changed(conv)

    @hook('{requires:basic-auth-check}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state(self.states.available)
        self._check_state_changed(conv)
        hookenv.log('basic-auth-check relation is gone')

    def backends(self):
        """Returns available targets as a list of (hostname, port) tuples."""
        backends = []
        for conv in self.conversations():
            if conv.scope is None:
                continue

            host = conv.get_local('hostname')
            port = conv.get_local('port')
            if host and port:
                backends.append((host, port))
        return backends

    def _check_state_changed(self, conv):
        old_relation_info = {
            'hostname': conv.get_local('hostname'),
            'port': conv.get_local('port')
        }
        relation_info = {
            'hostname': conv.get_remote('hostname'),
            'port': conv.get_remote('port')
        }
        relation_gone = not conv.is_state(self.states.available)
        if relation_info != old_relation_info or relation_gone:
            conv.set_local(**relation_info)
            conv.set_state(self.states.changed)
            hookenv.log(
                'basic-auth-check relation data changed: {}'.format(
                    relation_info))
            hookenv.atexit(self._clean_state_changed)

    def _clean_state_changed(self):
        conv = self.conversation()
        conv.remove_state(self.states.changed)
        hookenv.log('basic-auth-check changed stated removed')
