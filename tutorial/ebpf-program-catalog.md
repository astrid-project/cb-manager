# eBPF Program Catalog

Contains the available eBPF programs to be installed in the [execution environments](exec-env.md).

- [eBPF Program Catalog](#ebpf-program-catalog)
  - [Schema](#schema)
    - [Config Schema](#config-schema)
      - [Config Metric Schema](#config-metric-schema)
      - [Config Metric Label Schema](#config-metric-label-schema)
    - [Parameter Schema](#parameter-schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)
  - [Loaded data](#loaded-data)

## Schema

| Field         | Type            | Required | Readonly | Example        |
| ------------- | --------------- | -------- | -------- | -------------- |
| `id`          | String          | True     | True     | packet-counter |
| `config`      | Config          | True     | False    |                |
| `parameters`  | List(Parameter) | False    | False    |                |
| `description` | String          | False    | False    | [^1]           |

[^1]: Transparent service to capture packets flowing through the interface it is attached to,
      apply filters and obtain capture in .pcap format.

### Config Schema

| Field     | Type                        | Required | Readonly | Example |
| --------- | --------------------------- | -------- | -------- | ------- |
| `code`    | String                      | True     | False    |         |
| `metrics` | List(ParameterConfigMetric) | False    | False    |         |

#### Config Metric Schema

| Field                   | Type                        | Required | Readonly | Example |
| ----------------------- | --------------------------- | -------- | -------- | ------- |
| `name`                  | String                      | True     | False    |         |
| `map_name`              | String                      | False    | False    | x       |
| `open_metrics_metadata` | List(ParameterConfigMetric) | False    | False    |         |


#### Config Metric Label Schema

| Field   | Type   | Required | Readonly | Example  |
| ------- | ------ | -------- | -------- | -------- |
| `name`  | String | True     | False    | IP_PROTO |
| `value` | String | True     | False    | UPD      |


### Parameter Schema

| Field         | Type              | Required | Readonly | Example                      |
| ------------- | ----------------- | -------- | -------- | ---------------------------- |
| `id`          | String            | True     | True     | start                        |
| `type`        | Enum(String) [^2] | True     | False    | integer                      |
| `list`        | Boolean           | False    | False    | False                        |
| `values`      | Enum(String)      | False    | False    | yes, no                      |
| `description` | String            | False    | False    | Network Interface to attach. |
| `example`     | String            | False    | False    | 10s                          |

[^2] possible values: "integer", "number", "time-duration", "string", "choice", "boolean", and "binary".

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided.
  It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.

## Create

To create a new agent in the catalog use the following REST call:

**POST** /_catalog_ /_ebpf-program_

with the request body (in JSON format):

```json
{
    "id": "{ebpf_program_name}",
    "parameters": [
        {
            "id": "{parameter_name}",
            "type": "{parameter_type}",
            "example": "{parameter_example}",
            "description": "{parameter_human_readable_description}",
            "config": {
                "schema": "{parameter_schema}",
                "source": "{parameter_source}",
                "path": [
                    "{parameter_path}"
                ]
            }
        }
    ],
    "actions": [
        {
            "id": "{action_name}",
            "status": "{action_status}",
            "config": {
                "cmd": "{action_cmd}"
            }
        }
    ]
}
```

Replace the data with the correct values, for example `agent_name` with `nprobe`.
It is possible to add additional data specific for this agent.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "Agent Catalog with the given [id] correctly created.",
        "data": {
            "id": "{agent_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an agent with the given `id` is already found in the catalog, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Agent Catalog with the given [id] already found",
        "data": {
            "id": "{agent_name}",
            ...
        },
        "http_status_code": 409
    }
]
```

If some required data is missing (for example `type` of one `parameter`), the response could be:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "Not possible to create a Agent Catalog with the given [data]",
        "exception": "{'parameter.type': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{agent_name}",
            ...
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of the agents available in the catalog:

**GET** /_catalog_/_agent_

The response includes all the agents.

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

In this way, it will be returned only the `parameters` of the agent in the catalog with `id` = "_`{agent_name}`_"

## Update

To update an agent in the catalog, use:

**PUT** /_catalog_/_agent_

```json
{
    "id": "{agent_name}",
    "parameters": [
        {
            "id": "{parameter_name}",
            "type": "{new_parameter_type}"
        }
    ],
    "actions": [
        {
            "id": "{new_agent_action}",
            "config": {
                "cmd": "{new_action_cmd}"
            }
        }
    ]
}
```

This example

1. updates the new `type` of the `paramter` with `id` = "_`{parameter_name}`_";
2. adds a new action

of the agent with `id` = `agent_name`.

Also during the update it is possible to add additional data (not related to actions or parameters)
for the specific agent.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "Agent Catalog with the given [id] correctly updated.",
        "data": {
            "id": "{agent_name}",
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
        "description": "Agent Catalog with the given [id] not updated.",
        "data": {
            "id": "{agent_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a agent from the catalog, use:

**DELETE** /_catalog_/_agent_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{agent_name}"
        }
    }
}
```

This request removes from the catalog the agent with `id` = "_`{agent_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "Agent Catalog with the given [id] correctly deleted.",
        "data": {
            "id": "{agent_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the agent from the catalog.

## Loaded data

For the demo, this data is already available:

- [firewall](agent_catalog-firewall.json)
- [nprobe](agent_catalog-nprobe.json)
