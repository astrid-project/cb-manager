# Context Broker APIs

## Table of Contents

* [Terminology](#terminology)
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
* [Coming Soon](#coming-soon)
* [References](#references)

# Terminology

**Term**     | **Meaning**
:----------: | ---------------------
*ACL*        | Access Control List
*API*        | Application Program Interface
*BA*         | Basic Authentication
*BPF*        | Berkeley Packet Filter
*CB*         | Context Broker
*CRUD*       | Create - Read - Update - Delete
*eBPF*       | extended BPF
*ELK*        | Elastic - LogStash - Kibana
ExecEnv    | Execution Environment
*HOBA*       | HTTP Origin-Bound Authentication
*HTTP*       | Hyper Text Transfer Protocol
*ID*         | Identification
*IP*         | Internet Protocol
*LDAP*       | Lightweight Directory Access Protocol
*JSON*       | Java Object Notation
*RBAC*       | Role-Based Access Control
*regex*      | regular expression
*RFC*        | Request For Comments
*SCM*        | Security Context Model
*SLA*        | Service Level Agreements
*YANG*       | Yet Another Next Generation

# Data Model

![Data Model](data_model.png)

Each table in the figure represents an *index* in the Elastic nomenclature. Considering the *NoSQL* nature of the Elasticsearch engine for each document of any indices it is possible to add additional properties. The schema is not static and defined at priori, but it is dynamic allowing the possibility to add custom properties for a specific document. Elastic requires the name of the index in a lowercase format. For this reason, all the index names follow the *dash-case*[^1] format. Instead, each properties[^2] follow the *snake-case*[^3] format.

The *data* index contains the all the data collected from the ExecEnvs by means of the agent[^4]. The common attributes are:

1. *id* (unique identifier)[^5];
2. *id* of the source ExecEnv (*exec_env_id*); and 
3. *id* of the agent instance that collect the data (*agent_instance_id*).

The ID property type accepts only lowercase values without space that start with an alphabetic character, e.g: apache is valid but not Apache.

Then, the other two properties are related to the time-stamp:

1. *timestamp-event* when event is occurred; and
2. *timestamp-agent* when the agent collect the data.

The concept of the agent instance will be described in detail in the following sections. For now, it is sufficient to note that, with agent instance, we refer to specific agent installed in the ExecEnv.

The *exec-env* index contains the *hostname* of the remote host where is it allocated and the *type_id* field that correspond a specified type of ExecEnv. The different type of ExecEnv are defined with the index *exec-env-type*. Currently, the available types are: *i*) *Virtual Machine* and *ii*) *Container*. Obviously, it is possible to add other types depending on the specific requirements.

The *agent-catalog* index contains specific information related to the agents, and in particular the Beats of the Elastic stack and specific application deployed with the PolyCube framework. For a detailed description of these properties see [3] and [4]. Instead, the *agent-instance* index contains the properties and configurations related to the agents currently installed on the ExecEnvs.

The network links are defined with the relative index where it indicated the type. All the possible network link types are defined in the *nettwork-link-type* index. At the moment, the possible types are: *Point to Point* (Point 2 Point), *Multi-point*, and *Slice*. Similar to the ExecEnv case, also for the network link, it is possible to add additional types depending on specific needs.

In addition, the data model allow to see the status of the connections between the execution environments. The *connection* index couples the ExecEnv and network link to which it belongs. This index should contains all the information regarding the network link and the ExecEnv as, for example, the IP address (version 4 and/or 6) or if the link is encrypted and how (which method, etc.).

The *software* index contains the installed software with relative properties. Each software record is referred to a specific ExecEnv that indicate where the software is installed. This part is out of scope of the ASTRID project context and, for this reason, in the above figure, it is this highlighted with a dashed box. The API implementation, that will be described in the next sections, does not consider this index. Nervelessness, it represents a typical solution for various common cases. The proposed data model allows the customization with the integration of additional entities in very simple way.

[^1]: In the dash-case (also referred as *hyphen-case* or *kebab-case*) format all the letters are lower-case, the punctuation is not allowed and the words are separated by single dash (or hyphen: -). Example: *exec-env*.

[^2]: We use the terms properties, fields and attributes interchangeably.

[^3]: In the snake-case format all the letters are lower-case, the punctuation is not allowed and the words are separated by single underscore (_). Example: *exec_env_id*.

[^4]: In our architecture the agents are Beats from Elastic Stack. Notwithstanding, the data model refers to a generic agent allowing to possibility to use different types.

[^5]: In Elasticsearch, each document is identified by a unique id. For obvious reasons, in the description of the following indices, we omit the description of all the id fields.

## Methods

### ExecEnv

**HTTP Method** | **Path**                | **Action**
:-------------: | ----------------------- | ----------------------------------
GET             | /config/exec-env-id     | Returns all ExecEnv IDs.
GET             | /config/exec-env        | Returns all ExecEnvs.
GET             | /config/exec-env/{*id*} | Returns the ExecEnv with id = {*id*}.
POST            | /config/exec-env        | Create a new ExecEnv.
PUT             | /config/exec-env/{*id*} | Update the ExecEnv with id = {*id*}.
DELETE          | /config/exec-env/{*id*} | Delete the ExecEnv with id = {*id*}.

### ExecEnv type

**HTTP Method** | **Path**                     | **Action**
:-------------: | ---------------------------- | --------------------------------------
GET             | /config/exec-env-type-id     | Returns all ExecEnv type IDs.
GET             | /config/exec-env-type        | Returns all ExecEnv types.
GET             | /config/exec-env-type/{*id*} | Returns the ExecEnv type with id = {*id*}.
POST            | /config/exec-env-type        | Create a new ExecEnv type.
PUT             | /config/exec-env-type/{*id*} | Update the ExecEnv with id = {*id*}.
DELETE          | /config/exec-env-type/{*id*} | Delete the ExecEnv with id = {*id*}.

#### Network link

**HTTP Method** | **Path**                      | **Action**
:-------------: | ----------------------------- | ----------------------------------------
GET             | /config/network-link-id       | Returns all network link IDs.
GET             | /config/network-link          | Returns all network links.
GET             | /config/network-link/{*id*}   | Returns the network link with id = {*id*}.
POST            | /config/network-link          | Create a new network link.
PUT             | /config/network-link/{*id*}   | Update the network link with id = {*id*}.
DELETE          | /config/network-link/{*id*}   | Delete the network link with id = {*id*}.

#### Network link type

**HTTP Method** | **Path**                         | **Action**
:-------------: | -------------------------------- | ---------------------------------------------
GET             | /config/network-link-type-id     | Returns all network link type IDs.
GET             | /config/network-link-type        | Returns all network link types.
GET             | /config/network-link-type/{*id*} | Returns the network link type with id = {*id*}.
POST            | /config/network-link-type        | Create a new network link type.
PUT             | /config/network-link-type/{*id*} | Update the network link type with id = {*id*}.
DELETE          | /config/network-link-type/{*id*} | Delete the network link type with id = {*id*}.

#### Connection

**HTTP Method** | **Path**                                  | **Action**
:-------------: | ----------------------------------------- | ---------------------------------------------------------------------------
GET             | /config/connection-id                     | Returns all connection IDs.
GET             | /config/connection-id/exec-env/{*id*}     | Returns all connection IDs filtered by the ExecEnv with id = {*id*}.
GET             | /config/connection-id/network-link/{*id*} | Returns all connection IDs filtered by the network link ID {*id*}.
GET             | /config/connection                        | Returns all connections.
GET             | /config/connection/{*id*}                 | Returns the connection with id = {*id*}.
GET             | /config/connection/exec-env/{*id*}        | Returns all connection filtered by the ExecEnv ID {*id*}.
GET             | /config/connection/network-link/{*id*}    | Returns all connections filtered by the network link ID {*id*}.
POST            | /config/connection                        | Create a new connection.
PUT             | /config/connection/{*id*}                 | Update the connection with id = {*id*}.
DELETE          | /config/connection/{*id*}                 | Delete the connection with id = {*id*}.
DELETE          | /config/connection/exec-env/{*id*}        | Delete the connections filtered by the ExecEnv ID {*id*}.
DELETE          | /config/connection/network-link/{*id*}    | Delete the connections filtered by the network link ID {*id*}.

### Catalog

**HTTP Method** | **Path**              | **Action**
:-------------: | --------------------- | ----------------------------------
GET             | /catalog/agent-id     | Returns all agent IDs available in the catalog.
GET             | /catalog/agent        | Returns all agents available in the catalog.
GET             | /catalog/agent/{*id*} | Returns the agent in the catalog with id = {id}.
POST            | /catalog/agent        | Create a new agent in the catalog.
PUT             | /catalog/agent/{*id*} | Update the agent with id = {id} in catalog.
DELETE          | /catalog/agent/{*id*} | Delete the agent with id = {id} in catalog.

### Data Collection

**HTTP Method** | **Path**                                   | **Action**
:-------------: | ------------------------------------------ | -----------------------------------------------------------------------
POST            | /data                                      | Returns the collected data filtered by the query in the request body.
GET             | /data/exec-env/{*id*}                      | Returns the collected data filtered by the ExecEnv with id = {*id*}.
GET             | /data/agent/instance/{*id*}                | Returns the collected data filtered by the agent instance with id = {*id*}.
GET             | /data/agent/instance/{*id*}                | Returns the collected data filtered by the agent with id = {*id*} in the Catalog.
GET             | /data/timestamp/event/after/{*after*}      | Returns the collected data with event occurred after {*after*}.
GET             | /data/timestamp/event/before/{*before*}    | Returns the collected data with event occurred before {*before*}.
GET             | /data/timestamp/event/{*after*}/{*before*} | Returns the collected data with event occurred in the period between {*after*} and {*before*}.
GET             | /data/timestamp/agent/after/{*after*}      | Returns the data collected by the agent after {*after*}.
GET             | /data/timestamp/agent/before/{*before*}    | Returns the data collected by the agent before {*before*}.
GET             | /data/timestamp/agent/{*after*}/{*before*} | Returns the data collected by the agent in the period between {*after*} and {*before*}.

#### Full Query

**HTTP Method** | **Path**          | **Action**
:-------------: | ----------------- | ---------------------------------------------------------------------------------------------------|
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

# Coming soon

[ ] Error if id included in body request for create or update.
[ ] Complete Swagger API generator adding missing part in the code.
[ ] Fix error in data model for Swagger API generation.
[ ] Add docstring to code for API code generation. 

# References

[1] “Getting started with Beats,” [Online]. Available: https://www.elastic.co/guide/en/beats/libbeat/current/getting-started.html.
