from charms.reactive import (
    RelationBase,
    scopes,
    hook,
    bus)
from charmhelpers.core import hookenv


class BasicAuthCheckProvides(RelationBase):

    scope = scopes.UNIT

    class states(bus.StateList):
        available = bus.State('{relation_name}.available')
        changed = bus.State('{relation_name}.changed')

    @hook('{provides:basic-auth-check}-relation-{joined,changed}')
    def changed(self):
        self.set_state(self.states.available)

    @hook('{provides:basic-auth-check}-relation-{broken,departed}')
    def broken(self):
        self.remove_state(self.states.available)
        self.remove_state(self.states.changed)

    def configure(self, port):
        old_relation_info = {
            'hostname': self.get_local('hostname'),
            'port': self.get_local('port'),
        }
        relation_info = {
            'hostname': hookenv.unit_private_ip(),
            'port': port
        }
        self.set_remote(**relation_info)

        if relation_info != old_relation_info:
            self.set_local(**relation_info)
            self.set_state(self.states.changed)
        else:
            self.remove_state(self.states.changed)
