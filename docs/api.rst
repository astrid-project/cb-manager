.. _api:


API
===

.. currentmodule:: api

.. autofunction:: api


Error Handler
-------------

.. currentmodule:: api.error_handler

.. autoclass:: Base_Handler
    :members:
    :inherited-members:

.. autoclass:: Bad_Request_Handler
    :members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Handler
    :members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Handler
    :members:
    :inherited-members:


Media Handler
-------------

.. currentmodule:: api.media_handler

.. autoclass:: XML_Handler
    :members:
    :inherited-members:

.. autoclass:: YAML_Handler
    :members:
    :inherited-members:


Middleware
----------

.. currentmodule:: api.middleware

.. autoclass:: Basic_Auth_Backend_Middleware
    :members:
    :inherited-members:

.. autoclass:: Negotiation_Middleware
    :members:
    :inherited-members:


Spec
----

.. currentmodule:: api.spec

.. autoclass:: Spec
    :members:
    :inherited-members:


Docstring
---------

.. currentmodule:: docstring

.. autodecorator:: docstring


Document
--------

.. currentmodule:: document.base

.. autoclass:: Base_Document
    :members:
    :inherited-members:


Agent
^^^^^

.. currentmodule:: document.agent.catalog

.. autoclass:: Agent_Catalog_Document
    :members:
    :inherited-members:

.. currentmodule:: document.agent.instance

.. autoclass:: Agent_Instance_Document
    :members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

.. currentmodule:: document.ebpf_program.catalog

.. autoclass:: eBPF_Program_Catalog_Document
    :members:
    :inherited-members:

.. currentmodule:: document.ebpf_program.instance

.. autoclass:: eBPF_Program_Instance_Document
    :members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: document.connection

.. autoclass:: Connection_Document
    :members:
    :inherited-members:


Data
^^^^

.. currentmodule:: document.data

.. autoclass:: Data_Document
    :members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: document.exec_env

.. autoclass:: Exec_Env_Document
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Document
    :members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: document.network_link

.. autoclass:: Network_Link_Document
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Document
    :members:
    :inherited-members:

Lib
---

.. currentmodule:: lib.elasticsearch

.. autofunction:: connection

.. currentmodule:: lib.heartbeat

.. autofunction:: heartbeat

.. currentmodule:: lib.http

.. autoclass:: HTTP_Method
    :members:
    :inherited-members:

.. autoclass:: HTTP_Status
    :members:
    :inherited-members:


Response
--------

.. currentmodule:: lib.response

.. autoclass:: Base_Response
    :members:
    :inherited-members:

.. autoclass:: Bad_Request_Response
    :members:
    :inherited-members:

.. autoclass:: Conflict_Response
    :members:
    :inherited-members:

.. autoclass:: Content_Response
    :members:
    :inherited-members:

.. autoclass:: Created_Response
    :members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Response
    :members:
    :inherited-members:

.. autoclass:: No_Content_Response
    :members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response
    :members:
    :inherited-members:

.. autoclass:: Not_Found_Response
    :members:
    :inherited-members:

.. autoclass:: Not_Modified_Response
    :members:
    :inherited-members:

.. autoclass:: Ok_Response
    :members:
    :inherited-members:

.. autoclass:: Reset_Content_Response
    :members:
    :inherited-members:

.. autoclass:: Unauthorized_Response
    :members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response
    :members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response
    :members:
    :inherited-members:


Reader
------

.. currentmodule:: reader.arg

.. autoclass:: Arg_Reader
    :members:
    :inherited-members:

.. currentmodule:: reader.config

.. autoclass:: Config_Reader
    :members:
    :inherited-members:

.. currentmodule:: reader.query

.. autoclass:: Query_Reader
    :members:
    :inherited-members:


Resource
--------

.. currentmodule:: resource

.. autofunction:: routes

.. currentmodule:: resource.base

.. autoclass:: Base_Resource
    :members:
    :inherited-members:

.. currentmodule:: resource.base.handler.lcp

.. autoclass:: LCP
    :members:
    :inherited-members:


Agent
^^^^^

.. currentmodule:: resource.agent.catalog

.. autoclass:: Agent_Catalog_Resource
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Selected_Resource
    :members:
    :inherited-members:

.. currentmodule:: resource.agent.instance

.. autoclass:: Agent_Instance_Resource
    :members:
    :inherited-members:

.. autoclass:: Agent_Instance_Selected_Resource
    :members:
    :inherited-members:

.. currentmodule:: resource.agent.handler.lcp

.. autoclass:: LCP
    :members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

.. currentmodule:: resource.ebpf_program.catalog

.. autoclass:: eBPF_Program_Catalog_Resource
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Selected_Resource
    :members:
    :inherited-members:

.. currentmodule:: resource.ebpf_program.instance

.. autoclass:: eBPF_Program_Instance_Resource
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Instance_Selected_Resource
    :members:
    :inherited-members:

.. currentmodule:: resource.ebpf_program.handler.lcp

.. autoclass:: LCP
    :members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: resource.exec_env

.. autoclass:: Exec_Env_Resource
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Selected_Resource
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Resource
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Selected_Resource
    :members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: resource.network_link

.. autoclass:: Network_Link_Resource
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Selected_Resource
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Resource
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Selected_Resource
    :members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: resource.connection

.. autoclass:: Connection_Resource
    :members:
    :inherited-members:

.. autoclass:: Connection_Selected_Resource
    :members:
    :inherited-members:


Data
^^^^

.. currentmodule:: resource.data

.. autoclass:: Data_Resource
    :members:
    :inherited-members:

.. autoclass:: Data_Selected_Resource
    :members:
    :inherited-members:


Schema
------

.. currentmodule:: schema.validate

.. autoclass:: In
    :members:
    :inherited-members:

.. autoclass:: Unique_List
    :members:
    :inherited-members:

.. currentmodule:: schema.base

.. autoclass:: Base_Schema
    :members:
    :inherited-members:


Agent
^^^^^

Catalog
"""""""

.. currentmodule:: schema.agent.catalog

.. autoclass:: Agent_Catalog_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Action_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Action_Config_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Parameter_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Parameter_Config_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Resource_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Resource_Config_Schema
    :members:
    :inherited-members:


Instance
""""""""

.. currentmodule:: schema.agent.instance

.. autoclass:: Agent_Instance_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Instance_Operation_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Instance_Action_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Instance_Parameter_Schema
    :members:
    :inherited-members:

.. autoclass:: Agent_Instance_Resource_Schema
    :members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

Catalog
"""""""

.. currentmodule:: schema.ebpf_program.catalog

.. autoclass:: eBPF_Program_Catalog_Schema
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Parameter_Schema
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Schema
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Metric_Schema
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Schema
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Label_Schema
    :members:
    :inherited-members:


Instance
""""""""

.. currentmodule:: schema.ebpf_program.instance

.. autoclass:: eBPF_Program_Instance_Schema
    :members:
    :inherited-members:

.. autoclass:: eBPF_Program_Instance_Parameter_Schema
    :members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: schema.exec_env

.. autoclass:: LCP_Schema
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Schema
    :members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Schema
    :members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: schema.network_link

.. autoclass:: Network_Link_Schema
    :members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Schema
    :members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: schema.connection

.. autoclass:: Connection_Schema
    :members:
    :inherited-members:

.. currentmodule:: schema.data


Data
^^^^

.. autoclass:: Data_Schema
    :members:
    :inherited-members:


Query Request
^^^^^^^^^^^^^

.. currentmodule:: schema.query_request

.. autoclass:: Query_Request_Schema
    :members:
    :inherited-members:

.. autoclass:: Query_Request_Order_Schema
    :members:
    :inherited-members:

.. autoclass:: Query_Request_Limit_Schema
    :members:
    :inherited-members:

.. autoclass:: Query_Request_Filter_Schema
    :members:
    :inherited-members:

.. autoclass:: Query_Request_Clause_Schema
    :members:
    :inherited-members:


Response
^^^^^^^^

.. currentmodule:: schema.response

.. autoclass:: Exception_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Base_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Bad_Request_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Conflict_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Content_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Created_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: No_Content_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Not_Found_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Not_Modified_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Ok_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Reset_Content_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Unauthorized_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response_Schema
    :members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response_Schema
    :members:
    :inherited-members: