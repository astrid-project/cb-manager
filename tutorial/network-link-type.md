# Network Link Type

Describes the type of the network link including additional info.
Each [network link](network-link.md) belongs to a specific type that is referred
with the [`type_id`](network-link.md#create) field.

- [Network Link Type](#network-link-type)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)
  - [Loaded data](#loaded-data)

## Schema

| Field         | Type   | Required | Readonly | Example                                                                 |
| ------------- | ------ | -------- | -------- | ----------------------------------------------------------------------- |
| `id`          | String | True     | True     | pnt2pnt                                                                 |
| `name`        | String | True     | False    | Point to Point                                                          |
| `description` | String | False    | False    | Communications connection between two communication endpoints or nodes. |

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided. It is recommended to provide a friendly for simplify the retrieve of
  connected date in other indices.

## Create

To create a new network link type use the following REST call:

**POST** /_type_/_network-link_

with the request body (in JSON format):

```json
{
    "id": "{type_name}",
    "description": "{human_readable_description}"
    "name": "{formal_name}"
}
```

Replace the data with the correct values, for example `id` with `p2p.
It is possible to add additional data specific for this network link type.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Network Link Type with the given [id] correctly created.",
        "data": {
            "id": "{type_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, a network link type with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Network Link Type with the given [id] already found",
        "data": {
            "id": "{type_name}",
            ...
        },
        "http_status_code": 409
    }
]
```

If some required data is missing (for example `name`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible to create a Network Link with the given [data]",
        "exception": "{'name': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{type_name}",
            ...
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of network Link types:

**GET** /_type_/_network-link_

The response includes all the network link types created.

It is possible to filter the results using the following request body:

```json
{
    "select": ["name"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{type_name}"
        }
    }
}
```

In this way, it will be returned only the `name` of all the network link types with `id` = "_`{type_name}`_"

## Update

To update a network Link type, use:

**PUT** /_type_/_network-link_

```json
{
    "id": "{type_name}",
    "name":"{new_formal_name}",
}
```

This example set the new `name` for the network link type with `id` = "_`{type_name}`_".
Also during the update it is possible to add additional data for the specific network link type.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Network Link Type with the given [id] correctly updated.",
        "data": {
            "id": "{type_name}",
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
        "description": "Network Link Type with the given [id] not updated.",
        "data": {
            "id": "{type_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a network link type, use:

**DELETE** /_type_/_network-link_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{type_name}"
        }
    }
}
```

This request removes the network link type with `id` = "_`{type_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Network Link Type with the given [id] correctly deleted.",
        "data": {
            "id": "{type_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the network links.

## Loaded data

For the demo, this data is already available:

Response of **GET** /_type_/_network-link_

```json
[
    {
        "id": "p2p",
        "name": "Point to Point",
        "description": "Communications connection between two communication endpoints or nodes."
    },
    {
        "id": "slide",
        "name": "Slice",
        "description": """Separation of multiple virtual networks that operate on the same physical hardware
                          for different applications, services or purposes."""
    }
]
```
