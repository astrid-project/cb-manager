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

Field                      | Type   | Required | Readonly | Example
---------------------------|--------|----------|----------|--------
`id`                       | String | True     | True     | dsalkasdioi232382yieyqwuiy
`agent_instance_id`        | String | False    | True     | filebeat
`ebpf_program_instance_id` | String | False    | True     | synflood@mysql-server
`timestamp_event`          | Date   | False    | True     | 2020/06/04 09:22:09
`timestamp_agent`          | Date   | False    | True     | 2020/06/04 09:22:19

It is not possible to update readonly fields.

## Create

To create a new network link use the following REST call:

**POST** /_network-link_

with the request body (in JSON format):

```json
{
    "id": "{name-network-link}",
    "agent_instance_id": "{id-agent-instance}",
}
```

Replace the data with the correct values, for example `name-network-link` with `eth0`.
The `type_id` should be one of those stored in [`network-link-type`](network-link-type.md) index.
It is possible to add additional data specific for this network link.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Network Link with the given [id] correctly created.",
        "data": {
            "id": "{name-network-link}",
            "type_id": "{id-network-link-type}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, a network link with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Network link with the given [id] already found",
        "data": {
            "id": "{name-network-link}"
        },
        "http_status_code": 409
    }
]
```

If some required data is missing (for example `type_id`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible to create a Network Link with the given [data]",
        "exception": "{'type_id': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{name-network-link}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of network links:

**GET** /_network-link_

The response includes all the network links created.

It is possible to filter the results using the following request body:

```json
{
    "select": ["type_id"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-network-link}"
        }
    }
}
```

In this way, it will be returned only the `type_id` of the network link with `id` = "_`{name-network-link}`_".

## Update

To update a network link, use:

**PUT** /_network_link_

```json
{
    id: "{name-network-link}",
    "type_id":"{new-id-network-link-type}",
}
```

This example set the new `type_id` for the network link with `id` = "_`{name-network-link}`_".
Also during the update it is possible to add additional data for the specific network link.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Network Link with the given [id] correctly updated.",
        "data": {
            "id": "{name-network-link}",
            "type_id":"{new-id-network-link-type}"
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
        "description": "Network Link with the given [id] not updated.",
        "data": {
            "id": "{name-connection}",
            "hostname": "{id-network-link-type}"
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a network link, use:

**DELETE** /_network-link_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-network-link}"
        }
    }
}
```

This request removes the network link with `id` = "_`{name-network-link}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Network with the given [id] correctly deleted.",
        "data": {
            "id": "{name-network-link}",
            "type_id": "{id-network-link-type}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the nework links\.
