# Execution Environment

The execution environment represents the remove service.
When the service is deployed by the the orchestrator, it is necessary to insert related info to the Context Broker.

- [Execution Environment](#execution-environment)
  - [Schema](#schema)
    - [LCP Schema](#lcp-schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

| Field         | Type   | Required | Readonly | Example                                                    |
| ------------- | ------ | -------- | -------- | ---------------------------------------------------------- |
| `id`          | String | True     | True     | mysql-server                                               |
| `hostname`    | String | True     | False    | 10.0.0.1                                                   |
| `type_id`     | String | True     | False    | vm                                                         |
| `lcp`         | LCP    | True     | False    |
| `description` | String | False    | False    | Open-source relational database management system (RDBMS). |

### LCP Schema

| Field            | Type    | Required | Readonly | Example |
| ---------------- | ------- | -------- | -------- | ------- |
| `port`           | Integer | True     | False    | 4000    |
| `username`       | String  | False    | True     |         |
| `password`       | String  | False    | True     |         |
| `cb_password`    | String  | False    | True     |         |
| `cb_expiration`  | Date    | False    | True     |         |
| `last_heartbeat` | Date    | False    | True     |         |

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided. It is recommended to provide a friendly for simplify the retrieve of
  connected date in other indices.
- `type_id` should be one of those stored in [`exec-env-type`](exec-env-type.md) index.

## Create

To create a new Execution Environment use the following REST call:

**POST** /_exec-env_

with the request body (in JSON format):

```json
{
    "id": "{service_name}",
    "description": "{human_readable_description}",
    "type_id": "{exec_env_type_name}",
    "hostname":"{ip_address}",
    "lcp": {
        "port" {lcp_port}
    }
}
```

Replace the data with the correct values, for example `service_name` with `apache`.
It is possible to add additional data specific for this execution environment.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Execution Environment with the given [id] correctly created.",
        "data": {
            "id": "{service_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an execution environment with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Execution Environment with the given [id] already found",
        "data": {
            "id": "{service_name}",
            ...
        },
        "http_status_code": 409
    }
]
```

If some required data is missing (for example `hostname`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible to create a Execution Environment with the given [data]",
        "exception": "{'hostname': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{service_name}",
            ...
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
    "select": ["hostname"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{service_name}"
        }
    }
}
```

In this way, it will be returned only the `hostname` of all the execution environments with `id` = "_`{service_name}`_"

## Update

To update an execution environment, use:

**PUT** /_exec-env_

```json
{
    "id": "{service_name}",
    "hostname":"{new_ip_address}",
}
```

This example set the new `hostname` for execution environment with `id` = "_`{service_name}`_".
Also during the update it is possible to add additional data for the specific execution environment.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Execution Environment with the given [id] correctly updated.",
        "data": {
            "id": "{service_name}",
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
        "description": "Execution Environment with the given [id] not updated.",
        "data": {
            "id": "{service_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete an execution environment, use:

**DELETE** /_exec-env_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{service_name}"
        }
    }
}
```

This request removes the execution environment with `id` = "_`{service_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Execution Environment with the given [id] correctly deleted.",
        "data": {
            "id": "{service_name}",
            ,,,
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the execution environments.
