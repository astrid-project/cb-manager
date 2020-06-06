# Agent Instance

Contains the [agent](agent-catalog.md) instances installed in the [execution environments](exec-env.md).

- [Agent Instance](#agent-instance)
  - [Schema](#schema)
    - [Parameter Schema](#parameter-schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

## Schema

| Field              | Type                                    | Required | Readonly | Example               |
| ------------------ | --------------------------------------- | -------- | -------- | --------------------- |
| `id`               | String                                  | True     | True     | firewall@mysql-server |
| `agent_catalog_id` | String                                  | True     | True     | firewall              |
| `exec_env_id`      | String                                  | True     | True     | mysql-server          |
| `status`           | Enum(String)[started, stopped, unknown] | True     | True     | started               |
| `parameters`       | List(Parameter)                         | False    | False    |                       |
| `description`      | String                                  | False    | False    | [^1]                  |

[^1]: Collect system metrics from execution environments.

### Parameter Schema

| Field   | Type   | Required | Readonly | Example |
| ------- | ------ | -------- | -------- | ------- |
| `id`    | String | True     | True     | period  |
| `value` | String | True     | False    | 10s     |

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided.
  It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
  A common syntax is to use `agent_catalog_id` and `exec_env_id` concatenated with = '@'.
- `agent_catalog_id` should be one of those stored in [`agent-catalog`](agent-catalog.md) index.
- `exec_env_id` should be one of those stored in [`exec-env`](exec-env.md) index.

## Create

To create a new agent instance use the following REST call:

**POST** /_instance_ /_agent_

with the request body (in JSON format):

```json
{
    "id": "{agent_instance_name}",
    "parameters": [
        {
            "id": "{parameter_name}",
            "value": "{parameter_value}",
        }
    ],
    "actions": [

            "id": "{action_name}",
            "mode": "{action_mode_value}"
        }
    ]
}
```

Replace the data with the correct values, for example `agent_instance_name` with `firewall@mysql-server`.
It is possible to add additional data specific for this agent.
The `actions` fields is used to perform the actions defined in the catalog referenced by the `id`.
Any other fields (like, in the above example, `param` are used in the `cmd` field of
the action defined in the [catalog](agent-catalog.md)).
For example, if `cmd` is "firewall set {mode}" then it will be formatted using the values of the other fields.
If the action has a field `status` in the catalog, this field is used to update the status of the agent instance
if the execution finished correctly. Otherwise, if there are some error during the execution,
the `status` will be set to "unknown".

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Agent Instance with the given [id] correctly created.",
        "data": {
            "id": "{agent_instance_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an agent instance with the given `id` is already found, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Agent Instance with the given [id] already found",
        "data": {
            "id": "{agent_instance_name}",
            ...
        },
        "http_status_code": 409
    }
]
```

If some required data is missing (for example `status`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible to create a Agent Instance with the given [data]",
        "exception": "{'status': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{agent_instance_name}",
            ...
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of the agent instances:

**GET** /_instance_/_agent_

The response includes all the agent instances.

It is possible to filter the results using the following request body:

```json
{
    "select": ["parameters"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{agent_name}"
        }
    }
}
```

In this way, it will be returned only the `parameters` of the agent instance with `id` = "_`{agent_instance_name}`_"

## Update

To update an agent instance, use:

**PUT** /_instance_/_agent_

```json
{
    "id": "{agent_name}",
    "parameters": [
        {
            "id": "{parameter_name}",
            "value": "{new_parameter_value}"
        }
    ],
    "actions": [
        {
            "id": "{action_name}",
            "mode": "{new_action_mode_value}
        }
    ]
}
```

This example

1. updates the `valuee` of the `paramter` with `id` = "_`{parameter_name}`_";
2. execute a new action with  with `id` = "_`{action_name}`_

of the agent instance with `id` = `agent_instance_name`.

Also during the update it is possible to add additional data (not related to actions or parameters)
for the specific agent instances.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Agent Instance with the given [id] correctly updated.",
        "data": {
            "id": "{agent_instance_name}",
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
        "description": "Agent Instance with the given [id] not updated.",
        "data": {
            "id": "{agent_instance_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a agent instance, use:

**DELETE** /_instance_/_agent_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{agent_instance_name}"
        }
    }
}
```

This request removes the agent instance with `id` = "_`{agent_instance_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Agent Instance with the given [id] correctly deleted.",
        "data": {
            "id": "{agent_instance_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the agent instances.
