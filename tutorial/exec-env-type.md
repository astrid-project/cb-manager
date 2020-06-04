# Execution Environment Type

- [Execution Environment Type](#execution-environment-type)
  - [Read](#read)

## Read

**GET** /_type_/_exec-env_

A possible response is:

```json
[
    {
        "id": "vm",
        "name": "Virtual Machine"
    },
    {
        "id": "container",
        "name": "Container"
    },
    {
        "id": "host",
        "name": "Host"
    }
]
```
