from charms.reactive import RelationBase, scopes, hook
from charmhelpers.core import hookenv


class BasicAuthCheckProvides(RelationBase):

    scope = scopes.UNIT

    @hook('{provides:basic-auth-check}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:basic-auth-check}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')

    def configure(self, port):
        relation_info = {
            'hostname': hookenv.unit_private_ip(),
            'port': port
        }
        self.set_remote(**relation_info)
