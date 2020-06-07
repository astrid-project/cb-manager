# eBPF Program Instance

Contains the [eBPF Program](catalog.md) instances installed in the [execution environments](../exec-env/README.md).

- [eBPF Program Instance](#ebpf-program-instance)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

| Field                     | Type                                    | Required | Readonly | Example                     |
| ------------------------- | --------------------------------------- | -------- | -------- | --------------------------- |
| `id`                      | String                                  | True     | True     | packet-counter@mysql-server |
| `ebpf_program_catalog_id` | String                                  | True     | True     | packet-counter              |
| `exec_env_id`             | String                                  | True     | True     | mysql-server                |
| `description`             | String                                  | False    | False    | [^1]                        |

[^1]: Collect system metrics from Apache HTTP Web Server.

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided.
  It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
  A common syntax is to use `ebpf_program_catalog_id` and `exec_env_id` concatenated with = '@'.
- `ebpf_program_catalog_id` should be one of those stored in [`ebpf-program-catalog`](catalog.md) index.
- `exec_env_id` should be one of those stored in [`exec-env`](../exec-env/README.md) index.

## Create

To create a new eBPF Program instance use the following REST call:

**POST** /_instance_/_ebpf-program_

with the request body (in JSON format):

```json
{
    "id": "{ebpf_program_instance_name}",
    "ebpf_program_catalog_id": "{ebpf_program_name}",
    "exec_env_id": "{exec_env_name}"
}
```

Replace the data with the correct values, for example `ebpf_program_instance_name` with `packet-counter@mysql-server`.
It is possible to add additional data specific for this eBPF Program.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "eBPF Program Instance with the given [id] correctly created.",
        "data": {
            "id": "{ebpf_program_instance_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an eBPF Program instance with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "eBPF Program Instance with the given [id] already found",
        "data": {
            "id": "{ebpf_program_instance_name}",
            ...
        },
        "http_status_code": 409
    }
]
```

If some required data is missing (for example `exec_env_id`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible to create a eBPF Program Instance with the given [data]",
        "exception": "{'exec_end_id': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{ebpf_program_instance_name}",
            ...
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of the eBPF Program instances:

**GET** /_instance_/_ebpf-program_

The response includes all the eBPF Program instances.

It is possible to filter the results using the following request body:

```json
{
    "select": ["exec_env_id"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{ebpf_program_instance_name}"
        }
    }
}
```

In this way, it will be returned only the `exec_env_id` of the eBPF Program instance with `id` = "_`{ebpf_program_instance_name}`_"

## Update

To update an eBPF Program instance, use:

**PUT** /_instance_/_ebpf-program_

```json
{
    "id": "{epbf_program_instance_name}",
    "description": "{human_readable_description}"
}
```

This example set the `description` to "_`{human_readable_description}`_" of the eBPF Program instance with `id` = `ebpf_program_instance_name`.

Also during the update it is possible to add additional data (not related to actions or parameters)
for the specific eBPF Program instances.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "eBPF Program Instance with the given [id] correctly updated.",
        "data": {
            "id": "{ebpf_program_instance_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

Instead, if the are not changes the response is:

```json
[
    {
        "status": "noop",
        "description": "eBPF Program Instance with the given [id] not updated.",
        "data": {
            "id": "{ebpf_program_instance_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a eBPF Program instance, use:

**DELETE** /_instance_/_ebpf-program_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{ebpf_program_instance_name}"
        }
    }
}
```

This request removes the eBPF Program instance with `id` = "_`{ebpf_program_instance_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "eBPF Program Instance with the given [id] correctly deleted.",
        "data": {
            "id": "{ebpf_program_instance_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the eBPF Program instances.
