# Network Link

Represents a network link that connect two or more [execution environment](exec-env.md).

- [Network Link](#network-link)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

Field         | Type   | Required | Readonly | Example
--------------|--------|----------|----------|--------
`id`          | String | True     | True     | eth0
`description` | Text   | False    | False    | To connect HTTP and DB Servers.
`type_id`     | String | True     | False    | pnt2pnt

It is not possible to update readonly fields.

## Create

To create a new Network Link use the following REST call:

**POST** /_network-link_

with the request body (in JSON format):

```json
{
    "id": "{name-network-link}",
    "description":"{human-readable-description}",
    "type_id": "{id-network-link-type}",
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
            "description": "{human-readable-description}",
            "type_id": "{id-network-link-type}",
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, a network link with the given id is already found, this is the response:

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

If some data is missing (for example `type_id`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible create Network Link with the given [data]",
        "exception": "{'type_id': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{name-service}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of execution environment:

**GET** /_exec-env_

The response includes all the execution environments created.

It is possible to filter the results using the following request body:

```json
{
    "select": ["name"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-service}"
        }
    }
}
```

In this way, it will be returned only the `name` of all the network link with `id` = "_`{name-service}`_".

## Update

To update an execution environment, use:

**PUT** /_exec-env_

```json
{
    id: "{name-service}",
    "hostname":"{new-ip-address}",
}
```

This example set the new `hostname` for execution environment with `id` = "_`{name-service}`_".
Also during the update it is possible to add additional data for the specific execution environment.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Execution Environment with the given [id] correctly updated.",
        "data": {
            "id": "{name-service}",
            "hostname": "{ip-address}"
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
        "description": "Execution Environment with the given [id] not updated.",
        "data": {
            "id": "{name-service}",
            "hostname": "{new-ip-address}"
        },
        "http_status_code": 200
    }
]
```

The execution-environment model has not readonly fields.

## Delete

To delete an execution environment, use:

**DELETE** /_type_ / _exec-env_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-net-link}"
        }
    }
}
```

This request removes the network link with `id` = "_`{name-net-link}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Execution Environment with the given [id] correctly deleted.",
        "data": {
            "id": "{name-service}",
            "description": "{human-readable-description}",
            "type_id": "{id-exec-env-type}"
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the execution environments.
