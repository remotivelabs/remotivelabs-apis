# File format schemas

Compiled for documentation available at <https://docs.remotivelabs.com/>.

## Validation of sample `interfaces.json` files

We have a
[number](https://github.com/search?q=org%3Aremotivelabs+path%3A**%2Finterfaces.json+language%3AJSON&type=code&ref=advsearch)
of sample RemotiveBroker configurations in our public repositories. To ensure that we only publish configurations that
comply with the configuration schema in this repository, it is recommended to validate them with the validation task,
which can be run from RemotiveBroker repository.

```bash
mix broker.validate_configuration /path/to/configuration/interfaces.json
mix broker.validate_configuration --distributed /path/to/distributed/configuration/interfaces.json
```
