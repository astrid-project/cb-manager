# Execution Environment Type

Describes the type of the execution environment including additional info.
Each [execution environment](exec-env.md) belongs to a specific type that is referred with the [`type_id`](exec-env.md#create) field.

- [Execution Environment Type](#execution-environment-type)
  - [Schema](#schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)
  - [Loaded data](#loaded-data)

## Schema

Field         | Type   | Required | Readonly | Example
--------------|--------|----------|----------|--------
`id`          | String | True     | True     | vm
`name`        | String | True     | False    | Virtual Machine
`description` | Text   | False    | False    | The service is deployed in virtual machine.

It is not possible to update readonly fields.

## Create

To create a new Execution Environment Type use the following REST call:

**POST** /_type_/_exec-env_

with the request body (in JSON format):

```json
{
    id: "{name-type}",
    "name": "{formal-name}"
}
```

Replace the data with the correct values, for example `name-type`, and `formal-name` with `vm`
and `Virtual Machine`, respectively.
The `id` is auto generated if missing in the request body.
It is possible to add additional data specific for this execution environment type.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Execution Environment Type with the given [id] correctly created.",
        "data": {
            "id": "{name-type}",
            "name": "{forma-name}"
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an execution environment type with the given id is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Execution Environment Type with the given [id] already found",
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
        "description": "Not possible create Execution Environment with the given [data]",
        "exception": "{'name': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{name-type}",
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of execution environment:

**GET** /_type_/_exec-env_

The response includes all the execution environment types created.

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

In this way, it will be returned only the `name` of all the execution environment types with `id` = "_`{name-type}`_"

## Update

To update an execution environment type, use:

**PUT** /_type_/_exec-env_

```json
{
    id: "{name-type}",
    "name":"{new-formal-name}",
}
```

This example set the new `name` for execution environment type with `id` = "_`{name-type}`_".
Also during the update it is possible to add additional data for the specific execution environment type.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Execution Environment Type with the given [id] correctly updated.",
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
        "description": "Execution Environment Type with the given [id] not updated.",
        "data": {
            "id": "{name-type}",
            "name": "{formal-name}"
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete an execution environment type, use:

**DELETE** /_type_/_exec-env_

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

This request removes the execution environment type with `id` = "_`{name-type}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Execution Environment Type with the given [id] correctly deleted.",
        "data": {
            "name": "{formal-name}",
            "id": "{name-type}"
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the execution environments.

## Loaded data

For the demo, this data are already available:

Response of **GET** /_type_/_exec-env_

```json
[
    {
        "id": "vm",
        "name": "Virtual Machine",
        "description": "The service is deployed in a virtual machine."
    },
    {
        "id": "container",
        "name": "Container",
        "description": "The service is deployed in a container."
    },
    {
        "id": "host",
        "name": "Host",
        "description": "The service is deployed in a physical machine."
    }
]
```
