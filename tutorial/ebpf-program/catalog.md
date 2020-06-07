# eBPF Program Catalog

Contains the available eBPF programs to be installed in the [execution environments](../exec-env/README.md).

- [eBPF Program Catalog](#ebpf-program-catalog)
  - [Schema](#schema)
    - [Config Schema](#config-schema)
      - [Metric Schema](#metric-schema)
      - [Open Metrics Metadata Schema](#open-metrics-metadata-schema)
      - [Open Metrics Metadata Label Schema](#open-metrics-metadata-label-schema)
    - [Parameter Schema](#parameter-schema)
  - [Create](#create)
  - [Read](#read)
  - [Update](#update)
  - [Delete](#delete)

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

| Field     | Type         | Required | Readonly | Example |
| --------- | ------------ | -------- | -------- | ------- |
| `code`    | String       | True     | False    |         |
| `metrics` | List(Metric) | False    | False    |         |

#### Metric Schema

| Field                   | Type                      | Required | Readonly | Example       |
| ----------------------- | ------------------------- | -------- | -------- | ------------- |
| `name`                  | String                    | True     | False    | packets_total |
| `map_name`              | String                    | True     | False    | PKT_COUNTER   |
| `open_metrics_metadata` | List(OpenMetricsMetadata) | False    | False    |               |

#### Open Metrics Metadata Schema

| Field    | Type                           | Required | Readonly | Example |
| -------- | ------------------------------ | -------- | -------- | ------- |
| `type`   | String                         | True     | False    | counter |
| `help`   | String                         | False    | False    | [^2]    |
| `labels` | List(OpenMetricsMetadataLabel) | False    | False    |         |

[^2]: This metric represents the number of packets that has traveled trough this probe.

#### Open Metrics Metadata Label Schema

| Field   | Type   | Required | Readonly | Example  |
| ------- | ------ | -------- | -------- | -------- |
| `name`  | String | True     | False    | IP_PROTO |
| `value` | String | True     | False    | UPD      |

### Parameter Schema

| Field         | Type              | Required | Readonly | Example                      |
| ------------- | ----------------- | -------- | -------- | ---------------------------- |
| `id`          | String            | True     | True     | start                        |
| `type`        | Enum(String) [^3] | True     | False    | integer                      |
| `list`        | Boolean           | False    | False    | False                        |
| `values`      | Enum(String)      | False    | False    | yes, no                      |
| `description` | String            | False    | False    | Network Interface to attach. |
| `example`     | String            | False    | False    | 10s                          |

[^3]: Possible values are "integer", "number", "time-duration", "string", "choice", "boolean", and "binary".

Note:

- It is not possible to update readonly fields.
- `id` is required but it is auto-generated if not provided.
  It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.

## Create

To create a new eBPF program in the catalog use the following REST call:

**POST** /_catalog_/_ebpf-program_

with the request body (in JSON format):

```json
{
    "id": "{ebpf_program_name}",
    "config": {
        "code": "{source_code}",
        "metrics": [{
            "name": "{metric_name}",
            "map-name": "{map_name}",
            "open-metrics-metadata": {
                "type": "{metric_type}",
                "help": "{metric_help}",
                "labels": [{
                        "name": "{label_name}",
                        "value": "{label_Value}"
                }]
            }
        }]
    },
    "parameters": [
        {
            "id": "{parameter_name}",
            "type": "{parameter_type}",
            "example": "{parameter_example}",
            "description": "{parameter_human_readable_description}"
        }
    ]
}
```

Replace the data with the correct values, for example `ebpf_program_name` with `nprobe`.
It is possible to add additional data specific for this eBPF program.

If the creation is correctly executed the response is:

```json
[
    {
        "status": "created",
        "description": "eBPF Program Catalog with the given [id] correctly created.",
        "data": {
            "id": "{ebpf_program_name}",
            ...
        },
        "http_status_code": 201
    }
]
```

Otherwise, if, for example, an eBPF Program with the given `id` is already found in the catalog, this is the response:

```json
[
    {
        "status": "error",
        "error": true,
        "description": "eBPF Program Catalog with the given [id] already found",
        "data": {
            "id": "{ebpf_program_name}",
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
        "description": "Not possible to create a eBPF Program Catalog with the given [data]",
        "exception": "{'parameter.type': [ValidationException('Value required for this field.')]}",
        "data": {
            "id": "{ebpf_program_name}",
            ...
        },
        "http_status_code": 422
    }
]
```

## Read

To get the list of the eBPF programs available in the catalog:

**GET** /_catalog_/_ebpf-program_

The response includes all the eBPF programs.

It is possible to filter the results using the following request body:

```json
{
    "select": ["parameters"],
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{ebpf_program_name}"
        }
    }
}
```

In this way, it will be returned only the `parameters` of the eBPF program in the catalog
with `id` = "_`{ebpf_program_name}`_"

## Update

To update an eBPF program in the catalog, use:

**PUT** /_catalog_/_ebpf-program_

```json
{
    "id": "{ebpf_program_name}",
    "parameters": [
        {
            "id": "{parameter_name}",
            "type": "{new_parameter_type}"
        }
    ]
}
```

This example updates the new `type` of the `parameter` with
`id` = "_`{parameter_name}`_" of the agent with `id` = `agent_name`.

Also during the update it is possible to add additional data (not related to parameters)
for the specific eBPF program.

A possible response is:

```json
[
    {
        "status": "updated",
        "description": "eBPF Program Catalog with the given [id] correctly updated.",
        "data": {
            "id": "{ebpf_program_name}",
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
        "description": "eBPF Program Catalog with the given [id] not updated.",
        "data": {
            "id": "{ebpf_program_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

## Delete

To delete a eBPF program from the catalog, use:

**DELETE** /_catalog_/_ebpf-program_

```json
{
    "where": {
        "equals": {
            "target:" "id",
            "expr": "{ebpf_program_name}"
        }
    }
}
```

This request removes from the catalog the eBPF program with `id` = "_`{ebpf_program_name}`_".

This is a possible response:

```json
[
    {
        "status": "deleted",
        "description": "eBPF Program Catalog with the given [id] correctly deleted.",
        "data": {
            "id": "{ebpf_program_name}",
            ...
        },
        "http_status_code": 200
    }
]
```

NOTE: Without request body, it removes **all** the eBPF programs from the catalog.
