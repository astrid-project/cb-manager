# Connection

Defines the connection between [execution environments](exec-env.md) and [network links](network-link.md).

- [Connection](#connection)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

Field             | Type   | Required | Readonly | Example
------------------|--------|----------|----------|--------
`id`              | String | True     | True     | http-db-connection
`exec_env_id`     | String | True     | True     | mysql-server
`network_link_id` | String | True     | True     | eth0
`description`     | Text   | False    | False    | Connection for the HTTP and DB Servers.

It is not possible to update readonly fields.

## Create

To create a new connection use the following REST call:

**POST** /_connection_

with the request body (in JSON format):

```json
{
    "id": "{name-connection}",
    "exec_env_id": "{id-exec-env}",
    "network_link_id": "{id-network-link}",
    "description": "{human-readable-description}"
}
```

Replace the data with the correct values, for example `name-connection` with `http-db-connection`.
The `id` is auto generated if missing in the request body.
The `exec_env_id` should be one of those stored in [`exec-env`](exec-env.md) index.
The `network_link_id` should be one of those stored in [`network-link`](network-link.md) index.
It is possible to add additional data specific for this connection.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Connection with the given [id] correctly created.",
        "data": {
            "id": "{name-connection}",
            "exec_env_id": "{id-exec-env}",
            "network_link_id": "{id-network-link}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, a connection with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Connection with the given [id] already found",
        "data": {
            "id": "{name-connection}"
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
        "description": "Not possible to create a Connection with the given [data]",
        "exception": "{'exec_env_id': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{name-connection}",
            "network_link_id": "{id-network-link}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of connections:

**GET** /_connection_

The response includes all the connections created.

It is possible to filter the results using the following request body:

```json
{
    "select": ["network_link_id"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-connection}"
        }
    }
}
```

In this way, it will be returned only the `network_link_id` of the connection with `id` = "_`{name-connection}`_"

## Update

To update a connection, use:

**PUT** /_connection_

```json
{
    "id": "{name-connection}",
    "description":"{new-human-readable-description}"
}
```

This example set the new `description` for the connecion with `id` = "_`{name-connection}`_".
Also during the update it is possible to add additional data for the specific connection.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Connection with the given [id] correctly updated.",
        "data": {
            "id": "{name-connection}",
            "description":"{new-human-readable-description}"
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
        "description": "Connection with the given [id] not updated.",
        "data": {
            "id": "{name-connection}",
            "description":"{new-human-readable-description}"
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a connection, use:

**DELETE** /_connection_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{name-connection}"
        }
    }
}
```

This request removes the connection with `id` = "_`{name-connection}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Connection with the given [id] correctly deleted.",
        "data": {
            "id": "{name-connection}",
            "exec_env_id": "{id-exec-env}",
            "network_link_id": "{id-network-link}",
            "description": "{human-readable-description}"
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the connection.
