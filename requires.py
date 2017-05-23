from charms.reactive import (
    RelationBase,
    scopes,
    hook,
    bus)


class BasicAuthCheckRequires(RelationBase):

    scope = scopes.UNIT

    class states(bus.StateList):
        available = bus.State('{relation_name}.available')
        changed = bus.State('{relation_name}.changed')

    @hook('{requires:basic-auth-check}-relation-{joined,changed}')
    def changed(self):
        for conv in self.conversations():
            if conv.get_remote('port'):
                # If the port is configured, relation data are correctly set
                conv.set_state(self.states.available)
            self._check_state_changed(conv)

    @hook('{requires:basic-auth-check}-relation-{departed,broken}')
    def broken(self):
        for conv in self.conversations():
            conv.remove_state(self.states.available)
            conv.remove_state(self.states.changed)

    def backends(self):
        """Returns available targets.

        The returned value is a list of (hostname, port) tuples.

        """
        backends = []
        for conv in self.conversations():
            host = (conv.get_remote('hostname') or
                    conv.get_remote('private-address'))
            port = conv.get_remote('port')
            if host and port:
                backends.append((host, port))
        return backends

    def _check_state_changed(self, conv):
        old_relation_info = {
            'hostname': conv.get_local('hostname'),
            'port': conv.get_local('port'),
        }
        relation_info = {
            'hostname': (
                conv.get_remote('hostname') or
                conv.get_remote('private-address')),
            'port': conv.get_remote('port')
        }
        if relation_info != old_relation_info:
            conv.set_local(**relation_info)
            conv.set_state(self.states.changed)
        else:
            conv.remove_state(self.states.changed)
