# Data

This index stores all the incoming data from the [execution environments](exec-env.md) collected
by the [agent](agent-instance.md) or [eBPF](ebpf-program-instance.md) instance installed on them.

- [Data](#data)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

| Field                      | Type   | Required | Readonly | Example                    |
| -------------------------- | ------ | -------- | -------- | -------------------------- |
| `id`                       | String | True     | True     | dsalkasdioi232382yieyqwuiy |
| `agent_instance_id`        | String | False    | True     | filebeat@mysql-server      |
| `ebpf_program_instance_id` | String | False    | True     | synflood@mysql-server      |
| `timestamp_event`          | Date   | False    | True     | 2020/06/04 09:22:09        |
| `timestamp_agent`          | Date   | False    | True     | 2020/06/04 09:22:19        |

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided. It is recommended to provide a friendly for simplify the retrieve of
  connected date in other indices.
- `agent_instance_id` should be one of those stored in [`agent-instance`](agent-instance.md) index.
- `ebpf_program_instance_id` should be one of those stored in [`ebpf-program-instance`](ebpf-program-instance.md) index.

## Create

To create a new data use the following REST call:

**POST** /_data_

with the request body (in JSON format):

```json
{
    "id": "{data_name}",
    "agent_instance_id": "{agent_instance_id}",
    "timestamp_event": "{timestamp_event}",
    "timestamp_agent": "{timestamp_agent}",
}
```

Replace the data with the correct values, for example `agent_instance_id` with `filebeat@mysql-server`.
It is possible to add additional data.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Data with the given [id] correctly created.",
        "data": {
            "id": "{data_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, a data with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Data with the given [id] already found",
        "data": {
            "id": "{data_name}",
            ...
        },
        "http_status_code": 409
    }
]
```

## Read

To get the list of data:

**GET** /_data_

The response includes all the data created.

It is possible to filter the results using the following request body:

```json
{
    "select": ["type_id"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{data_name}"
        }
    }
}
```

In this way, it will be returned only the `type_id` of the data with `id` = "_`{data_name}`_".

## Update

To update a data, use:

**PUT** /_data_

```json
{
    "id": "{data_name}",
    "source":"{ip_address}",
}
```

This example add a new field `source` for the data with `id` = "_`{data_name}`_".

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Data with the given [id] correctly updated.",
        "data": {
            "id": "{data_name}",
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
        "description": "Data with the given [id] not updated.",
        "data": {
            "id": "{data_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a data, use:

**DELETE** /_data_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{data_name}"
        }
    }
}
```

This request removes the data with `id` = "_`{data_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Data with the given [id] correctly deleted.",
        "data": {
            "id": "{data_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the data.
