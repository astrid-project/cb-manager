# Network Link

Represents a network link that connect two or more [execution environment](exec-env.md).

- [Network Link](#network-link)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

| Field         | Type   | Required | Readonly | Example                         |
| ------------- | ------ | -------- | -------- | ------------------------------- |
| `id`          | String | True     | True     | eth0                            |
| `type_id`     | String | True     | False    | pnt2pnt                         |
| `description` | String | False    | False    | To connect HTTP and DB Servers. |

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided. It is recommended to provide a friendly for simplify the retrieve of
  connected date in other indices.
- `type_id` should be one of those stored in [`network-link-type`](network-link-type.md) index.

## Create

To create a new network link use the following REST call:

**POST** /_network-link_

with the request body (in JSON format):

```json
{
    "id": "{network_link_name}",
    "type_id": "{network_link_type_id}",
    "description":"{human_readable_description}"
}
```

Replace the data with the correct values, for example `network_link_name` with `eth0`.
It is possible to add additional data specific for this network link.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Network Link with the given [id] correctly created.",
        "data": {
            "id": "{network_link_name}",
            ...
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
            "id": "{network_link_name}",
            ...
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
            "id": "{network_link_name}",
            ...
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
            "expr": "{network_link_name}"
        }
    }
}
```

In this way, it will be returned only the `type_id` of the network link with `id` = "_`{network_link_name}`_".

## Update

To update a network link, use:

**PUT** /_network_link_

```json
{
    "id": "{network_link_name}",
    "type_id":"{new_network_link_type_id}",
}
```

This example set the new `type_id` for the network link with `id` = "_`{network_link_name}`_".
Also during the update it is possible to add additional data for the specific network link.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Network Link with the given [id] correctly updated.",
        "data": {
            "id": "{network_link_name}",
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
        "description": "Network Link with the given [id] not updated.",
        "data": {
            "id": "{name-connection}",
            ...
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
            "expr": "{network_link_name}"
        }
    }
}
```

This request removes the network link with `id` = "_`{network_link_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Network Link with the given [id] correctly deleted.",
        "data": {
            "id": "{network_link_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the network links.
