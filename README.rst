Context Broker Manager
======================

APIs to interact with the ``Context Broker``'s database. Through a |REST| Interface, it exposes data and events stored
in the internal storage system in a structured way. It provides uniform access to the capabilities of monitoring agents.

.. toctree::
   :maxdepth: 2
   :numbered:

Data Model
----------

.. image:: data_model.png

Each table in the figure represents an **index** in the Elastic nomenclature.
Considering the **NoSQL** nature of the Elasticsearch engine for each document of any indices it is possible to add
additional properties.
The schema is not static and defined at priori, but it is dynamic allowing the possibility to add custom properties for a
specific document. Elastic requires the name of the index in a lower-case format.
For this reason, all the index names follow the *dash-case* [1]_ format.
Instead, each property [2]_ follows the *snake-case* [3]_ format.
All the properties marked with an asterisk (*) are required by the |APIs| in order to make the POST request
(i.e. to create a new resource, for example an Exec_Env). Instead the ones underlined are identifies the specific
resource (aka document in Elastic nomenclature or record in traditional |DB| one) and must be unique.
The ``data`` index contains the all the data collected from the Exec_Envs by means of the agent [4]_.

The common attributes are:

1. ``id`` (unique identifier) [5]_;
2. ``id`` of the source Exec_Env (``exec_env_id``); and
3. ``id`` of the agent instance that collect the data (``agent_instance_id``).

The ``id`` property type accepts only lower-case values without space that start with an alphabetic character,
e.g: apache is valid but not Apache.
Then, the other two properties are related to the time-stamp:

1. ``timestamp_event`` when event is occurred; and
2. ``timestamp_agent`` when the agent instance collect the data.

With the term agent instance, we refer to a specific agent installed in the Exec_Env.

The ``exec-env`` index contains the ``hostname`` of the remote host where is it allocated and the ``type_id`` field
that correspond a specified type of Exec_Env. The different type of Exec_Env are defined with the index ``exec-env-type``.
Currently, the available ones are: *i*) *Virtual Machine* and *ii*) *Container*.
Obviously, it is possible to add other types depending on the specific requirements.

The ``agent-catalog`` index contains specific information related to the agents, and in particular the Beats of the
Elastic stack and eBPF-based services deployed with the **Polycube** framework. For a detailed description of these
properties see [6]_ and [7]_.

Each agent in the catalog is characterized by one or more options.
The options are defined with the `agent-option` *nested-index* [8]_. This index described the option in terms of name and
relative type. At this moment, the supported types are:

- *integer* (e.g. 1, 2, etc.);
- *number* (e..g 1, 2.3, etc.);
- *time-duration* (e.g. 1s, 2m, 3h, etc.);
- *string*; *choice*, *obj*, and *boolean* (i.e. true or false).

There two additional (and optional) properties: *list* and *values*. The first one indicate if the option is a
list or not (default value: false); while the latter one described the data in the case the type is choice or obj.
To accept different types, the values property can be of any type.

All the data of the installed agent is stored in the ``agent-instance`` index.
This index contains the options got from the catalog with the actual values.
In addition, it includes the ``id`` of the Exec_Env where the agent is installed (``exec_env_id``) and
the current *status* in terms of *started* or *stopped*.

The network links are defined with the relative index where it is indicate the type.
All the possible network link types are defined in the ``network-link-type`` index.
At the moment, the possible types are: *Point to Point* (Point 2 Point), *Multi-point*, and *Slice*.
Similar to the Exec_Env case, also for the network link, it is possible to add additional types
depending on specific needs.

In addition, the data model allow to see the status of the connections between the Exec_Envs.
The ``connection`` index couples the Exec_Env and the network link to which it belongs.
This index should contains all the information regarding the network link and the Exec_Env as, for example,
the |IP| address (version 4 and/or 6) or if the link is encrypted and how (which method, etc.).

The ``software`` index contains the installed software with relative properties.
Each software record is referred to a specific Exec_Env that indicate where the software is installed.
This part is out of scope of the |ASTRID| project context and, for this reason, it is this highlighted with a dashed box.
The |API| implementation does not consider this index. Nervelessness, it represents a typical solution for various
common cases. The proposed data model allows the customization with the integration of additional entities in very
simple way.

Methods
-------

Exec_Env
^^^^^^^^

+---------------+-----------------------+-----------------------------------------------------------------+
| |HTTP| Method | Path                  | Action                                                          |
+===============+=======================+=================================================================+
| GET           | /exec-env             | Returns the Exec_Envs selected by the query in the request body |
|               |                       | (or all it the request body is empty).                          |
|               +-----------------------+-----------------------------------------------------------------+
|               | /exec-env/(string:id) | Returns the Exec_Env selected by the given ``id``               |
|               |                       | and the query in the request body.                              |
+---------------+-----------------------+-----------------------------------------------------------------+
| POST          | /exec-env             | Create one or more new Exec_Envs.                               |
|               +-----------------------+-----------------------------------------------------------------+
|               | /exec-env/(string:id) | Create a new Exec_Env with the given ``id``.                    |
+---------------+-----------------------+-----------------------------------------------------------------+
| PUT           | /exec-env             | Update one or more existing Exec_Envs.                          |
|               +-----------------------+-----------------------------------------------------------------+
|               | /exec-env/(string:id) | Update the Exec_Env with given ``id``.                          |
+---------------+-----------------------+-----------------------------------------------------------------+
| DELETE        | /exec-env             | Delete the Exec_Envs selected by the query in the request body  |
|               |                       | (or all it the request body is empty).                          |
|               +-----------------------+-----------------------------------------------------------------+
|               | /exec-env/(string:id) | Delete the Exec_Env selected by the given ``id``                |
|               |                       | and the query in the request body.                              |
+---------------+-----------------------+-----------------------------------------------------------------+


Exec_Env Type
+++++++++++++

+---------------+----------------------------+----------------------------------------------------------------------+
| |HTTP| Method | Path                       | Action                                                               |
+===============+============================+======================================================================+
| GET           | /type/exec-env             | Returns the Exec_Env types selected by the query in the request body |
|               |                            | (or all it the request body is empty).                               |
|               +----------------------------+----------------------------------------------------------------------+
|               | /type/exec-env/(string:id) | Returns the Exec_Env type selected by the given ``id``               |
|               |                            | and the query in the request body.                                   |
+---------------+----------------------------+----------------------------------------------------------------------+
| POST          | /type/exec-env             | Create one or more new Exec_Env types.                               |
|               +-----------------------+---------------------------------------------------------------------------+
|               | /type/exec-env/(string:id) | Create a new Exec_Env with the given ``id``.                         |
+---------------+----------------------------+----------------------------------------------------------------------+
| PUT           | /type/exec-env             | Update one or more existing Exec_Env types.                          |
|               +-----------------------+---------------------------------------------------------------------------+
|               | /type/exec-env/(string:id) | Update the Exec_Env type with given ``id``.                          |
+---------------+-----------------------+---------------------------------------------------------------------------+
| DELETE        | /type/exec-env             | Delete the Exec_Env types selected by the query in the request body  |
|               |                            | (or all it the request body is empty).                               |
|               +-----------------------+---------------------------------------------------------------------------+
|               | /type/exec-env/(string:id) | Delete the Exec_Env type selected by the given ``id``                |
|               |                            | and the query in the request body.                                   |
+---------------+----------------------------+----------------------------------------------------------------------+


Network link
^^^^^^^^^^^^

+---------------+---------------------------+---------------------------------------------------------------------+
| |HTTP| Method | Path                      | Action                                                              |
+===============+===========================+=====================================================================+
| GET           | /network-link             | Returns the network links selected by the query in the request body |
|               |                           | (or all it the request body is empty).                              |
|               +---------------------------+---------------------------------------------------------------------+
|               | /network-link/(string:id) | Returns the network link selected by the given ``id``               |
|               |                           | and the query in the request body.                                  |
+---------------+---------------------------+---------------------------------------------------------------------+
| POST          | /network-link             | Create one or more new network links.                               |
|               +---------------------------+---------------------------------------------------------------------+
|               | /network-link/(string:id) | Create a new network link with the given ``id``.                    |
+---------------+---------------------------+---------------------------------------------------------------------+
| PUT           | /network-link             | Update one or more existing network links.                          |
|               +---------------------------+---------------------------------------------------------------------+
|               | /network-link/(string:id) | Update the network link with given ``id``.                          |
+---------------+---------------------------+---------------------------------------------------------------------+
| DELETE        | /network-link             | Delete the network links selected by the query in the request body  |
|               |                           | (or all it the request body is empty).                              |
|               +---------------------------+---------------------------------------------------------------------+
|               | /network-link/(string:id) | Delete the network link selected by the given ``id``                |
|               |                           | and the query in the request body.                                  |
+---------------+---------------------------+---------------------------------------------------------------------+


Network link Type
+++++++++++++++++

+---------------+--------------------------------+--------------------------------------------------------------------------+
| |HTTP| Method | Path                           | Action                                                                   |
+===============+================================+==========================================================================+
| GET           | /type/network-link             | Returns the network link types selected by the query in the request body |
|               |                                | (or all it the request body is empty).                                   |
|               +--------------------------------+--------------------------------------------------------------------------+
|               | /type/network-link/(string:id) | Returns the network link type selected by the given ``id``               |
|               |                                | and the query in the request body.                                       |
+---------------+--------------------------------+--------------------------------------------------------------------------+
| POST          | /type/network-link             | Create one or more new network link types.                               |
|               +--------------------------------+--------------------------------------------------------------------------+
|               | /type/network-link/(string:id) | Create a new network link type with the given ``id``.                    |
+---------------+--------------------------------+--------------------------------------------------------------------------+
| PUT           | /type/network-link             | Update one or more existing network link types.                          |
|               +--------------------------------+--------------------------------------------------------------------------+
|               | /type/network-link/(string:id) | Update the network link type with given ``id``.                          |
+---------------+--------------------------------+--------------------------------------------------------------------------+
| DELETE        | /type/network-link             | Delete the network link types selected by the query in the request body  |
|               |                                | (or all it the request body is empty).                                   |
|               +--------------------------------+--------------------------------------------------------------------------+
|               | /type/network-link/(string:id) | Delete the network link type selected by the given ``id``                |
|               |                                | and the query in the request body.                                       |
+---------------+--------------------------------+--------------------------------------------------------------------------+


Connection
^^^^^^^^^^

+---------------+-------------------------+-------------------------------------------------------------------+
| |HTTP| Method | Path                    | Action                                                            |
+===============+=========================+===================================================================+
| GET           | /connection             | Returns the connections selected by the query in the request body |
|               |                         | (or all it the request body is empty).                            |
|               +-------------------------+-------------------------------------------------------------------+
|               | /connection/(string:id) | Returns the connection selected by the given ``id``               |
|               |                         | and the query in the request body.                                |
+---------------+-------------------------+-------------------------------------------------------------------+
| POST          | /connection             | Create one or more new connections.                               |
|               +-------------------------+-------------------------------------------------------------------+
|               | /connection/(string:id) | Create a new connection with the given ``id``.                    |
+---------------+-------------------------+-------------------------------------------------------------------+
| PUT           | /connection             | Update one or more existing connections.                          |
|               +-------------------------+-------------------------------------------------------------------+
|               | /connection/(string:id) | Update the connection with given ``id``.                          |
+---------------+-------------------------+-------------------------------------------------------------------+
| DELETE        | /connection             | Delete the connections selected by the query in the request body  |
|               |                         | (or all it the request body is empty).                            |
|               +-------------------------+-------------------------------------------------------------------+
|               | /connection/(string:id) | Delete the connection selected by the given ``id``                |
|               |                         | and the query in the request body.                                |
+---------------+-------------------------+-------------------------------------------------------------------+

Agent
^^^^^

Catalog
+++++++

+---------------+----------------------------+------------------------------------------------------------------+
| |HTTP| Method | Path                       | Action                                                           |
+===============+============================+==================================================================+
| GET           | /catalog/agent             | Returns the agents from the catalog selected by the query in the |
|               |                            | request body (or all it the request body is empty).              |
|               +----------------------------+------------------------------------------------------------------+
|               | /catalog/agent/(string:id) | Returns the agent from the catalog selected by the given ``id``  |
|               |                            | and the query in the request body.                               |
+---------------+----------------------------+------------------------------------------------------------------+
| POST          | /catalog/agent             | Insert one or more new agents in the catalog.                    |
|               +----------------------------+------------------------------------------------------------------+
|               | /catalog/agent/(string:id) | Insert a new agents in the catalog with the given ``id``.        |
+---------------+----------------------------+------------------------------------------------------------------+
| PUT           | /catalog/agent             | Update one or more existing agents in the catalog.               |
|               +-------------------------+---------------------------------------------------------------------+
|               | /catalog/agent/(string:id) | Update the agent in the catalog with given ``id``.               |
+---------------+-------------------------+---------------------------------------------------------------------+
| DELETE        | /catalog/agent             | Delete the agents from the catalog selected by the query in the  |
|               |                            | request body (or all it the request body is empty).              |
|               +----------------------------+------------------------------------------------------------------+
|               | /catalog/agent/(string:id) | Delete the agent from the catalog selected by the given ``id``   |
|               |                            | and the query in the request body.                               |
+---------------+----------------------------+------------------------------------------------------------------+


Instance
++++++++

+---------------+-----------------------------+----------------------------------------------------------+
| |HTTP| Method | Path                        | Action                                                   |
+===============+=============================+==========================================================+
| GET           | /instance/agent             | Returns the agent instances selected by the query in the |
|               |                             | request body (or all it the request body is empty).      |
|               +-----------------------------+----------------------------------------------------------+
|               | /instance/agent/(string:id) | Returns the agent instances selected by the given ``id`` |
|               |                             | and the query in the request body.                       |
+---------------+-----------------------------+----------------------------------------------------------+
| POST          | /instance/agent             | Create one or more new agent instances.                  |
|               +-----------------------------+----------------------------------------------------------+
|               | /instance/agent/(string:id) | Create a new agent instances with the given ``id``.      |
+---------------+-----------------------------+----------------------------------------------------------+
| PUT           | /instance/agent             | Update one or more existing agent instances.             |
|               +-----------------------------+----------------------------------------------------------+
|               | /instance/agent/(string:id) | Update the agent instance with given ``id``.             |
+---------------+-----------------------------+----------------------------------------------------------+
| DELETE        | /instance/agent             | Delete the agent instances selected by the query in the  |
|               |                             | request body (or all it the request body is empty).      |
|               +-----------------------------+----------------------------------------------------------+
|               | /instance/agent/(string:id) | Delete the agent instance selected by the given ``id``   |
|               |                             | and the query in the request body.                       |
+---------------+-----------------------------+----------------------------------------------------------+


eBPF Program
^^^^^^^^^^^^

Catalog
+++++++

+---------------+-----------------------------------+---------------------------------------------------------------------------+
| |HTTP| Method | Path                              | Action                                                                    |
+===============+===================================+===========================================================================+
| GET           | /catalog/ebpf-program             | Returns the |eBPF| programs from the catalog selected by the query in the |
|               |                                   | request body (or all it the request body is empty).                       |
|               +-----------------------------------+---------------------------------------------------------------------------+
|               | /catalog/ebpf-program/(string:id) | Returns the |eBPF| program from the catalog selected by the given ``id``  |
|               |                                   | and the query in the request body.                                        |
+---------------+-----------------------------------+---------------------------------------------------------------------------+
| POST          | /catalog/ebpf-program             | Insert one or more new |eBPF| programs in the catalog.                    |
|               +-----------------------------------+-------------------------------------------------------------------------- +
|               | /catalog/ebpf-program/(string:id) | Insert a new |eBPF| programs in the catalog with the given ``id``.        |
+---------------+-----------------------------------+---------------------------------------------------------------------------+
| PUT           | /catalog/ebpf-program             | Update one or more existing |eBPF| programs in the catalog.               |
|               +-----------------------------------+---------------------------------------------------------------------------+
|               | /catalog/ebpf-program/(string:id) | Update the |eBPF| program in the catalog with given ``id``.               |
+---------------+-----------------------------------+---------------------------------------------------------------------------+
| DELETE        | /catalog/ebpf-program             | Delete the |eBPF| programs from the catalog selected by the query in the  |
|               |                                   | request body (or all it the request body is empty).                       |
|               +-----------------------------------+---------------------------------------------------------------------------+
|               | /catalog/ebpf-program/(string:id) | Delete the |eBPF| program from the catalog selected by the given ``id``   |
|               |                                   | and the query in the request body.                                        |
+---------------+-----------------------------------+---------------------------------------------------------------------------+


Instance
++++++++

+---------------+-------------------------------------+------------------------------------------------------------------+
| |HTTP| Method | Path                               | Action                                                            |
+===============+====================================+===================================================================+
| GET           | /instance/ebpf-program             | Returns the |eBPF| program instances selected by the query in the |
|               |                                    | request body (or all it the request body is empty).               |
|               +------------------------------------+-------------------------------------------------------------------+
|               | /instance/ebpf-program/(string:id) | Returns the |eBPF| program instances selected by the given ``id`` |
|               |                                    | and the query in the request body.                                |
+---------------+------------------------------------+-------------------------------------------------------------------+
| POST          | /instance/ebpf-program             | Create one or more new |eBPF| program instances.                  |
|               +------------------------------------+-------------------------------------------------------------------+
|               | /instance/ebpf-program/(string:id) | Create a new |eBPF| program instances with the given ``id``.      |
+---------------+------------------------------------+-------------------------------------------------------------------+
| PUT           | /instance/ebpf-program             | Update one or more existing |eBPF| program instances.             |
|               +------------------------------------+-------------------------------------------------------------------+
|               | /instance/ebpf-program/(string:id) | Update the |eBPF| program instance with given ``id``.             |
+---------------+------------------------------------+-------------------------------------------------------------------+
| DELETE        | /instance/ebpf-program             | Delete the |eBPF| program instances selected by the query in the  |
|               |                                    | request body (or all it the request body is empty).               |
|               +------------------------------------+-------------------------------------------------------------------+
|               | /instance/ebpf-program/(string:id) | Delete the |eBPF| program instance selected by the given ``id``   |
|               |                                    | and the query in the request body.                                |
+---------------+------------------------------------+-------------------------------------------------------------------+


Data
^^^^
+---------------+-------------------+----------------------------------------------------------------------+
| |HTTP| Method | Path              | Action                                                               |
+===============+===================+======================================================================+
| GET           | /data             | Returns the collected data selected by the query in the request body |
|               |                   | (or all it the request body is empty).                               |
|               +-------------------+----------------------------------------------------------------------+
|               | /data/(string:id) | Returns the collected data selected by the given ``id``              |
|               |                   | and the query in the request body.                                   |
+---------------+-------------------+----------------------------------------------------------------------+
| POST          | /data             | Create one or more new collected data.                               |
|               +-------------------+----------------------------------------------------------------------+
|               | /data/(string:id) | Create a new collected data with the given ``id``.                   |
+---------------+-------------------+----------------------------------------------------------------------+
| PUT           | /data             | Update one or more existing collected data.                          |
|               +-------------------+----------------------------------------------------------------------+
|               | /data/(string:id) | Update the collected data with given ``id``.                         |
+---------------+-------------------+----------------------------------------------------------------------+
| DELETE        | /data             | Delete the collected data selected by the query in the request body  |
|               |                   | (or all it the request body is empty).                               |
|               +-------------------+----------------------------------------------------------------------+
|               | /data/(string:id) | Delete the collected data selected by the given ``id``               |
|               |                   | and the query in the request body.                                   |
+---------------+-------------------+----------------------------------------------------------------------+


Guide
-----

See the Swagger Schema (`|YAML| <api/swagger.yaml>`_, `|JSON| <api/swagger.json>`_) and the relative **documentation** (|REST|
endpoint ``/api/doc </api/doc>``) more details about the |REST| endpoints and relative formats and
requirements of request and response.


Installation
------------

1. Prerequisite

   - python (version >= 3.5)
   - pip (for python 3)

2. Clone the repository.

.. code-block:: console

  git clone https://gitlab.com/astrid-repositories/cb-manager.git
  cd cb-manager

3. Install the dependencies.

.. code-block:: console

  pip3 install -r requirements.txt


Configuration
-------------

The configurations are stored in the `config.ini <config.ini>`_ file.

+----------------+-----------------+--------------------+---------------------------------------------------------+
| Section        | Setting         | Default value      | Note                                                    |
+================+=================+====================+=========================================================+
| context=broker | host            | 0.0.0.0            | |IP| address to accept requests.                        |
|                +-----------------+--------------------+---------------------------------------------------------+
|                | port            | 5000               | |TCP| Port of the |REST| Server.                        |
+----------------+-----------------+--------------------+---------------------------------------------------------+
| heartbeat      | timeout         | 5s                 | Timeout for heartbeat with |LCP|.                       |
|                +-----------------+--------------------+---------------------------------------------------------+
|                | period          | 10s                | Period for the heartbeat with the |LCP|.                |
|                +-----------------+--------------------+---------------------------------------------------------+
|                | auth-expiration | 5min               | Period for auth expiration                              |
|                |                 |                    | used in the heartbeat with the |LCP|.                   |
+----------------+-----------------+--------------------+---------------------------------------------------------+
| elasticsearch  | endpoint        | elasticsearch:9200 | Elasticsearch server hostname/|IP|:port.                |
|                +-----------------+--------------------+---------------------------------------------------------+
|                | timeout         | 20s                | Timeout for the connection to Elasticsearch.            |
|                +-----------------+--------------------+---------------------------------------------------------+
|                | retry-period    | 1min               | Period to retry the connection to Elasticsearch.        |
+----------------+-----------------+--------------------+---------------------------------------------------------+
| dev            | username        | cb-manager         | Username for |HTTP| authentication (for developer use). |
|                +-----------------+--------------------+---------------------------------------------------------+
|                | password        | astrid [9]_        | Password for |HTTP| authentication (for developer use). |
+----------------+-----------------+--------------------+---------------------------------------------------------+


Usage
-----

Display help
^^^^^^^^^^^^

```bash
python3 main.py -h
```

.. glossary::

  ACL
    Access Control Lis

  API
    Application Program Interface

  BA
    Basic Authentication

  BPF
    Berkeley Packet Filter

  CB
    Context Broker

  CRUD
    Create - Read - Update - Delete

  DB
    Database

  eBPF
    extended BPF

  ELK
    Elastic - LogStash - Kibana

  Exec_Env
    Execution Environment

  gRPC
    Google RPC

  HOBA
    HTTP Origin-Bound Authentication

  HTTP
    Hyper Text Transfer Protocol

  ID
    Identification

  IP
    Internet Protocol

  JSON
    Java Object Notation

  LCP
    Local Control Plane

  LDAP
    Lightweight Directory Access Protocol

  RBAC
    Role-Based Access Control

  regex
    regular expression

  REST
    Representational State Transfer

  RFC
    Request For Comments

  RPC
    Remote Procedure Call

  SCM
    Security Context Model

  SLA
    Service Level Agreements

  SQL
    Structured Query Language

  TCP
    Transmission Control Protocol

  VNF
    Virtual Network Function

  YANG
    Yet Another Next Generation

  YAML
    YAML Ain't Markup Language


.. _references:

References
----------

.. [1] In the dash-case (also referred as **hyphen-case** or **kebab-case**) format all the letters are lower-case,
       the punctuation is not allowed and the words are separated by single dash (or hyphen: -). Example: ``exec-env``.

.. [2] We use the terms properties, fields and attributes interchangeably.

.. [3] In the snake-case format all the letters are lower-case, the punctuation is not allowed and the
       words are separated by single underscore (_). Example: ``exec_env_id``.

.. [4] In our architecture the agents are Beats from Elastic Stack. Notwithstanding, the data model refers
       to a generic agent allowing to possibility to use different types.

.. [5] In Elasticsearch, each document is identified by a unique id. For obvious reasons, in the description of
       the following indices, we omit the description of all the id fields.

.. [6] "Getting started with Beats," [Online]. Available: libbeat_.

.. [7] "Polycube. eBPF/XDP-based software framework for fast network services running in the Linux kernel,"
       [Online]. Available: `Polycube in GitHub`_.

.. [8] With nested index, we refer to index that are embedded inside your parent one,
       `managing relations inside elasticsearch`_

.. [9] Stored in hashed sha256 version.


.. _libbeat: https://www.elastic.co/guide/en/beats/libbeat/current/getting-started.html
.. _`Polycube in GitHub`: https://github.com/polycube-network/polycube
.. _`managing relations inside elasticsearch`: https://www.elastic.co/blog/managing-relations-inside-elasticsearch


.. |APIs| replace:: :abbr:`APIs (Application Program Interfaces)`
.. |DB| replace:: :abbr:`DB (DataBase)`
.. |eBPF| replace:: :abbr:`eBPF (extended Berkeley Packet Filter)`
.. |HTTP| replace:: :abbr:`HTTP (HyperText Transfer Protocol)`
.. |IP| replace:: :abbr:`IP (Internet Protocol)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |LCP| replace:: :abbr:`LCP (Local Control Plane)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
.. |TCP| replace:: :abbr:`TCP (Transmission Control Protocol)`
.. |YAML| replace:: :abbr:`YAML (YAML Ain't Markup Language )`
