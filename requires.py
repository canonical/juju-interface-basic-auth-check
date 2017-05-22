from charmhelpers.core import hookenv
from charms.reactive import (
    hook,
    RelationBase,
    scopes,
)


class BasicAuthCheckRequires(RelationBase):

    scope = scopes.UNIT

    @hook('{requires:basic-auth-check}-relation-{joined,changed}')
    def changed(self):
        for conv in self.conversations():
            if conv.get_remote('port'):
                # this unit's conversation has a port, so it is part of the set
                # of available units
                conv.set_state('{relation_name}.available')

    @hook('{requires:basic-auth-check}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

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
