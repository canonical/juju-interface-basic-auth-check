# Juju interface for basic-auth-service

This is a Juju interface interface for
the [basic-auth-service](https://github.com/CanonicalLtd/basic-auth-service)
application.

It can be used to relate an application with the with the
basic-auth-service
[charm](https://github.com/CanonicalLtd/basic-auth-service-charm), and it
provides hostnames and ports for the related units.

The interface provides the following states:

- `basic-auth-check.available`: the relation has been established
- `basic-auth-check.changed`: relation configuration has changed

An example of use in a service related to basic-auth-service is

```python
@when('basic-auth-check.changed)
def basic_auth_check_available(basic_auth_check):
    for hostname, port in basic_auth_check.backends():
        configure_my_service(hostname, int(port))
```
