# Context Broker APIs

## Table of Contents

* [Data Model](#data-model)
    * [Methods](#methods)
        * [Execution Environment](#execution-environment)
        * [Execution Environment Type](#execution-environment-type)
        * [Network Link](#network-link)
        * [Network Link Type](#network-link-type)
        * [Connection](#connection)
        * [Catalog](#catalog)
        * [Data Collection](#data-collection)
        * [Full Query](#full-query)
* [Installation](#installation)
* [Usage](#usage)
* [References](#references)

# Data Model

![Data Model](data_model.png)

Each table in the figure represents an index in the Elastic nomenclature. Considering the NoSQL nature of the Elasticsearch engine for each document of any indices it is possible to add additional properties. The schema is not static and defined at priori, but it is dynamic allowing the possibility to add custom properties for a specific document.

The Data index contains the all the data collected from the Execution Environments (ExEnvs) by means of the agent[^1]. The common attributes are:

1. id (unique identifier)[^2];
2. id of the source execution environment; and 
3. id of the agent that collect the data.

Then, the other two properties are related to the time-stamp:

1. timestamp when event is occurred; and
2. timestamp-agent when the agent collect the data.

The ExecEnv index contains the host-name of the remote host where is it allocated and the list of agent IDs that are available in that ExEnv. In addition, it contain the type field that correspond a specified type of ExEnv. The different type of execution environment are defined with the index ExecEnvType. Currently, the available types are: *i*) *Virtual Machine* and *ii*) *Container*. Obviously, it is possible to add other types depending on the specific requirements. Finally, the ExeEnvs could contain the information regarding the installed software. The field software contains the list of IDs of the sofware defined with the index Software. This part is not out of scope of the ASTRID project context and, for this reason, in Figure 4, it is this highlighted with a dashed box. The API implementation, that will be described in the next sections, does not consider the software index. Nervelessness, this example represent a typical solution for various common cases. The proposed data model allows the customization with the integration of additional entities in very simple way.

The Agent index contains specific information related to the agents, and in particular the Beats of the Elastic stack. For a detailed description of these properties see [1].

In addition, the data model allow to see the status of the connections between the execution environments. The Connection index couples the ExEnv and network link to which it belongs. This index should contains all the information regarding the network link and the ExEnv as, for example, the IP address (version 4 and/or 6) or if the link is encrypted and how (which method, etc.).

The network links are defined with the relative index where it indicated the type. All the possible network link types are defined in the NetworkLinkType index. At the moment, the possible types are: Point to Point (Point 2 Point), Multi-point, and Slice.

[^1]: In the reference architecture the agents are Beats from Elastic Stack. Notwithstanding, the data model refers to a generic agent allowing to possibility to use different types.

[^2]: In Elasticsearch, each document is identified by a unique id. For obvious reasons, in the description of the following indices, we omit the description of all the id fields.

## Methods

### Execution Environment

**HTTP Method** | **Path**                | **Action**
--------------- | ----------------------- | ----------------------------------
GET             | /config/exec-env-id     | Returns all ExEnv IDs.
GET             | /config/exec-env        | Returns all ExEnvs.
GET             | /config/exec-env/{*id*} | Returns the ExEnv with ID {*id*}.
POST            | /config/exec-env        | Create a new ExEnv.
PUT             | /config/exec-env/{*id*} | Update the ExEnv with ID {*id*}.
DELETE          | /config/exec-env/{*id*} | Delete the ExEnv with ID {*id*}.

### Execution Environment Type

**HTTP Method** | **Path**                     | **Action**
--------------- | ---------------------------- | --------------------------------------
GET             | /config/exec-env-type-id     | Returns all ExEnv Type IDs.
GET             | /config/exec-env-type        | Returns all ExEnv Types.
GET             | /config/exec-env-type/{*id*} | Returns the ExEnv Type with ID {*id*}.
POST            | /config/exec-env-type        | Create a new ExEnv Type.
PUT             | /config/exec-env-type/{*id*} | Update the ExEnv with ID {*id*}.
DELETE          | /config/exec-env-type/{*id*} | Delete the ExEnv with ID {*id*}.

#### Network Link

**HTTP Method** | **Path**                      | **Action**
--------------- | ----------------------------- | ----------------------------------------
GET             | /config/network-link-id       | Returns all Network Link IDs.
GET             | /config/network-link          | Returns all Network Links.
GET             | /config/network-link/{*id*}   | Returns the Network Link with ID {*id*}.
POST            | /config/network-link          | Create a new Network Link.
PUT             | /config/network-link/{*id*}   | Update the Network Link with ID {*id*}.
DELETE          | /config/network-link/{*id*}   | Delete the Network Link with ID {*id*}.

#### Network Link Type

**HTTP Method** | **Path**                         | **Action**
--------------- | -------------------------------- | ---------------------------------------------
GET             | /config/network-link-type-id     | Returns all Network Link Type IDs.
GET             | /config/network-link-type        | Returns all Network Link Types.
GET             | /config/network-link-type/{*id*} | Returns the Network Link Type with ID {*id*}.
POST            | /config/network-link-type        | Create a new Network Link Type.
PUT             | /config/network-link-type/{*id*} | Update the Network Link Type with ID {*id*}.
DELETE          | /config/network-link-type/{*id*} | Delete the Network Link Type with ID {*id*}.

#### Connection

**HTTP Method** | **Path**                                  | **Action**
--------------- | ----------------------------------------- | ---------------------------------------------------------------------------
GET             | /config/connection-id                     | Returns all Connection IDs.
GET             | /config/connection-id/exec-env/{*id*}     | Returns all Connection IDs filtered by the Execution Environment ID {*id*}.
GET             | /config/connection-id/network-link/{*id*} | Returns all Connection IDs filtered by the Network Link ID {*id*}.
GET             | /config/connection                        | Returns all Connections.
GET             | /config/connection/{*id*}                 | Returns the Connection with ID {*id*}.
GET             | /config/connection/exec-env/{*id*}        | Returns all Connection filtered by the Execution Environment ID {*id*}.
GET             | /config/connection/network-link/{*id*}    | Returns all Connections filtered by the Network Link ID {*id*}.
POST            | /config/connection                        | Create a new Connection.
PUT             | /config/connection/{*id*}                 | Update the Connection with ID {*id*}.
DELETE          | /config/connection/{*id*}                 | Delete the Connection with ID {*id*}.
DELETE          | /config/connection/exec-env/{*id*}        | Delete the Connections filtered by the Execution Environment ID {*id*}.
DELETE          | /config/connection/network-link/{*id*}    | Delete the Connections filtered by the Network Link ID {*id*}.

### Catalog

**HTTP Method** | **Path**              | **Action**
--------------- | --------------------- | ----------------------------------
GET             | /catalog/agent-id     | Returns all Agent IDs.
GET             | /catalog/agent        | Returns all Agents.
GET             | /catalog/agent/{*id*} | Returns the Agent with ID {*id*}.
POST            | /catalog/agent        | Create a new Agent.
PUT             | /catalog/agent/{*id*} | Update the Agent with ID {*id*}.
DELETE          | /catalog/agent/{*id*} | Delete the Agent with ID {*id*}.

### Data Collection

**HTTP Method** | **Path**                             | **Action**
--------------- | ------------------------------------ | -----------------------------------------------------------------------
POST            | /data                                | Returns the collected data filtered by the query in the request body.
GET             | /data/exec-env/{*id*}                | Returns the collected data filtered by the Execution Environment {*id*}.
GET             | /data/agent/{*id*}                   | Returns the collected data filtered by the Agent {*id*}.
GET             | /data/timestamp/after/{*after*}      | Returns the data collected after {*after*}.
GET             | /data/timestamp/before/{*before*}    | Returns the data collected before {*before*}.
GET             | /data/timestamp/{*after*}/{*before*} | Returns the data collected in the period between {*after*} and {*before*}.

#### Full Query

**HTTP Method** | **Path**          | **Action**
--------------- | ----------------- | ---------------------------------------------------------------------------------------------------|
POST            | /data/elastic-dsl | Returns the collected data filtered by the query in the request body using the [Elastic DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html) syntax.
POST            | /data/graph-ql    | Returns the collected data filtered by the query in the request body using the [GraphQL](https://graphql.org) syntax.

# Installation

1. Prerequisite

- python3
- pip3

2. Clone the repository.

```bash
git clone https://gitlab.com/astrid-repositories/wp2/context-broker-apis.git
```

3. Install the dipendence.

```bash
pip3 install -r requirements.txt
```

# Usage

```bash
python3 context_broker-rest-api.py -h
```

# ToDo

[] Error if id included in body request for create or update.
[] Complete Swagger API generator adding missing part in the code.
[] Fix error in data model for Swagger API generation.
[] Add docstring to code for API code generation. 

# References

[1] “Getting started with Beats,” [Online]. Available: https://www.elastic.co/guide/en/beats/libbeat/current/getting-started.html.
