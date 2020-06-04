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

Field         | Type   | Required | Readonly | Example
--------------|--------|----------|----------|--------
`id`          | String | True     | True     | pnt2pnt
`name`        | String | True     | False    | Point to Point
`description` | Text   | False    | False    | Communications connection between two communication endpoints or nodes.

It is not possible to update readonly fields.

## Create

To create a new Network Link Type use the following REST call:

**POST** /_type_/_network-link_

with the request body (in JSON format):

```json
{
    "id": "{name-type}",
    "description": "{human-readable-description}"
    "name": "{formal-name}"
}
```

Replace the data with the correct values, for example `id`, and `name` with `vm`
and `Virtual Machine`, respectively.
The `id` is auto generated if missing in the request body.
It is possible to add additional data specific for this Network Link type.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Network Link Type with the given [id] correctly created.",
        "data": {
            "id": "{name-type}",
            "name": "{forma-name}"
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an Network Link type with the given id is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Network Link Type with the given [id] already found",
        "data": {
            "id": "{name-type}"
        },
        "http_status_code": 409
    }
]
```

If some data is missing (for example `name`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible create Network Link with the given [data]",
        "exception": "{'name': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{name-type}",
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of Network Link:

**GET** /_type_/_network-link_

The response includes all the Network Link types created.

It is possible to filter the results using the following request body:

```json
{
    "select": ["name"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-type}"
        }
    }
}
```

In this way, it will be returned only the `name` of all the Network Link types with `id` = "_`{name-type}`_"

## Update

To update an Network Link type, use:

**PUT** /_type_/_network-link_

```json
{
    id: "{name-type}",
    "name":"{new-formal-name}",
}
```

This example set the new `name` for Network Link type with `id` = "_`{name-type}`_".
Also during the update it is possible to add additional data for the specific Network Link type.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Network Link Type with the given [id] correctly updated.",
        "data": {
            "id": "{name-type}",
            "name": "{new-formal-name}"
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
            "id": "{name-type}",
            "name": "{formal-name}"
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete an Network Link type, use:

**DELETE** /_type_/_network-link_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-type}"
        }
    }
}
```

This request removes the Network Link type with `id` = "_`{name-type}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Network Link Type with the given [id] correctly deleted.",
        "data": {
            "id": "{name-type}",
            "description": "{human-readable-description}",
            "name": "{formal-name}",
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the Network Links.

## Loaded data

For the demo, this data are already available:

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
